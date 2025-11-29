import { client } from '~/generated/api/client.gen';

export default defineNuxtPlugin(() => {
    const token = useCookie('access_token');
    client.setConfig({
        baseUrl: useRuntimeConfig().public.backendApiUrl,
        auth: () => token.value || undefined,
    });
});
