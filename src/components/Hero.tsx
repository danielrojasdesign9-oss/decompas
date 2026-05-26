import { motion } from "motion/react";

interface HeroProps {
  onScaleOperation: () => void;
  onScrollToSection: (sectionId: string) => void;
}

export default function Hero({ onScaleOperation, onScrollToSection }: HeroProps) {
  return (
    <section
      id="hero"
      className="min-h-[70vh] md:min-h-[819px] flex flex-col justify-center px-6 md:px-20 max-w-7xl mx-auto py-12 md:py-24"
    >
      <div className="max-w-4xl">
        {/* Animated Headline matching exactly Stitch text and typography styles */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="font-display text-[24px] md:text-[56px] leading-[44px] md:leading-[64px] font-bold text-secondary mb-8 tracking-tight"
        >
          Si pasas el día respondiendo los mismos precios y pasando datos a mano, tu negocio no está creciendo, te está consumiendo. Automatiza tu flujo hoy.
        </motion.h1>

        {/* Animated Subtitle matching exactly Stitch text styles */}
        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="font-sans text-lg md:text-[18px] leading-relaxed text-on-surface max-w-2xl mb-12 opacity-90 font-light"
        >
          Escalamos tu operación con tecnología de vanguardia y diseño de alta conversión.
        </motion.p>

        {/* Action Buttons matching exactly Stitch styles */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="flex flex-wrap gap-4 md:gap-6"
        >
          <button
            onClick={onScaleOperation}
            className="bg-secondary text-on-secondary font-display text-[11px] uppercase tracking-widest px-8 py-4 rounded-full hover:scale-105 transition-transform duration-200 font-bold cursor-pointer"
          >
            Escala tu Negocio
          </button>

          <button
            onClick={() => onScrollToSection("proceso")}
            className="border border-on-surface/20 text-on-surface font-display text-[11px] uppercase tracking-widest px-8 py-4 rounded-full hover:border-secondary hover:text-secondary hover:scale-102 transition-all duration-300 cursor-pointer"
          >
            Ver Proceso
          </button>
        </motion.div>
      </div>
    </section>
  );
}
