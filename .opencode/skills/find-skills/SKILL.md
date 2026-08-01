---
name: find-skills
description: Use when the user asks to discover, install, or update OpenCode skills and extensions, or wants to find capabilities for a project goal (e.g., scraping, MCP, design, testing). Searches the OpenCode catalog and MCP registries, evaluates compatibility, and installs. Trigger on keywords like "buscar skill", "instalar skill", "find skills", "catálogo de skills", "extensión", "nuevas capacidades".
---

# Find & Auto-Install Skills (Catalog Discovery)

Descubridor autónomo e instalador de skills y extensiones según la meta del proyecto.

## Capacidades

- Análisis del prompt/requerimiento del usuario para inferir la capacidad necesaria.
- Búsqueda en el catálogo público de OpenCode / MCP Registries / repositorios de skills.
- Evaluación de compatibilidad y dependencias (runtime, versiones, permisos requeridos).
- Instalación e inyección de contexto en `.opencode/skills/<name>/SKILL.md` o registro vía `skills.paths` en `opencode.json`.
- Notificación al usuario de las nuevas capacidades añadidas.

## Reglas de ejecución

1. **Confirmar dependencias:** verificar dependencias necesarias antes de instalar (Node, Python, binarios, API keys) y reportarlas al usuario.
2. **Confirmación antes de instalar:** la auto-instalación requiere confirmación del usuario; nunca instalar skills desconocidos sin consentimiento explícito. Presentar el candidato, su origen y qué permisos/archivos toca.
3. **Compatibilidad:** revisar que el skill siga el formato estándar (carpeta `<name>/SKILL.md` con frontmatter `name` + `description`) y que no haya colisiones de nombre con skills existentes.
4. **Documentar:** tras instalar, listar los skills/extensiones añadidos, su propósito y ejemplos de uso, y notificar que se debe reiniciar opencode para que cargue la nueva config.
5. **Seguridad:** no ejecutar scripts ni instalar paquetes de fuentes no verificadas; verificar autor/origen del skill.
