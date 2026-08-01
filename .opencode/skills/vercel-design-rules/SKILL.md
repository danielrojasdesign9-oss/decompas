---
name: vercel-design-rules
description: Use when auditing a web app or landing for quality, performance, UX, accessibility, SEO, and production readiness before a deploy. Runs a quality checklist (Core Web Vitals, loading states, empty states, semantic HTML, OG tags), assigns a 0-100 score, and recommends fixes. Trigger on keywords like "auditoría", "audit", "calidad", "Core Web Vitals", "LCP", "deploy", "producción", "puntaje".
---

# Vercel UI/UX & Quality Rules Engine

Motor de auditoría con +100 reglas de calidad de software, diseño y rendimiento inspiradas en los estándares de Vercel.

## Checklist de reglas

### Performance
- Core Web Vitals en producción: LCP < 2.5s, CLS < 0.1, INP < 200ms.
- Imágenes optimizadas (Next.js Image / WebP / AVIF), lazy loading, dimensiones explícitas (sin layout shift).
- Fuentes con `font-display: swap` y subconjunto; evitar render blocking de CSS/JS innecesario.
- JS bundles bajo presupuesto; evitar hidratación pesada en client components.

### UX/UI
- Estados de carga visibles (skeletons, spinners) en toda operación asíncrona.
- Manejo de errores visible y recuperable (mensajes claros, botón reintentar), nunca fallos silenciosos.
- Estados vacíos (empty states) con guía de acción para el usuario.
- Feedback inmediato en cada interacción (hover, focus, submit, éxito/error).

### Accesibilidad & SEO
- HTML semántico (header, nav, main, section, footer; encabezados jerárquicos).
- ARIA labels y roles correctos; navegación por teclado funcional; foco visible.
- Contraste WCAG AA/AAA en todo texto interactivo.
- Open Graph tags, meta description, título único, alt texts dinámicos y descriptivos.

### Código
- Zero layout shifts (dimensiones reservadas para imágenes/media).
- Server vs. client components bien delimitados (menos JS enviado al cliente).
- Sin dependencias muertas, sin código comentado, sin consolas de debug en producción.

## Reglas de ejecución

1. **Checklist antes de deploy:** ejecutar el checklist automático completo antes de sugerir despliegues a producción.
2. **Puntaje 0-100:** asignar un puntaje de calidad global, desglosado por categorías (Performance, UX, A11y, SEO, Código).
3. **Soluciones específicas:** por cada fallo, indicar el archivo/línea (si es posible) y una solución accionable concreta, priorizada por impacto.
4. **Evidencia:** respaldar cada métrica con medición real (auditoría del navegador, Lighthouse, datos de campo) cuando esté disponible; si no, marcar como "por verificar".
5. **Entregable:** reporte en markdown con puntaje global, desglose por categoría, tabla de fallos y plan de remediación priorizado.
