import { motion } from "motion/react";

export default function Stats() {
  return (
    <section className="px-6 md:px-20 max-w-7xl mx-auto py-16 md:py-24" id="stats-section">
      <div className="flex flex-col md:flex-row gap-6 md:gap-12">
        {/* Header Left Col */}
        <div className="md:w-1/3 flex flex-col justify-start items-start">
          <h2 className="font-display text-3xl md:text-[36px] font-bold text-secondary mb-6 leading-tight">
            ¿Por qué digitalizarte?
          </h2>
          <div className="h-1 w-24 bg-secondary rounded-full mb-6"></div>
          <p className="font-sans text-sm text-on-surface opacity-85 leading-relaxed">
            Mapeamos y automatizamos los procesos clave para que tu negocio crezca de manera sostenible en canales digitales.
          </p>
        </div>

        {/* Stats Grid Right Col */}
        <div className="md:w-2/3 grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1 */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="glass-panel p-8 rounded-2xl flex flex-col items-start hover:border-secondary/50 transition-all duration-300"
          >
            <span className="material-symbols-outlined text-secondary text-4xl mb-4" style={{ fontVariationSettings: "'wght' 200" }}>
              trending_up
            </span>
            <h3 className="font-display text-3xl md:text-[24px] font-bold text-on-surface mb-2">
              +45%
            </h3>
            <p className="font-sans text-sm text-on-surface opacity-80">
              Retención de clientes
            </p>
          </motion.div>

          {/* Card 2 */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="glass-panel p-8 rounded-2xl flex flex-col items-start hover:border-secondary/50 transition-all duration-300"
          >
            <span className="material-symbols-outlined text-secondary text-4xl mb-4" style={{ fontVariationSettings: "'wght' 200" }}>
              bolt
            </span>
            <h3 className="font-display text-3xl md:text-[24px] font-bold text-on-surface mb-2">
              3x
            </h3>
            <p className="font-sans text-sm text-on-surface opacity-80">
              Velocidad de atención
            </p>
          </motion.div>

          {/* Card 3 */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="glass-panel p-8 rounded-2xl flex flex-col items-start hover:border-secondary/50 transition-all duration-300"
          >
            <span className="material-symbols-outlined text-secondary text-4xl mb-4" style={{ fontVariationSettings: "'wght' 200" }}>
              schedule
            </span>
            <h3 className="font-display text-3xl md:text-[24px] font-bold text-on-surface mb-2">
              24/7
            </h3>
            <p className="font-sans text-sm text-on-surface opacity-80">
              Operación automática
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
