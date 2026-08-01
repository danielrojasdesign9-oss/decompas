# OpenCode Skills & DeCompas — Framework de Experiencia Agentic (AX)

> **Autor:** DeCompas — Consultoría de Innovación, IA y Diseño para Pymes.
> **Plataforma:** https://decompas.netlify.app
> **Propósito:** Configurar un ecosistema de skills para OpenCode que permita (1) desarrollar agentes especializados y (2) automatizar un embudo de prospección local con valor agregado para Pymes.

---

## PARTE 1: Configuración de Skills para OpenCode

Las skills se instalan en el proyecto siguiendo el formato estándar de OpenCode:

```
.opencode/skills/<nombre>/SKILL.md
```

Cada `SKILL.md` usa frontmatter con `name` (obligatorio, minúsculas y guiones) y `description` (qué hace y cuándo activarse, en tercera persona y con keywords de disparo).

---

### 1. Skill: Agent Browser (Navegación e Interacción Web Autónoma)

- **ID:** `agent-browser`
- **Descripción:** Navegador headless controlado por IA capaz de interactuar con el DOM, ejecutar pruebas de usuario E2E y scraping estructurado.

**Capacidades:**
- Navegación web en tiempo real con renderizado de JavaScript dinámico.
- Interacción con elementos: `click`, `type`, `scroll`, `hover`, `drag_and_drop`.
- Captura de screenshots visuales y análisis de layout UI.
- Auditoría E2E de flujos de conversión de Pymes (formularios, checkout, agenda, WhatsApp).

**Reglas de Ejecución:**
1. Ante cada navegación, verificar certificados SSL y tiempo de respuesta; registrar el error en lugar de abortar.
2. Extraer datos en formatos JSON estructurados para alimentar diagnósticos y CRMs.
3. Simular personas de usuario (User Personas) para detectar fricciones en el flujo de ventas.
4. Respetar rate-limiting y `robots.txt`; añadir delays aleatorios entre peticiones.

---

### 2. Skill: MCP Builder (Model Context Protocol Generator)

- **ID:** `mcp-builder`
- **Descripción:** Crea e integra conectores MCP (Model Context Protocol) en tiempo récord, sin escribir conectores manuales.

**Capacidades:**
- Ingesta de especificaciones OpenAPI / Swagger / REST APIs.
- Generación de conectores para CRMs (HubSpot, Zoho, WhatsApp Business API, Airtable, Google Sheets).
- Autenticación dinámica (OAuth2, API Keys, Bearer Tokens con `{env:VAR}`).
- Creación de Tools y Resources en tiempo de ejecución con validación de esquemas.

**Reglas de Ejecución:**
1. Validar esquemas de request/response antes de registrar el conector; descartar endpoints no definidos.
2. Implementar rate-limiting y manejo transparente de errores 4xx/5xx con retry y backoff.
3. Nunca hardcodear secretos; usar variables de entorno e interpolación `{env:VAR}`.

---

### 3. Skill: Frontend Design System & Typography Engine

- **ID:** `frontend-design-system`
- **Descripción:** Motor de diseño UI/UX con +50 presets estilísticos y pares tipográficos profesionales para eliminar la estética genérica de IA.

**Estilos Disponibles:**
- *Editorial Premium, Neobrutalism, Swiss Minimalist, Warm Organic, Dark Cyber, B2B Modern Enterprise.*

**Capacidades:**
- Selección inteligente de paletas cromáticas basadas en la identidad de marca (regla 60-30-10).
- Configuración de componentes en Tailwind CSS, Radix UI o CSS Modules.
- Optimización de microinteracciones, jerarquía visual y espaciado (8pt grid system).

**Reglas de Ejecución:**
1. Prohibido usar estilos genéricos por defecto (ej. Tailwind predeterminado sin personalizar).
2. Aplicar contraste WCAG AAA para legibilidad comercial.
3. Justificar el preset elegido en función del sector de la Pyme.

---

### 4. Skill: Vercel UI/UX & Quality Rules Engine

- **ID:** `vercel-design-rules`
- **Descripción:** Motor de auditoría con +100 reglas de calidad de software, diseño y rendimiento inspiradas en los estándares de Vercel.

**Checklist de Reglas:**
- **Performance:** Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms), imágenes Next.js / WebP optimizadas, fuentes con `font-display: swap`.
- **UX/UI:** Estados de carga (skeletons), manejo de errores visibles, estados vacíos (empty states), feedback inmediato.
- **Accesibilidad & SEO:** HTML semántico, ARIA labels, Open Graph tags, alt texts dinámicos, contraste AA/AAA.
- **Código:** Zero-layout shifts, server vs. client components bien delimitados.

**Reglas de Ejecución:**
1. Ejecutar checklist automático antes de sugerir despliegues a producción.
2. Asignar un puntaje de calidad (0 a 100) desglosado por categoría e indicar soluciones específicas para cada fallo.

---

### 5. Skill: Find & Auto-Install Skills (Catalog Discovery)

- **ID:** `find-skills`
- **Descripción:** Descubridor autónomo e instalador de habilidades y extensiones según la meta del proyecto.

**Capacidades:**
- Análisis del prompt/requerimiento del usuario.
- Búsqueda en el catálogo público de OpenCode / MCP Registries.
- Evaluación de compatibilidad y dependencias.
- Auto-instalación e inyección de contexto en `.opencode/skills/<nombre>/SKILL.md`.

