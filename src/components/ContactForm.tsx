import React from "react";
import { Send } from "lucide-react";

export default function ContactForm() {
  const handleWhatsAppClick = () => {
    const waText = `Hola DECOMPAS, me gustaría recibir una propuesta para automatizar mi negocio.`;
    const waUrl = `https://wa.me/573174446641?text=${encodeURIComponent(waText)}`;
    window.open(waUrl, "_blank");
  };

  return (
    <section className="px-6 md:px-20 max-w-7xl mx-auto py-16 md:py-24" id="cta-section">
      <div className="glass-panel border border-secondary/20 rounded-3xl p-12 md:p-24 text-center relative overflow-hidden">
        {/* Ambient glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-secondary/10 rounded-full blur-[100px] pointer-events-none" />

        <h2 className="font-display text-[32px] md:text-[56px] leading-[40px] md:leading-[64px] font-bold text-secondary mb-8 relative z-10 tracking-tight">
          ¿Listo para automatizar tu negocio?
        </h2>

        <button
          onClick={handleWhatsAppClick}
          className="bg-secondary text-on-secondary font-display text-[11px] uppercase tracking-widest px-10 py-5 rounded-full hover:scale-105 transition-transform duration-200 relative z-10 shadow-[0_0_30px_rgba(230,255,128,0.2)] font-bold cursor-pointer flex items-center gap-2 mx-auto"
        >
          <Send className="w-3.5 h-3.5" />
          Contactar por WhatsApp
        </button>
      </div>
    </section>
  );
}
