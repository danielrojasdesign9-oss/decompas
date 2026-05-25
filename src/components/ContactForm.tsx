import React, { useState, useEffect } from "react";
import { Check, Send, Sparkles, X, Database } from "lucide-react";
import { LeadFormData } from "../types";

export default function ContactForm() {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState<LeadFormData>({
    name: "",
    phone: "",
    email: "",
    businessType: "generico",
    notes: ""
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [savedLeads, setSavedLeads] = useState<any[]>([]);
  const [showAdmin, setShowAdmin] = useState(false);

  const fetchLeads = async () => {
    try {
      const res = await fetch("/api/leads");
      if (res.ok) {
        const data = await res.json();
        setSavedLeads(data.leads || []);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.phone.trim()) {
      setErrorMsg("Por favor, ingresa tu nombre y WhatsApp.");
      return;
    }

    setIsSubmitting(true);
    setErrorMsg("");

    try {
      const response = await fetch("/api/proposal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error();

      // Dispatch to the team WhatsApp link directly
      const waText = `Hola DECOMPAS, mi nombre es ${formData.name}. Me gustaría recibir una propuesta para automatizar mi negocio. Mi contacto es ${formData.phone}. Notas adicionales: ${formData.notes || "Ninguna"}`;
      const waUrl = `https://wa.me/573174446641?text=${encodeURIComponent(waText)}`;
      window.open(waUrl, "_blank");

      setSubmitSuccess(true);
      setFormData({
        name: "",
        phone: "",
        email: "",
        businessType: "generico",
        notes: ""
      });
      fetchLeads();
    } catch (err) {
      setErrorMsg("Error al guardar la solicitud. Intenta de nuevo.");
    } finally {
      setIsSubmitting(false);
    }
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
          onClick={() => setIsOpen(true)}
          className="bg-secondary text-on-secondary font-display text-[11px] uppercase tracking-widest px-10 py-5 rounded-full hover:scale-105 transition-transform duration-200 relative z-10 shadow-[0_0_30px_rgba(230,255,128,0.2)] font-bold cursor-pointer"
        >
          Contactar por WhatsApp
        </button>

        {/* Collapsible database simulation trigger inside the main screen */}
        <div className="mt-8 relative z-10">
          <button
            onClick={() => {
              setShowAdmin(!showAdmin);
              fetchLeads();
            }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-black/30 hover:bg-black/50 border border-secondary/10 text-on-surface hover:text-secondary rounded text-[10px] font-mono transition-colors cursor-pointer uppercase tracking-wider"
          >
            <Database className="w-3.5 h-3.5 text-secondary" />
            <span>Ver Base de Datos de Leads ({savedLeads.length})</span>
          </button>
        </div>

        {/* Collapsible local leads list view */}
        {showAdmin && (
          <div className="mt-8 relative z-10 bg-black/20 border border-secondary/10 rounded-xl p-6 text-left max-w-2xl mx-auto animate-fadeIn">
            <h4 className="font-display text-xs text-secondary font-bold uppercase tracking-wider mb-4">Leads Simulados Guardados</h4>
            {savedLeads.length === 0 ? (
              <p className="text-xs text-on-surface/60 font-light">Aún no hay leads registrados. Haz clic en "Contactar por WhatsApp" para simular y agendar.</p>
            ) : (
              <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
                {savedLeads.map((lead, idx) => (
                  <div key={idx} className="bg-background/80 p-4 rounded-lg border border-on-surface/5 text-xs">
                    <div className="flex justify-between items-center font-bold text-on-surface mb-1">
                      <span>{lead.name}</span>
                      <span className="text-secondary tracking-widest uppercase text-[9px] px-2 py-0.5 border border-secondary/20 rounded bg-secondary/5 font-mono">{lead.businessType}</span>
                    </div>
                    <div className="text-on-surface/60 font-light flex gap-4">
                      <span>📞 {lead.phone}</span>
                      <span>📧 {lead.email || "No especificado"}</span>
                    </div>
                    {lead.notes && (
                      <p className="border-l border-secondary/30 pl-2 mt-2 font-mono text-on-surface/70 text-[10px] italic">
                        "{lead.notes}"
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* High Fidelity Lead-capture Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-md">
          <div className="glass-panel w-full max-w-lg rounded-2xl p-6 sm:p-10 relative overflow-hidden shadow-2xl animate-scaleUp text-left">
            <button 
              onClick={() => {
                setIsOpen(false);
                setSubmitSuccess(false);
              }}
              className="absolute top-4 right-4 text-on-surface/60 hover:text-secondary cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="absolute top-0 left-0 right-0 h-1.5 bg-secondary" />

            {submitSuccess ? (
              <div className="space-y-6 pt-4 text-center">
                <div className="w-16 h-16 rounded-full bg-secondary/20 border-2 border-secondary flex items-center justify-center mx-auto">
                  <Check className="w-8 h-8 text-secondary" />
                </div>
                
                <h3 className="font-display text-2xl font-bold text-secondary">
                  ¡Suscripción Simulada con Éxito!
                </h3>
                
                <p className="font-sans text-sm text-on-surface/80 opacity-90 leading-relaxed font-light">
                  Gracias por tu mensaje. Tu solicitud de cotización se ha registrado correctamente y te hemos abierto el canal de WhatsApp (+57 317 444 6641) para coordinar de inmediato con nuestro equipo.
                </p>

                <button
                  onClick={() => {
                    setIsOpen(false);
                    setSubmitSuccess(false);
                  }}
                  className="w-full py-4 bg-secondary text-on-secondary font-display text-xs uppercase tracking-widest rounded-full font-bold cursor-pointer hover:scale-102 transition-transform"
                >
                  Regresar a la Landing
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5 pt-2">
                <div>
                  <h3 className="font-display text-xl font-bold text-secondary tracking-tight">
                    Mandar Mensaje de Contacto
                  </h3>
                  <p className="font-sans text-xs text-on-surface/60 mt-1 font-light">
                    Rellena este simulador para ver cómo capturamos tus requerimientos en base de datos.
                  </p>
                </div>

                {errorMsg && (
                  <div className="p-3 bg-red-950/30 border border-red-500/20 text-red-200 rounded text-xs">
                    {errorMsg}
                  </div>
                )}

                <div className="space-y-1">
                  <label className="text-[10px] font-mono text-on-surface/80 uppercase">Nombre Completo *</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="Ej. Daniel Rojas"
                    className="w-full bg-black/20 border border-on-surface/10 focus:border-secondary rounded-lg px-3 py-2.5 text-xs text-on-surface focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-mono text-on-surface/80 uppercase">WhatsApp / Celular *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    placeholder="Ej. +57 301 234 5678"
                    className="w-full bg-black/20 border border-on-surface/10 focus:border-secondary rounded-lg px-3 py-2.5 text-xs text-on-surface focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-mono text-on-surface/80 uppercase">Correo Electrónico (Opcional)</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Ej. daniel@empresa.com"
                    className="w-full bg-black/20 border border-on-surface/10 focus:border-secondary rounded-lg px-3 py-2.5 text-xs text-on-surface focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-mono text-on-surface/80 uppercase">Procesos a Automatizar</label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    rows={3}
                    placeholder="Ej. Saturación de chats, menús interactivos, etc."
                    className="w-full bg-black/20 border border-on-surface/10 focus:border-secondary rounded-lg px-3 py-2.5 text-xs text-on-surface focus:outline-none resize-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-4 bg-secondary text-on-secondary font-display text-xs uppercase tracking-widest rounded-full font-bold flex items-center justify-center gap-2 cursor-pointer border-none"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{isSubmitting ? "GUARDANDO..." : "Mandar por WhatsApp"}</span>
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
