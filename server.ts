import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = 3000;

app.use(express.json());

// Simple in-memory storage for leads captured during the session
interface Lead {
  id: string;
  name: string;
  phone: string;
  email?: string;
  businessType: string;
  notes?: string;
  roiEstimate?: {
    monthlySavings: number;
    extraSales: number;
    hoursRegained: number;
  };
  createdAt: string;
}

const leads: Lead[] = [];

// Initialize Gemini safely
let ai: GoogleGenAI | null = null;
const API_KEY = process.env.GEMINI_API_KEY;

if (API_KEY && API_KEY !== "MY_GEMINI_API_KEY" && API_KEY.trim() !== "") {
  try {
    ai = new GoogleGenAI({
      apiKey: API_KEY,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
    console.log("Gemini API initialized successfully.");
  } catch (error) {
    console.error("Failed to initialize Gemini API:", error);
  }
} else {
  console.log("GEMINI_API_KEY not found in environment, running simulation engine.");
}

// API Routes

// Helper template for simulation when API key is missing
const getDeterministicSimulation = (message: string, businessType: string) => {
  const lowercaseInput = message.toLowerCase();
  
  if (businessType === "restaurant") {
    if (lowercaseInput.includes("menú") || lowercaseInput.includes("carta") || lowercaseInput.includes("comer") || lowercaseInput.includes("plato")) {
      return {
        text: "¡Claro! 🍽️ Aquí tienes nuestro menú digital interactivo QR: *https://ejemplo.com/menu-decompas*. \n\n¿Te gustaría que te reserve una mesa para hoy o prefieres pedir para llevar?",
        suggestedReplies: ["Reservar mesa 📅", "Pedir delivery 🛵", "Ver especial del día 🌟"]
      };
    }
    if (lowercaseInput.includes("reserv") || lowercaseInput.includes("mesa") || lowercaseInput.includes("reserva")) {
      return {
        text: "¡Perfecto! 📅 Reservar con nuestro chatbot es facilísimo. \n\nPor favor, indícame: \n1 - Tu Nombre \n2 - Número de personas \n3 - Hora deseada (servimos de 12:00 a 23:00).\n\n¡La reserva se confirmará inmediatamente en nuestro sistema!",
        suggestedReplies: ["Hoy 8:00 PM 🍽️", "Mañana 2:00 PM 🌞", "Volver al inicio 🏠"]
      };
    }
    return {
      text: "🍽️ ¡Hola! Bienvenido a *La Selva Tech*, un restaurante simulado automatizado por **Decompas**. \n\nPuedo ayudarte a:\n• Ver la Carta / Menú interactivo QR\n• Hacer una Reserva instantánea en 15 segundos \n• Consultar Horarios y Ubicación\n\n¿De qué tienes antojo hoy?",
      suggestedReplies: ["Ver Menú Digital 📜", "Reservar una mesa 📅", "Preguntas Frecuentes ❓"]
    };
  }

  if (businessType === "ecommerce") {
    if (lowercaseInput.includes("comprar") || lowercaseInput.includes("catalogo") || lowercaseInput.includes("producto") || lowercaseInput.includes("precio")) {
      return {
        text: "🛍️ Te presento nuestro *Catálogo Inteligente de Moda*: \n\n• 👟 Zapatillas Cyber-Jungle - $45.000\n• 👕 Camiseta Minimal Tech - $18.000\n• 🎒 Mochila Inteligente Impermeable - $35.000\n\n¿Quieres que agregue alguno al carrito o prefieres ver la vitrina web completa?",
        suggestedReplies: ["Comprar Zapatillas 👟", "Comprar Camiseta 👕", "Ver Vitrina Web 🌐"]
      };
    }
    if (lowercaseInput.includes("envio") || lowercaseInput.includes("llega") || lowercaseInput.includes("despacho")) {
      return {
        text: "🚚 ¡Despachamos a todo el país! El tiempo estimado de entrega es de 1 a 3 días hábiles. Al finalizar la compra por aquí, recibirás un enlace de seguimiento de WhatsApp automático.\n\n¿Te gustaría realizar tu pedido ahora?",
        suggestedReplies: ["Sí, comprar ahora 🛒", "Ver catálogo de nuevo 🎒", "Hablar con soporte 👤"]
      };
    }
    return {
      text: "🛍️ ¡Hola! Soy el asistente virtual de *Moda Jungle*, automatizado por **Decompas**.\n\nEstoy aquí para guiarte en tu compra sin fricciones. \n¿Qué te gustaría hacer hoy?",
      suggestedReplies: ["Ver catálogo interactivo 🛒", "Consultar estado de envío 🚚", "Garantías y Cambios 🛡️"]
    };
  }

  if (businessType === "estetica") {
    if (lowercaseInput.includes("cita") || lowercaseInput.includes("agenda") || lowercaseInput.includes("turno") || lowercaseInput.includes("agendar")) {
      return {
        text: "💆🏼‍♀️ ¡Perfecto! Vamos a elegir tu turno para tu tratamiento de bienestar. \n\nNuestras horas disponibles para hoy son: \n• 15:30 \n• 17:00 \n• 18:30 \n\n¿Cuál prefieres agendar?",
        suggestedReplies: ["Hoy 15:30 ⏰", "Hoy 17:00 🌸", "Ver días de la otra semana 🗓️"]
      };
    }
    if (lowercaseInput.includes("precio") || lowercaseInput.includes("tratamiento") || lowercaseInput.includes("servicio")) {
      return {
        text: "✨ Aquí tienes nuestros mejores tratamientos estéticos:\n\n1️⃣ Limpieza Facial Profunda - $25.000\n2️⃣ Masaje Descontracturante Natural - $35.000\n3️⃣ Peeling de Ácido Hialurónico - $42.000\n\nTodos se agendan en un instante. ¿Cuál te llama más la atención?",
        suggestedReplies: ["Agendar Limpieza Facial 💆🏼‍♀️", "Agendar Masaje 🌸", "Volver al inicio 🏠"]
      };
    }
    return {
      text: "✨ ¡Hola! Bienvenido a *Vitality Spa*, una clinica estética automatizada por **Decompas**.\n\nPuedo ayudarte con:\n• Agendar una cita de forma automática\n• Ver la lista de tratamientos y precios\n• Ubicación y Horarios de atención\n\n¿Cómo podemos consentirte hoy?",
      suggestedReplies: ["Ver Tratamientos ✨", "Ver Horas disponibles 📅", "Ubicación 📍"]
    };
  }

  // Fallback default business type "general"
  if (lowercaseInput.includes("precio") || lowercaseInput.includes("cuanto") || lowercaseInput.includes("cuesta") || lowercaseInput.includes("servicios")) {
    return {
      text: "💼 En **Decompas** creamos soluciones a la medida:\n\n• **Vitrinas Web:** Desde $450.000 (diseñadas para convertir)\n• **Automatizaciones WhatsApp con IA:** Desde $600.000 un pago único y mantenimiento mínimo\n• **Portafolios QR Inteligentes:** Desde $300.000\n\n¡La inversión se recupera en las primeras semanas gracias a las ventas que dejas de perder!",
      suggestedReplies: ["Me interesan Automatizaciones IA 🤖", "Me interesan Vitrinas Web 🌐", "Pedir Propuesta Personalizada 📑"]
    };
  }
  return {
    text: "🤖 ¡Hola! Soy el Agente de Demostración de **Decompas**.\n\nEstoy mostrándote en tiempo real cómo tu negocio puede responder a cualquier cliente en **menos de 2 segundos**.\n\n¿Quieres simular un caso o revisar cómo digitalizar tu catálogo?",
    suggestedReplies: ["Simular un restaurante 🍽️", "Simular E-Commerce 🛍️", "Simular Spa Estética ✨"]
  };
};

// Endpoint to chat with the Gemini AI bot
app.post("/api/gemini/chatbot", async (req, res) => {
  const { message, businessType, chatHistory } = req.body;

  if (!message) {
    return res.status(400).json({ error: "El mensaje es obligatorio" });
  }

  const selectedBusiness = businessType || "general";

  // If Gemini API is configured, use it!
  if (ai) {
    try {
      const typePrompts: Record<string, string> = {
        restaurant: "un chatbot de atención automatizado en WhatsApp de un restaurante llamado 'La Selva Tech' (carnes, comida fresca, ambiente acogedor). Debe ofrecer ver el menú digital QR, tomar reservas recopilando nombre, número de comensales y hora, y responder dudas sobre horarios o ubicación. Mantener tono amigable, persuasivo, ágil y con bastantes emojis. Usa formato amigable con viñetas elegantes.",
        ecommerce: "un chatbot de WhatsApp para una tienda de e-commerce de moda urbana llamada 'Moda Jungle' que automatiza ventas, muestra catálogos interactivos, responde preguntas de envíos (1 a 3 días hábiles) y gestiona pedidos guiando al cliente con fluidez, emojis y tono dinámico.",
        estetica: "un servicio de chatbot de WhatsApp para un centro estético y esteticista premium llamado 'Vitality Spa'. Ofrece tratamientos estéticos (limpieza facial $25mil, masajes $35mil), agenda citas preguntando disponibilidad (propón horas como 15:30 o 17:00), y transmite relajación y profesionalismo con tono cálido, emojis y elegancia.",
        general: "un chatbot de WhatsApp corporativo de la agencia 'DECOMPAS' que digitaliza y automatiza negocios eliminando WhatsApps saturados y PDFs pesados. Vende servicios de Vitrinas Web, Menús QR interactivos, Portafolios Inteligentes y Automatizaciones de Flujos con Inteligencia Artificial."
      };

      const systemInstruction = `Eres un chatbot simulado de servicio al cliente de WhatsApp creado por la agencia de automatización 'DECOMPAS' (https://decompas.com).
Tu contexto de simulación actual es: ${typePrompts[selectedBusiness] || typePrompts.general}.

Reglas estrictas de respuesta:
1. Responde de forma concisa, simulando un mensaje real de WhatsApp (usa emojis, formato de texto en negrita con asteriscos como *texto* para resaltar, y saltos de línea amigables).
2. Debes sugerir siempre entre 2 y 3 opciones cortas como botones de respuesta rápida al final de tu mensaje en un campo JSON separado (por ejemplo, "Ver catálogo", "Hablar con asesor").
3. Mantén el idioma en español neutral y profesional pero con alto sentido de conversión.
4. Tu respuesta final debe estar formateada en JSON estructurado para que el frontend la procese limpiamente. El JSON debe tener exactamente esta estructura:
{
  "text": "La respuesta textual que leerá el usuario imitando a WhatsApp...",
  "suggestedReplies": ["Respuesta sugerida 1", "Respuesta sugerida 2", "Respuesta sugerida 3"]
}

No agregues texto fuera de este objeto JSON. No uses bloques de markdown como \`\`\`json ... \`\`\`. Devuelve el objeto JSON directamente en formato de texto plano que pueda ser parseado.`;

      const formattedHistory = (chatHistory || []).map((msg: any) => ({
        role: msg.role === "user" ? "user" : "model",
        parts: [{ text: msg.text }]
      }));

      // Append current user message
      formattedHistory.push({
        role: "user",
        parts: [{ text: message }]
      });

      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: JSON.stringify(formattedHistory),
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          temperature: 0.7
        }
      });

      const textResponse = response.text || "{}";
      const parsed = JSON.parse(textResponse);
      return res.json(parsed);

    } catch (error) {
      console.error("Gemini API Error, falling back to simulation engine:", error);
      // Fallback if API call fails
      const fallback = getDeterministicSimulation(message, selectedBusiness);
      return res.json(fallback);
    }
  } else {
    // Return deterministic highly realistic simulated response in real-time
    const fallback = getDeterministicSimulation(message, selectedBusiness);
    return res.json(fallback);
  }
});

// Capture leads / contact requests
app.post("/api/proposal", (req, res) => {
  const { name, phone, email, businessType, notes, roiEstimate } = req.body;

  if (!name || !phone) {
    return res.status(400).json({ error: "Nombre y teléfono son obligatorios" });
  }

  const newLead: Lead = {
    id: "lead_" + Math.random().toString(36).substr(2, 9),
    name,
    phone,
    email,
    businessType: businessType || "No especificado",
    notes,
    roiEstimate,
    createdAt: new Date().toISOString()
  };

  leads.push(newLead);
  return res.json({ success: true, lead: newLead });
});

// Fetch all captured leads (for the Admin simulator panel in frontend)
app.get("/api/leads", (req, res) => {
  return res.json({ success: true, leads });
});

// Configure dev environment vs production static build
const startServer = async () => {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Decompas Fullstack Server running on http://localhost:${PORT}`);
  });
};

startServer().catch((err) => {
  console.error("Failed to start server:", err);
});
