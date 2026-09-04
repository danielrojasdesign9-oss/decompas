# 🔄 Elementos que se Repiten — Plantillas Reutilizables

## Filosofía: 80% Template + 20% Personalización

El objetivo es que cada proyecto tome **2-4 horas** de configuración en vez de 2-3 semanas de desarrollo.

---

## ELEMENTOS QUE SE REPITEN EN TODOS LOS NEGOCIOS

### 1. MENSAJE DE BIENVENIDA (100% template)

```
┌─────────────────────────────────────────────┐
│ 🏢 [NOMBRE_DEL_NEGOCIO]                     │
│                                             │
│ ¡Bienvenido/a a [NOMBRE]!                     │
│                                             │
│ ¿En qué te puedo ayudar hoy?                │
│                                             │
│ 📋 Catálogo    ⏰ Horarios    📅 Reservar     │
│ 🛒 Pedir      📍 Ubicación   💬 Contacto     │
│                                             │
│ Escribe "hola" para empezar                 │
└─────────────────────────────────────────────┘
```

**Template variables:** `NOMBRE`, `emoji_icono`, `horas_atención`

---

### 2. HORARIOS (95% template)

```
┌─────────────────────────────────────────────┐
│ ⏰ Horario de Atención                       │
│                                             │
│ 📅 Lunes a Viernes: [H]:[MM] - [H]:[MM]    │
│ 📅 Sábado: [H]:[MM] - [H]:[MM]             │
│ 📅 Domingo: [CERRADO / HORARIO]             │
│                                             │
│ 📍 [CIUDAD], [DEPARTAMENTO]                 │
│ 📞 [TELÉFONO]                               │
│ 📱 [WHATSAPP]                               │
└─────────────────────────────────────────────┘
```

**Template variables:** `HORA_INICIO`, `HORA_FIN`, `CIUDAD`, `TELÉFONO`

---

### 3. CATÁLOGO DE PRODUCTOS/SERVICIOS (85% template)

```
┌─────────────────────────────────────────────┐
│ 🛒 Nuestros [PRODUCTOS/SERVICIOS]            │
│                                             │
│ 📂 Categoría 1:                              │
│    • [Item 1] - $X.XXX                     │
│    • [Item 2] - $X.XXX                     │
│    • [Item 3] - $X.XXX                     │
│                                             │
│ 📂 Categoría 2:                              │
│    • [Item 4] - $X.XXX                     │
│    • [Item 5] - $X.XXX                     │
│                                             │
│ 💬 Escribe el [NÚMERO] del producto para     │
│    pedirlo                                   │
└─────────────────────────────────────────────┘
```

**Template variables:** `CATEGORÍAS`, `ITEMS`, `PRECIOS`, `NÚMERO`

---

### 4. FLUJO DE RESERVA/AGENDAMIENTO (90% template)

```
┌─────────────────────────────────────────────┐
│ 📅 Reserva tu cita                          │
│                                             │
│ Paso 1: ¿Qué servicio necesitas?           │
│    [Opción 1] / [Opción 2] / [Opción 3]    │
│                                             │
│ Paso 2: ¿Cuándo prefieres?                 │
│    📅 [Fecha] ⏰ [Hora]                    │
│                                             │
│ Paso 3: ¿Nombre y contacto?                │
│    Nombre: [input]                         │
│    Teléfono: [input]                       │
│                                             │
│ ✅ Reserva confirmada para [Fecha] [Hora]  │
│    Con [Servicio]                           │
│    En [Nombre del negocio]                  │
└─────────────────────────────────────────────┘
```

**Template variables:** `SERVICIOS`, `NOMBRE_NEGOCIO`

---

### 5. FLUJO DE PEDIDO (90% template)

```
┌─────────────────────────────────────────────┐
│ 🛒 Tu pedido                                │
│                                             │
│ 📝 Paso 1: ¿Qué quieres pedir?             │
│    [Lista de items]                         │
│                                             │
│ 📝 Paso 2: ¿Cantidad?                      │
│    [Input]                                  │
│                                             │
│ 📝 Paso 3: ¿Dirección de entrega?          │
│    [Input]                                  │
│                                             │
│ 💳 Paso 4: Pago                            │
│    [Método de pago]                         │
│                                             │
│ ✅ Pedido recibido! Total: $X.XXX           │
│    Llegará en [X] minutos                  │
└─────────────────────────────────────────────┘
```

**Template variables:** `ITEMS`, `TIEMPO_ENTREGA`, `MÉTODO_PAGO`

---

### 6. FAQ / PREGUNTAS FRECUENTES (80% template)

```
┌─────────────────────────────────────────────┐
│ ❓ Preguntas Frecuentes                      │
│                                             │
│ Q: ¿Cuánto demora la entrega?               │
│ A: [TIEMPO] según tu ubicación              │
│                                             │
│ Q: ¿Aceptan pagos en efectivo?              │
│ A: Sí, [MÉTODO] y también [OTRO]           │
│                                             │
│ Q: ¿Qué pasa si algo llega mal?            │
│ A: [POLÍTICA]                               │
│                                             │
│ Q: ¿Cómo hago una reserva?                  │
│ A: Escribe "reservar" arriba 👆             │
│                                             │
│ ¿Tienes otra pregunta? Escribe "contacto"  │
└─────────────────────────────────────────────┘
```

