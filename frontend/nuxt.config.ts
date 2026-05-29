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
        '@nuxtjs/i18n',
        '@nuxt/eslint',
        '@nuxt/image',
        '@nuxt/scripts',
        '@nuxt/test-utils',
        '@nuxt/ui',
        '@nuxt/content',
        '@compodium/nuxt',
    ],

    i18n: {
        strategy: 'prefix_except_default',
        defaultLocale: 'ru',
        locales: [
            { code: 'ru', language: 'ru-RU', name: 'Русский', file: 'ru.json' },
            { code: 'en', language: 'en-US', name: 'English', file: 'en.json' },
        ],
        langDir: 'locales/',
        detectBrowserLanguage: {
            useCookie: true,
            cookieKey: 'i18n_redirected',
            redirectOn: 'root',
        },
    },

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
