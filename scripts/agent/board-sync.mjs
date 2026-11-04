// Synchronise les issues du dépôt avec un GitHub Project (v2).
//
// Le statut de chaque carte est déduit des labels du cycle agent :
//   fermée           → Done
//   agent:blocked    → Blocked (ou reste en place si la colonne n'existe pas)
//   agent:review     → In review
//   agent:working    → In progress
//   agent:ready      → Ready
//   spec:review      → Spec review
//   agent:refine     → Refinement
//   (aucun)          → Backlog, uniquement si la carte n'a pas encore de statut
//                      (un déplacement manuel n'est jamais écrasé)
//
// Variables d'environnement :
//   GH_TOKEN         PAT avec les scopes `repo` + `project` (obligatoire)
//   REPO             owner/name (fourni par GitHub Actions via GITHUB_REPOSITORY)
//   PROJECT_OWNER    propriétaire du projet (défaut : owner du dépôt)
//   PROJECT_NUMBER   numéro du projet (visible dans son URL)
//   ISSUE_NUMBER     optionnel : ne synchroniser que cette issue
//   STATUS_FIELD     optionnel : nom du champ (défaut « Status »)
//   DRY_RUN=1        optionnel : affiche sans écrire

const token = process.env.GH_TOKEN;
const repo = process.env.REPO ?? process.env.GITHUB_REPOSITORY;
const projectNumber = Number(process.env.PROJECT_NUMBER);
const projectOwner = process.env.PROJECT_OWNER || repo?.split('/')[0];
const statusFieldName = process.env.STATUS_FIELD || 'Status';
const onlyIssue = process.env.ISSUE_NUMBER ? Number(process.env.ISSUE_NUMBER) : undefined;
const dryRun = process.env.DRY_RUN === '1';

if (!token || !repo || !projectNumber) {
  console.log('board-sync : GH_TOKEN, REPO ou PROJECT_NUMBER manquant — synchronisation ignorée.');
  process.exit(0);
}

// Noms de colonnes acceptés pour chaque statut logique (comparaison insensible à la casse).
const STATUS_CANDIDATES = {
  backlog: ['Backlog', 'Todo', 'To do', 'À faire'],
  refinement: ['Refinement', 'Raffinement', 'Spec', 'Backlog', 'Todo'],
  specReview: ['Spec review', 'Spec à valider', 'Refinement', 'Todo'],
  ready: ['Ready', 'Prêt', 'Todo', 'To do'],
  inProgress: ['In progress', 'En cours', 'Doing'],
  inReview: ['In review', 'Review', 'En revue'],
  blocked: ['Blocked', 'Bloqué'],
  done: ['Done', 'Terminé'],
};

async function rest(path) {
  const res = await fetch(`https://api.github.com/${path}`, {
    headers: {
      authorization: `Bearer ${token}`,
      accept: 'application/vnd.github+json',
      'x-github-api-version': '2022-11-28',
    },
  });
  if (!res.ok) throw new Error(`REST ${path} → ${res.status} ${await res.text()}`);
  return res.json();
}

async function graphql(query, variables) {
  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (!res.ok || json.errors) {
    throw new Error(`GraphQL → ${res.status} ${JSON.stringify(json.errors ?? json)}`);
  }
  return json.data;
}

async function loadProject() {
  const fields = `id title field(name: $field) {
    ... on ProjectV2SingleSelectField { id options { id name } }
  }`;
  for (const kind of ['user', 'organization']) {
    try {
      const data = await graphql(
        `query($login: String!, $number: Int!, $field: String!) {
          ${kind}(login: $login) { projectV2(number: $number) { ${fields} } }
        }`,
        { login: projectOwner, number: projectNumber, field: statusFieldName },
      );
      const project = data[kind]?.projectV2;
      if (project) return project;
    } catch (error) {
      if (kind === 'organization') throw error;
    }
  }
  throw new Error(`Projet #${projectNumber} introuvable pour ${projectOwner}`);
}

function resolveOptions(options) {
  const byName = new Map(options.map((o) => [o.name.trim().toLowerCase(), o]));
  return Object.fromEntries(
    Object.entries(STATUS_CANDIDATES).map(([key, names]) => [
      key,
      names.map((n) => byName.get(n.toLowerCase())).find(Boolean),
    ]),
  );
}

function desiredStatus(issue) {
  const labels = new Set(issue.labels.map((l) => (typeof l === 'string' ? l : l.name)));
  if (issue.state === 'closed') return 'done';
  if (labels.has('agent:blocked')) return 'blocked';
  if (labels.has('agent:review')) return 'inReview';
  if (labels.has('agent:working')) return 'inProgress';
  if (labels.has('agent:ready')) return 'ready';
  if (labels.has('spec:review')) return 'specReview';
  if (labels.has('agent:refine')) return 'refinement';
  return 'backlog';
}

async function listIssues() {
  if (onlyIssue) return [await rest(`repos/${repo}/issues/${onlyIssue}`)];
  const all = [];
  for (let page = 1; ; page++) {
    const batch = await rest(`repos/${repo}/issues?state=all&per_page=100&page=${page}`);
    all.push(...batch.filter((i) => !i.pull_request));
    if (batch.length < 100) return all;
  }
}

async function main() {
  const project = await loadProject();
  if (!project.field?.options) {
    throw new Error(`Champ « ${statusFieldName} » (sélection unique) absent du projet.`);
  }
  const options = resolveOptions(project.field.options);
  console.log(
    `Projet « ${project.title} » — colonnes : ${project.field.options.map((o) => o.name).join(', ')}`,
  );

  const issues = await listIssues();
  let changed = 0;
  for (const issue of issues) {
    if (issue.pull_request) continue;
    const key = desiredStatus(issue);
    const option = options[key];

    const added = dryRun
      ? null
      : await graphql(
          `
            mutation ($project: ID!, $content: ID!, $field: String!) {
              addProjectV2ItemById(input: { projectId: $project, contentId: $content }) {
                item {
                  id
                  fieldValueByName(name: $field) {
                    ... on ProjectV2ItemFieldSingleSelectValue {
                      name
                    }
                  }
                }
              }
            }
          `,
          { project: project.id, content: issue.node_id, field: statusFieldName },
        );
    const item = added?.addProjectV2ItemById.item;
    const current = item?.fieldValueByName?.name;

    if (!option) {
      if (key !== 'backlog') console.warn(`#${issue.number} : aucune colonne pour « ${key} ».`);
      continue;
    }
    // Ne jamais écraser un déplacement manuel par « Backlog ».
    if (key === 'backlog' && current) continue;
    if (current === option.name) continue;

    console.log(`#${issue.number} ${issue.title} : ${current ?? '∅'} → ${option.name}`);
    changed++;
    if (dryRun) continue;
    await graphql(
      `
        mutation ($project: ID!, $item: ID!, $field: ID!, $option: String!) {
          updateProjectV2ItemFieldValue(
            input: {
              projectId: $project
              itemId: $item
              fieldId: $field
              value: { singleSelectOptionId: $option }
            }
          ) {
            projectV2Item {
              id
            }
          }
        }
      `,
      { project: project.id, item: item.id, field: project.field.id, option: option.id },
    );
  }
  console.log(`${issues.length} issue(s) parcourue(s), ${changed} statut(s) mis à jour.`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
