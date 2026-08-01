# Daniel Rojas — Consultor de IA y Diseño para Pymes

Consultor de IA y diseño para Pymes. Aliado estratégico (Fractional AI & Design Officer): auditoría de procesos primero, código después.

- **Sitio:** https://decompas-318.netlify.app

## Estructura

```
index.html                 Landing principal (estática, con calculadora de impacto integrada)
landing/calculadora.html   Widget standalone de la calculadora de impacto de IA
leads/                     Lead Engine: extracción de Pymes (Google Maps API/scraping, directorios)
score/                     DeCompas Score: auditor 0-100 de presencia digital + test de WhatsApp
outreach/                  Reportes HTML personalizados + mensajes WhatsApp/Email por lead
.opencode/skills/          Skills para OpenCode (agent-browser, mcp-builder, frontend-design, vercel-rules, find-skills)
```

## Correr localmente

```bash
# Landing (abre en http://localhost:5173)
npm run dev
# o sin Node:
python -m http.server 5173

# Build para deploy (Netlify)
npm run build

# Lead Engine (Paso A)
pip install -r requirements.txt
python leads/run.py --source demo
python leads/run.py --source google_maps --query restaurantes --city Monterrey --max 50

# DeCompas Score (Paso B)
python score/run_score.py --lead data/<leads>.json

# Outreach
python outreach/run_outreach.py --scored data/<scored>.json
```

## Configuración

- `GOOGLE_MAPS_API_KEY` en `.env` para el Lead Engine (Places API).
- WhatsApp de contacto: +573174446641 (edítalo en `index.html`).
- Despliegue: Netlify con `netlify.toml` (build `npm run build`, publish `dist`).
