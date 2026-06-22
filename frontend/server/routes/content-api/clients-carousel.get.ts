import { readFileSync } from "fs";
import { resolve } from "path";

export default defineEventHandler(() => {
  const filePath = resolve("./server/data/content.json");
  try {
    const store = JSON.parse(readFileSync(filePath, "utf-8"));
    return store["clients-carousel"] ?? [];
  } catch {
    return [];
  }
});
