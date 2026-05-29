import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const pathSerializer = join(
  root,
  'app/generated/api/core/pathSerializer.gen.ts',
);

let source = readFileSync(pathSerializer, 'utf8');
const broken =
  "'Deeply-nested arrays/objects aren't supported. Provide your own `querySerializer()` to handle these.'";
const fixed =
  '"Deeply-nested arrays/objects aren\'t supported. Provide your own `querySerializer()` to handle these."';

if (source.includes(broken)) {
  source = source.replace(broken, fixed);
  writeFileSync(pathSerializer, source);
}
