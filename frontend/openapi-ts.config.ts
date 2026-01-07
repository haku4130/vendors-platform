import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
    input: 'http://127.0.0.1:8000/api/v1/openapi.json',
    output: {
        path: 'app/generated/api',
    },
});
