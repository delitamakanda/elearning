module.exports = {
    'declaration-block-trailing-semicolon': null,
    'no-descending-specificity': null,
    rules: {
        'at-rule-no-unknown': [true, {
            ignoreAtRules: [
                'tailwind',
                'apply',
                'variants',
                'responsive',
                'screen'
            ]
        }
    ]}
}
