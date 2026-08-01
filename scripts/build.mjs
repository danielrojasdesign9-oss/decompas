// Copia solo los archivos estáticos del sitio a dist/ para el deploy en Netlify.
import { copyFileSync, mkdirSync, cpSync, existsSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(root, "dist");

rmSync(dist, { recursive: true, force: true });
mkdirSync(join(dist, "landing"), { recursive: true });

const files = ["index.html", "favicon.svg", "landing/calculadora.html"];
for (const f of files) {
  if (!existsSync(join(root, f))) {
    console.error(`Falta archivo: ${f}`);
    process.exit(1);
  }
  copyFileSync(join(root, f), join(dist, f));
}

console.log("Build listo: dist/ contiene solo la landing estática.");