**Reglas de Ejecución:**
1. Confirmar dependencias necesarias antes de instalar.
2. Requerir confirmación explícita del usuario antes de instalar cualquier skill de terceros.
3. Notificar al usuario las nuevas capacidades añadidas y recordar reiniciar opencode.

---

## PARTE 2: Estrategia de Automatización y Crecimiento para DeCompas

> **Objetivo:** posicionarse como el **aliado estratégico de IA y Diseño para Pymes**, impulsando https://decompas.netlify.app mediante un embudo de prospección local automatizado que genera valor antes de vender.

### 1. Embudo Tecnológico de Prospección Local (Lead Engine)

```
[ Google Maps / API / Directorios ]
                │
                ▼
   [ Scraping & Lead Extraction ] ──── (Python + Agent Browser)
                │
                ▼
   [ Diagnóstico IA Automático ] ───── (Evaluación con Vercel Rules + Frontend Audit)
                │
                ▼
[ Landing Personalizada / Outreach ] ─── (Vía WhatsApp / Email enviando a DeCompas)
```

#### Paso A: Extracción e Identificación de Pymes Locales

Usando la skill `agent-browser` o librerías de Python (`googlemaps`, `playwright`):

- **Fuentes:** Google Maps, Cámaras de Comercio locales, Instagram Business, directorios sectoriales (restaurantes, clínicas, tiendas de retail, firmas profesionales).
- **Datos a capturar:** Nombre de la empresa, sitio web, teléfono de WhatsApp, calificación en Google, número de reseñas y presencia en redes.

#### Paso B: Diagnóstico Automático "DeCompas Score"

Antes de contactarlos, generar valor inmediato con un script que audite automáticamente su presencia digital:

1. **¿Tienen sitio web?**
   - **No tienen:** oportunidad de creación de ecosistema digital desde cero.
   - **Sí tienen:** ejecutar `vercel-design-rules` y `frontend-design-system` para detectar:
     - Carga lenta o nula respuesta en móviles.
     - Estética obsoleta o genérica.
     - Falta de asistente/chat de ventas con IA para capturar leads.

2. **¿Responden rápido por WhatsApp / Redes?**
   - Simular un mensaje de cliente potencial. Si tardan más de 15 minutos en responder, identificar la oportunidad de un **Agente MCP de Automatización de Ventas**.

**Output esperado:** reporte de una página (DeCompas Score 0-100) por Pyme, listo para el outreach.

### 2. Cadena de Contacto & Estrategia de Inbound/Outbound

#### A. Estrategia Outreach (Cold Outreach con Valor Agregado)

Enviar un video corto (Loom/Veed de 60 segundos) o un reporte visual interactivo en lugar del mensaje de ventas típico:

> *"Hola [Nombre del Dueño/Gerente], vi tu negocio en [Ciudad/Plataforma]. Analizamos la experiencia digital de [Nombre del Negocio] y notamos 2 detalles en el flujo de ventas móvil donde están perdiendo clientes frente a la competencia. Preparamos un diagnóstico rápido sin costo aquí: [Link a Landing/DeCompas con reporte]. En DeCompas nos enfocamos en entender a fondo el negocio y resolverlo con IA y diseño."*

#### B. Conversión en DeCompas (https://decompas.netlify.app)

Para maximizar la conversión en la landing actual:

1. **Calculadora de Impacto de IA para Pymes:** widget interactivo donde el dueño selecciona su sector y recibe un estimado de cuántas horas/dinero puede ahorrar automatizando procesos con IA.
2. **Sección "Diagnóstico Gratuito de 3 Minutos":** formulario o chatbot interactivo que escanea la web del cliente en tiempo real y entrega un reporte inicial inmediato.
3. **Casos de Estudio Enfocados en Resultados:** mostrar resultados de negocio, no tecnología (MCP, LLMs, Tailwind):
   - *"Cómo ayudamos a una Pyme local a aumentar sus citas en un 40% implementando un agente de atención 24/7."*

### 3. Propuesta de Valor Diferenciadora (Posicionamiento)

1. **Auditoría de Procesos de Negocio Primero, Código Después:** no vender "páginas web", sino **soluciones operativas**.
2. **Partner Tecnológico (Fractional AI & Design Officer):** convertirse en el socio que actualiza y optimiza sistemas mes a mes, asegurando recurrencia (retainer mensual).
3. **Implementación Ágil de Agentes MCP:** crear conectores a sus sistemas actuales (CRM, bases de datos local, inventario) sin obligarlos a cambiar de software.

---

## Hoja de Ruta de Implementación

| Fase | Entregable | Skills / Herramientas |
| --- | --- | --- |
| 1. Setup del ecosistema | Skills instaladas y probadas en el proyecto | `find-skills`, `agent-browser` |
| 2. Lead Engine local | Script de extracción de Pymes (JSON normalizado) | `agent-browser`, Python (`googlemaps`, `playwright`) |
| 3. DeCompas Score | Auditor automático 0-100 + reporte de 1 página | `vercel-design-rules`, `frontend-design-system` |
| 4. Outreach automatizado | Secuencia WhatsApp/Email con reporte personalizado | Conectores `mcp-builder` |
| 5. Optimización de conversión | Calculadora de impacto + Diagnóstico de 3 minutos en la landing | `frontend-design-system`, `vercel-design-rules` |
| 6. Recurrencia | Retainer mensual como Fractional AI & Design Officer | `mcp-builder`, agentes de soporte |
