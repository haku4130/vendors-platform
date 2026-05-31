import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

export default defineEventHandler(async (event) => {
    const token = getCookie(event, 'access_token');
    if (!token) throw createError({ statusCode: 401 });

    const { backendApiUrl } = useRuntimeConfig();

    const user = await $fetch<{ is_superuser?: boolean }>(
        `${backendApiUrl}/api/v1/users/me`,
        { headers: { Authorization: `Bearer ${token}` } },
    ).catch(() => null);

    if (!user?.is_superuser) {
        throw createError({
            statusCode: 403,
            message: 'Superuser access required',
        });
    }

    const slug = getRouterParam(event, 'slug')!;
    const body = await readBody<{ ru: string; en: string }>(event);
    const filePath = resolve('./server/data/content.json');

    const store = JSON.parse(readFileSync(filePath, 'utf-8'));
    store[slug] = { ru: body.ru ?? '', en: body.en ?? '' };
    writeFileSync(filePath, JSON.stringify(store, null, 2));

    return { ok: true };
});
