import Header from "./components/Header";
import Hero from "./components/Hero";
import Stats from "./components/Stats";
import Services from "./components/Services";
import Proceso from "./components/Proceso";
import ContactForm from "./components/ContactForm";
import Footer from "./components/Footer";

export default function App() {
  // Smooth scroll handler with safety check
  const handleScrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const handleScaleOperation = () => {
    handleScrollToSection("cta-section");
  };

  return (
    <div className="bg-background min-h-screen text-on-surface selection:bg-secondary selection:text-on-secondary antialiased flex flex-col relative">
      {/* Ambient Tech Pattern Background from Stitch */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute inset-0 bg-pattern"></div>
      </div>

      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Premium Header */}
        <Header 
          onScrollToSection={handleScrollToSection} 
        />

        {/* Hero Presentation */}
        <Hero 
          onScaleOperation={handleScaleOperation} 
          onScrollToSection={handleScrollToSection} 
        />

        {/* Metrics / Stats panel */}
        <Stats />

        {/* Premium Services list */}
        <Services />

        {/* Step by step method process */}
        <Proceso />

        {/* High-Converting Form captures */}
        <ContactForm />

        {/* Interactive footer links */}
        <Footer onScrollToSection={handleScrollToSection} />
      </div>
    </div>
  );
}
