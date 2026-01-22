// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs';

export default withNuxt({
    'vue/html-self-closing': [
        'error',
        {
            html: {
                void: 'always',
            },
        },
    ],
});
