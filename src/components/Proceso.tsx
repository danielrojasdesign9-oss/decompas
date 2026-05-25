import { motion } from "motion/react";

export default function Proceso() {
  const steps = [
    {
      num: "1",
      title: "Identificamos tu dolor",
      desc: "Análisis profundo de cuellos de botella en tu operación actual y mapeo de oportunidades digitales."
    },
    {
      num: "2",
      title: "Creamos el Prototipo",
      desc: "Diseño iterativo de la solución, validando la interfaz y la experiencia del usuario antes del desarrollo final."
    },
    {
      num: "3",
      title: "Automatizamos tu operación",
      desc: "Implementación técnica, integración de sistemas y despliegue para escalar de manera inmediata."
    }
  ];

  return (
    <section 
      className="px-6 md:px-20 max-w-7xl mx-auto py-16 md:py-24 border-t border-on-surface/10" 
      id="proceso"
    >
      <div className="text-center mb-16">
        <h2 className="font-display text-3xl md:text-[36px] font-bold text-secondary mb-4 tracking-tight">
          Nuestro Método
        </h2>
        <p className="font-sans text-lg md:text-[18px] text-on-surface opacity-90 max-w-2xl mx-auto font-light leading-relaxed">
          Ingeniería de procesos aplicada al diseño digital.
        </p>
      </div>

      <div className="flex flex-col space-y-12 max-w-4xl mx-auto relative">
        {/* Connecting Line from Stitch */}
        <div className="hidden md:block absolute left-[28px] top-8 bottom-8 w-[1px] bg-secondary/20"></div>

        {steps.map((step, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: i * 0.15 }}
            className="flex flex-col md:flex-row gap-6 md:gap-8 items-start relative z-10"
          >
            {/* Step Counter Bubble */}
            <div className="w-14 h-14 rounded-full bg-background border-2 border-secondary flex items-center justify-center shrink-0 shadow-lg">
              <span className="font-display text-lg font-bold text-secondary">
                {step.num}
              </span>
            </div>

            {/* Step Content */}
            <div className="glass-panel p-8 rounded-2xl flex-grow w-full md:w-auto">
              <h3 className="font-display text-xl md:text-[24px] font-bold text-on-surface mb-3">
                {step.title}
              </h3>
              <p className="font-sans text-sm md:text-[16px] text-on-surface/80 opacity-80 leading-relaxed font-light">
                {step.desc}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
