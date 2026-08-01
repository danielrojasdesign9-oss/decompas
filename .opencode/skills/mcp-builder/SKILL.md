---
name: mcp-builder
description: Use when the user needs to create or integrate MCP (Model Context Protocol) connectors and servers, generate them from OpenAPI/Swagger specs, connect CRMs (HubSpot, Zoho, WhatsApp Business API, Airtable), or set up OAuth2 / API Key / Bearer auth. Trigger on keywords like "MCP", "conector", "OpenAPI", "Swagger", "integrar CRM", "WhatsApp API", "server MCP".
---

# MCP Builder

Crea e integra conectores MCP (Model Context Protocol) en tiempo récord, sin escribir conectores manuales desde cero.

## Capacidades

- Ingesta de especificaciones OpenAPI / Swagger / REST APIs y conversión automática a Tools y Resources de MCP.
- Generación de conectores para CRMs y plataformas: HubSpot, Zoho, WhatsApp Business API, Airtable, Google Sheets.
- Autenticación dinámica: OAuth2, API Keys, Bearer Tokens (con interpolación `{env:VAR}` para secretos).
- Creación de Tools y Resources en tiempo de ejecución con validación de esquemas.
- Generación de la config `mcp` de opencode (tipo `local` o `remote`) lista para copiar en `opencode.json`.

## Reglas de ejecución

1. **Validar esquemas primero:** comprobar request/response de cada endpoint antes de registrar el conector; descartar endpoints sin definir en el spec.
2. **Manejo de errores transparente:** implementar retry con backoff y mapeo claro de errores 4xx/5xx; nunca exponer secretos en mensajes de error.
3. **Rate-limiting:** respetar límites del proveedor y añadir throttling configurable.
4. **Secretos:** usar variables de entorno (nunca hardcodear API keys) y referenciarlas con `{env:VAR}` en `opencode.json`.
5. **Forma del conector:** `mcp` es un objeto por nombre de servidor; `command` es un array de strings; `type` es obligatorio (`local` o `remote`).
6. **Entregable:** documentar en markdown el conector generado: endpoints expuestos, autenticación usada, ejemplos de llamada y cómo probarlo.
