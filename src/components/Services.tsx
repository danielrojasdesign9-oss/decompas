import { motion } from "motion/react";

export default function Services() {
  const servicesData = [
    {
      id: "web",
      tag: "Presencia digital",
      title: "Vitrinas Web",
      desc: "Sitios de alto impacto visual y conversión diseñados para capturar leads y transmitir autoridad.",
      icon: "web",
      isLarge: true,
      waText: "Hola DECOMPAS, quiero más información sobre el servicio de Vitrinas Web.",
      mailSubject: "Información sobre Vitrinas Web"
    },
    {
      id: "menu",
      tag: "Hospitalidad",
      title: "Menús Digitales QR",
      desc: "Experiencias interactivas para el sector gastronómico.",
      icon: "qr_code_scanner",
      isLarge: false,
      waText: "Hola DECOMPAS, quiero más información sobre el servicio de Menús Digitales QR.",
      mailSubject: "Información sobre Menús Digitales QR"
    },
    {
      id: "portfolio",
      tag: "Datos",
      title: "Portafolios Inteligentes",
      desc: "Catálogos con bases de datos editables y escalables.",
      icon: "database",
      isLarge: false,
      waText: "Hola DECOMPAS, quiero más información sobre el servicio de Portafolios Inteligentes.",
      mailSubject: "Información sobre Portafolios Inteligentes"
    },
    {
      id: "whatsapp",
      tag: "Eficiencia",
      title: "Automatizaciones con IA",
      desc: "Flujos de trabajo que operan de manera autónoma, reduciendo carga manual y errores operativos.",
      icon: "smart_toy",
      isLarge: true,
      waText: "Hola DECOMPAS, quiero más información sobre el servicio de Automatizaciones con IA.",
      mailSubject: "Información sobre Automatizaciones con IA"
    }
  ];

  const whatsappNumber = "573174446641";
  const teamEmail = "decompasdesing@gmail.com";

  return (
    <section className="px-6 md:px-20 max-w-7xl mx-auto py-16 md:py-24" id="servicios">
      <h2 className="font-display text-3xl md:text-[36px] font-bold text-secondary mb-12 tracking-tight">
        Nuestros Servicios
      </h2>
      
      {/* Bento Grid layout matching Stitch exactly */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 auto-rows-min">
        {servicesData.map((service, index) => {
          const waUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(service.waText)}`;
          const mailUrl = `mailto:${teamEmail}?subject=${encodeURIComponent(service.mailSubject)}`;

          return (
            <motion.div 
              key={service.id}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className={`${
                service.isLarge ? "md:col-span-8" : "md:col-span-4"
              } glass-panel p-8 rounded-2xl flex flex-col justify-between group overflow-hidden relative min-h-[300px] hover:border-secondary/30 transition-all duration-300`}
            >
              {/* Subtle hover background overlay */}
              <div className="absolute inset-0 bg-secondary/[0.01] group-hover:bg-secondary/[0.02] transition-colors duration-300" />
              
              <div className="relative z-10 text-left">
                <div className="inline-block px-3 py-1 border border-secondary/30 rounded-full font-display text-[10px] text-secondary mb-6 uppercase tracking-widest font-semibold">
                  {service.tag}
                </div>
                <h3 className="font-display text-xl md:text-[24px] font-bold text-on-surface mb-4">
                  {service.title}
                </h3>
                <p className="font-sans text-sm md:text-[18px] text-on-surface opacity-90 max-w-md font-light leading-relaxed">
                  {service.desc}
                </p>
              </div>
              
              <div className="relative z-10 mt-8 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                {/* Dual Call to Action contact options tailored to the service */}
                <div className="flex flex-wrap items-center gap-3">
                  <a 
                    href={mailUrl}
                    className="inline-flex items-center gap-1.5 bg-secondary text-on-secondary font-display text-[10px] uppercase tracking-wider px-4 py-2.5 rounded-full font-bold hover:scale-105 transition-transform duration-200"
                  >
                    <span>Colaboremos juntos</span>
                  </a>
                </div>

                <span 
                  className="material-symbols-outlined text-secondary text-5xl opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-300 hidden sm:block" 
                  style={{ fontVariationSettings: "'wght' 200" }}
                >
                  {service.icon}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
