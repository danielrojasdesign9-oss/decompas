---
name: frontend-design-system
description: Use when designing or building frontend UI/UX: choosing a design preset, typography pairs, color palettes, or setting up Tailwind CSS / Radix UI / CSS Modules. Prevents generic AI aesthetics and applies professional design systems. Trigger on keywords like "diseño", "UI", "UX", "frontend", "landing", "paleta de colores", "tipografía", "estilo visual", "neobrutalism".
---

# Frontend Design System & Typography Engine

Motor de diseño UI/UX con presets estilísticos y pares tipográficos profesionales para eliminar la estética genérica de IA.

## Estilos disponibles

- **Editorial Premium** — tipografía serif de alta contraste, whitespace generoso, elegancia.
- **Neobrutalism** — bordes gruesos, sombras duras, colores saturados, energía.
- **Swiss Minimalist** — grid estricto, tipografía grotesca, jerarquía limpia.
- **Warm Organic** — tonos tierra, formas suaves, tono cercano y humano.
- **Dark Cyber** — fondos oscuros, neones, glassmorphism, tecnología.
- **B2B Modern Enterprise** — sobrio, confiable, azul/gris, pensado para convertir clientes corporativos.

## Capacidades

- Selección inteligente de paletas cromáticas basadas en la identidad de marca (regla 60-30-10).
- Configuración de componentes en Tailwind CSS, Radix UI o CSS Modules.
- Optimización de microinteracciones, jerarquía visual y espaciado (8pt grid system).
- Pares tipográficos profesionales (display + body) con tamaños fluidos.

## Reglas de ejecución

1. **Prohibido estilos genéricos por defecto:** nunca usar Tailwind predeterminado sin personalizar; el preset debe elegirse y adaptarse a la marca del cliente.
2. **Contraste WCAG AAA:** aplicar contraste de al menos 7:1 para texto comercial legible; verificar antes de dar por terminado.
3. **Jerarquía y grid:** usar el sistema de espaciado de 8pt; definir escala tipográfica (display, h1-h6, body, caption) antes de escribir componentes.
4. **Regla 60-30-10:** 60% color dominante (fondo/superficies), 30% color secundario, 10% acento para CTA y estados.
5. **Decisiones con justificación:** al elegir un preset, explicar en una línea por qué se adapta al sector de la Pyme (ej. clínica = Warm Organic + azul confiable).
6. **Entrega:** entregar tokens (colores, tipografías, radios, sombras) en formato para Tailwind (`tailwind.config`) o variables CSS.
