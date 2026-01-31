// https://nuxt.com/docs/api/configuration/nuxt-config

const backendApiUrl =
    process?.env?.NUXT_PUBLIC_BACKEND_API_URL ?? 'http://localhost:8000';
const backendStaticUrl =
    process.env.NUXT_PUBLIC_BACKEND_STATIC_URL ??
    'http://localhost:8000/static';

export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },

    modules: [
        '@nuxt/eslint',
        '@nuxt/image',
        '@nuxt/scripts',
        '@nuxt/test-utils',
        '@nuxt/ui',
        '@nuxt/content',
        '@compodium/nuxt',
    ],

    css: ['~/assets/css/main.css'],

    ui: {
        colorMode: false,
    },

    runtimeConfig: {
        public: {
            backendApiUrl: backendApiUrl,
            backendStaticUrl: backendStaticUrl,
        },
    },

    nitro: {
        routeRules: {
            '/api/**': {
                proxy: `${backendApiUrl}/api/v1/**`,
            },
            '/backend/static/**': {
                proxy: `${backendStaticUrl}/**`,
            },
        },
        // Avoid slow prerender of Nuxt Content routes (e.g. /__nuxt_content/content/*) when content module is not used.
        prerender: { ignore: ['/__nuxt_content/**'] },
    },
    icon: {
        localApiEndpoint: '/icons',
    },
});
