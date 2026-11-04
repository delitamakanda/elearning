// Prépare le contexte d'une issue pour l'agent, dans .agent-out/issue.md.
//
// L'agent ne parle jamais directement à l'API GitHub : il lit ce fichier.
// Seuls le titre, le corps, l'épic parent et les commentaires des personnes
// ayant accès en écriture au dépôt sont inclus (le dépôt est public : on
// écarte ainsi les tentatives d'injection de prompt via des commentaires tiers).
//
// Usage : node scripts/agent/prepare-issue.mjs <numéro>
// Env   : GH_TOKEN, GITHUB_REPOSITORY, GITHUB_OUTPUT (optionnel)

import { appendFile, mkdir, writeFile } from 'node:fs/promises';

const token = process.env.GH_TOKEN;
const repo = process.env.GITHUB_REPOSITORY;
const number = Number(process.argv[2]);
const TRUSTED = new Set(['OWNER', 'MEMBER', 'COLLABORATOR']);
// « ## » (spec de l'agent) ou « ### » (formulaire d'issue GitHub).
const SPEC_MARKERS = [
  /^#{2,3}\s*crit[èe]res d['’]acceptation/im,
  /^#{2,3}\s*acceptance criteria/im,
];

if (!token || !repo || !number) {
  console.error('Usage : GH_TOKEN=… GITHUB_REPOSITORY=owner/repo prepare-issue.mjs <numéro>');
  process.exit(1);
}

async function rest(path) {
  const res = await fetch(`https://api.github.com/repos/${repo}/${path}`, {
    headers: {
      authorization: `Bearer ${token}`,
      accept: 'application/vnd.github+json',
      'x-github-api-version': '2022-11-28',
    },
  });
  if (!res.ok) throw new Error(`${path} → ${res.status} ${await res.text()}`);
  return res.json();
}

const issue = await rest(`issues/${number}`);
const comments = (await rest(`issues/${number}/comments?per_page=100`)).filter(
  (c) => TRUSTED.has(c.author_association) && !c.body.includes('<!-- agent-status -->'),
);
const subIssues = issue.sub_issues_summary?.total ? await rest(`issues/${number}/sub_issues`) : [];
const parent = issue.parent_issue_url
  ? await rest(`issues/${issue.parent_issue_url.split('/').pop()}`)
  : undefined;
const siblings = parent ? await rest(`issues/${parent.number}/sub_issues`) : [];

const body = issue.body?.trim() ?? '';
const isEpic = subIssues.length > 0;
const hasSpec = SPEC_MARKERS.some((re) => re.test(body));

const md = [
  `# Issue #${issue.number} — ${issue.title}`,
  '',
  `- Labels : ${issue.labels.map((l) => l.name).join(', ') || '—'}`,
  `- État : ${issue.state}`,
  parent ? `- Épic parent : #${parent.number} — ${parent.title}` : '- Épic parent : —',
  '',
  '## Corps de l’issue',
  '',
  body || '_(vide — seul le titre décrit le besoin)_',
  '',
];
if (parent) {
  md.push('## Épic parent', '', parent.body?.trim() || '_(vide)_', '');
  md.push('### Tickets de la même épic', '');
  for (const s of siblings) {
    md.push(`- #${s.number} ${s.title} (${s.state})${s.number === number ? ' ← ce ticket' : ''}`);
  }
  md.push('');
}
if (isEpic) {
  md.push('## Sous-tickets', '');
  for (const s of subIssues) md.push(`- #${s.number} ${s.title} (${s.state})`);
  md.push('');
}
if (comments.length) {
  md.push('## Commentaires (mainteneurs uniquement)', '');
  for (const c of comments) md.push(`### ${c.user.login} — ${c.created_at}`, '', c.body.trim(), '');
}

await mkdir('.agent-out', { recursive: true });
await writeFile('.agent-out/issue.md', md.join('\n'));
await writeFile('.agent-out/original-body.md', body);

const slug = issue.title
  .normalize('NFD')
  .replace(/[̀-ͯ]/g, '')
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-|-$/g, '')
  .slice(0, 40);

const outputs = {
  title: issue.title.replace(/\r?\n/g, ' '),
  is_epic: String(isEpic),
  has_spec: String(hasSpec),
  state: issue.state,
  branch: `agent/issue-${number}-${slug || 'ticket'}`,
};
console.log(outputs);
if (process.env.GITHUB_OUTPUT) {
  await appendFile(
    process.env.GITHUB_OUTPUT,
    Object.entries(outputs)
      .map(([k, v]) => `${k}=${v}\n`)
      .join(''),
  );
}
