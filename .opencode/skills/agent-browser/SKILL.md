---
name: agent-browser
description: Use when the user needs autonomous web browsing, real-time DOM interaction, E2E user testing, visual screenshot analysis, or structured scraping of websites, directories, Google Maps, or Pyme business listings. Trigger on keywords like "browser", "scraping", "extraer leads", "navegación web", "E2E", "screenshot", "auditar web".
---

# Agent Browser

Navegación e interacción web autónoma para recolección de datos, auditoría de UX y pruebas de usuario E2E.

## Capacidades

- Navegación web en tiempo real con renderizado de JavaScript dinámico.
- Interacción con el DOM: `click`, `type`, `scroll`, `hover`, `drag_and_drop`, `select`.
- Captura de screenshots visuales y análisis de layout UI.
- Auditoría E2E de flujos de conversión (formularios, checkout, WhatsApp, agenda).
- Extracción estructurada de datos a JSON para alimentar diagnósticos y CRMs.

## Casos de uso principales

1. **Lead Engine local (DeCompas):** extraer Pymes de Google Maps, directorios sectoriales, Cámaras de Comercio, Instagram Business. Capturar: nombre, sitio web, WhatsApp, calificación Google, número de reseñas, presencia en redes.
2. **Auditoría de presencia digital:** detectar si la Pyme tiene web, si carga rápido en móvil, estética del sitio, presencia de chat de ventas.
3. **Pruebas de fricción de ventas:** simular personas de usuario (User Personas) recorriendo el flujo de compra y detectando puntos de abandono.

## Reglas de ejecución

1. Ante cada navegación, verificar certificados SSL y tiempo de respuesta; si fallan, registrar el error en lugar de abortar.
2. Extraer los datos siempre en formatos JSON estructurados (campos normalizados: nombre, url, telefono, whatsapp, rating, reviews, redes).
3. Simular personas de usuario definidas (objetivo, frustraciones, dispositivo) para detectar fricciones en el flujo de ventas.
4. Respetar rate-limiting del sitio y robots.txt; añadir delays aleatorios entre peticiones.
5. No almacenar datos personales sensibles; tratar el contacto comercial como PII y pedir confirmación antes de persistir.
6. Al terminar, entregar resumen en markdown con: datos capturados, fricciones encontradas y sugerencias accionables.
