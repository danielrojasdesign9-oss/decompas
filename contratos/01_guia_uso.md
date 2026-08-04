# Contratos y propuestas — Daniel Rojas (Consultor de IA y Diseño)

Flujo de venta recomendado y cuál documento usar en cada punto.

## Cuándo usar cada documento

| Punto del proceso            | Documento                          |
|------------------------------|------------------------------------|
| Después de la llamada de 15 min (dolores detectados) | `02_propuesta_servicios.md` |
| Cliente quiere un proyecto puntual (web, chatbot, automatización, identidad) | `03_contrato_proyecto.md` |
| Cliente quiere relación continua (mejora mensual + soporte + nuevas ideas) | `04_retainer_socio.md` |
| El cliente pide firmar confidencialidad antes de mostrar información sensible | `03_contrato_proyecto.md` (cláusula 10) o NDA propio |

## Regla rápida

- **Un solo trabajo, con alcance cerrado** → contrato de proyecto.
- **Relación mensual, "socio" que genera proyectos todo el año** → retainer.
- **Ambos**: arrancas con un proyecto y propones pasarlo a retainer al terminar
  (es el movimiento natural: "si el proyecto les funciona, continuamos con un
  plan mensual para que no vuelva a quedarse atrás").

## Antes de enviar cualquier contrato

1. Rellena todos los `{CORCHETES}`: nombres, NIT/RUT, valores en COP, fechas.
2. Precio de referencia (ajusta a tu mercado): llamada gratis, propuesta gratis,
   proyecto base `{5.000.000} COP`, retainer `{1.500.000} COP/mes`.
3. Nunca envíes un contrato sin haber hecho la llamada de dolores de 15 min.
4. Pagos siempre por adelantado parcial (50% proyecto / 100% primer mes de retainer).
5. Guarda una copia firmada en `out/ventas/` y registra el caso en el tracker:
   `python scripts/track.py update <id> --status socio --note "Firmó retainer {X}"`

## Documentos que aún faltan cuando el negocio crezca
- Factura electrónica (COP): se emite por el proveedor tecnológico, no aquí.
- Contrato de distribución/afiliado si el retainer se vuelve una "agencia".
- Minuta de constitución si creas empresa (ahora opera como persona natural).