**Template variables:** `TIEMPOS`, `MÉTODOS`, `POLÍTICAS`

---

### 7. MENSAJE DE SEGUIMIENTO (75% template)

```
┌─────────────────────────────────────────────┐
│ 💬 ¿Cómo quedó tu pedido/reserva?           │
│                                             │
│ ¿Todo bien con tu [pedido/reserva]?          │
│                                             │
│ ⭐ ¿Cómo fue tu experiencia?                │
│    😍 Excelente / 😊 Buena / 😐 Regular     │
│                                             │
│ 📩 ¿Necesitas algo más?                      │
│    Escribe "sí" para ayuda                  │
└─────────────────────────────────────────────┘
```

**Template variables:** `TIPO`, `TIEMPO`

---

### 8. MENSAJE DE URGENCIA / HUMANO (70% template)

```
┌─────────────────────────────────────────────┐
│ ⚠️ ¿Necesitas hablar con una persona?       │
│                                             │
│ Escribe "persona" para contactar a          │
│ [NOMBRE] al [TELÉFONO]                      │
│                                             │
│ Horario de atención humana: [HORAS]         │
└─────────────────────────────────────────────┘
```

**Template variables:** `NOMBRE`, `TELÉFONO`, `HORAS`

---

### 9. NOTIFICACIÓN DE PEDIDO (65% template)

```
┌─────────────────────────────────────────────┐
│ 🔔 [NOMBRE] - Nuevo Pedido                  │
│                                             │
│ 📦 Pedido #XXXX                             │
│ 🛒 [Items]                                  │
│ 💰 Total: $X.XXX                           │
│ 📍 Dirección: [Dirección]                   │
│ 💳 Método: [Método]                         │
│                                             │
│ Estado: [PENDIENTE / PROCESANDO / ENVIADO]  │
└─────────────────────────────────────────────┘
```

**Template variables:** `NOMBRE_NEGOCIO`, `ITEMS`

---

## CONFIGURACIÓN POR NEGOCIO (Solo 20% del trabajo)

Para cada negocio, solo necesitas llenar estos datos:

```json
{
  "negocio": {
    "nombre": "La Burguesa",
    "tipo": "restaurante",
    "ciudad": "Cali",
    "direccion": "Calle 12 #3-45",
    "telefono": "+57 317 444 6641",
    "whatsapp": "+57 311 123 4567",
    "horario": {
      "lunes_viernes": "08:00-22:00",
      "sabado": "10:00-20:00",
      "domingo": "CERRADO"
    },
    "logo": "la_burguesa.png"
  },
  "productos": [
    { "categoria": "Hambúrgueres", "items": [{"nombre": "Clásico", "precio": 12000}, {"nombre": "Doble", "precio": 18000}] },
    { "categoria": "Bebidas", "items": [{"nombre": "Refresco", "precio": 3500}, {"nombre": "Jugo", "precio": 4500}] }
  ],
  "flujos": ["reserva", "pedido", "cita"],
  "config": {
    "tiempo_entrega": "30 minutos",
    "metodos_pago": ["Efectivo", "Transferencia", "Nequi"],
    "politica_cambios": "Se aceptan cambios dentro de 30 min"
  }
}
```

**Eso es TODO lo que necesitas por negocio.** El template maneja el resto.

---

## TYPES DE NEGOCIOS Y SUS TEMPLATES

| Tipo de Negocio | Flujos Principales | Productos | Personalización |
|---|---|---|---|
| **Restaurante** | Pedido + Reserva | Menú | Horario, platos, entrega |
| **Clínica** | Cita + Urgencia | Servicios | Especialidades, precios |
| **Tienda** | Pedido + Catálogo | Inventario | Productos, precios, envío |
| **Servicio Profesional** | Cita + Consulta | Servicios | Tarifas, disponibilidad |
| **Bar/Café** | Pedido + Reserva | Bebidas + Comida | Horario, promociones |
| **Salón de Belleza** | Cita | Servicios | Servicios, precios, duración |

Cada tipo usa el MISMO template base, solo cambia el JSON de configuración.

---

## FLUJO DE TRABAJO CON TEMPLATES

```
┌─────────────────────────────────────────────────┐
│ 1. Auditar (gratis)                             │
│    → Entender qué necesita el negocio          │
│                                                   │
│ 2. Seleccionar template base                    │
│    → Restaurante / Clínica / Tienda / etc.     │
│                                                   │
│ 3. Llenar JSON de configuración                 │
│    → 20 minutos                                 │
│                                                   │
│ 4. Configurar flujos                            │
│    → 30 minutos                                 │
│                                                   │
│ 5. Probar                                       │
│    → 30 minutos                                 │
│                                                   │
│ 6. Entregar                                     │
│    → 10 minutos                                 │
│                                                   │
│ TOTAL: ~2 horas                                 │
│ VS: 2-3 semanas sin templates                  │
└─────────────────────────────────────────────────┘
```

---

## 📊 AHORRO DE TIEMPO

| Escenario | Sin Templates | Con Templates |
|---|---|---|
| 1 negocio | 15-20 horas | 2 horas |
| 3 negocios | 45-60 horas | 6 horas |
| 5 negocios | 75-100 horas | 10 horas |
| 10 negocios | 150-200 horas | 20 horas |

**Con templates puedes servir 10 clientes en 20 horas (2.5 días).**
**Sin templates, solo 1-2 clientes por mes.**
