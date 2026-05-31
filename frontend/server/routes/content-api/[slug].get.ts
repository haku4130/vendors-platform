import { readFileSync } from 'fs';
import { resolve } from 'path';

export default defineEventHandler((event) => {
  const slug = getRouterParam(event, 'slug')!;
  const filePath = resolve('./server/data/content.json');

  try {
    const store = JSON.parse(readFileSync(filePath, 'utf-8'));
    return store[slug] ?? { ru: '', en: '' };
  } catch {
    return { ru: '', en: '' };
  }
});
