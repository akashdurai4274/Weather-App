import { HeroSection } from "@/components/home/HeroSection";
import { FeatureGrid } from "@/components/home/FeatureGrid";
import { WeatherSection } from "@/components/home/WeatherSection";

export function HomePage() {

  return (
    <div className="space-y-12">
      {/* Static sections – instant load */}
      <HeroSection />
      <FeatureGrid />

      {/* Dynamic section – backend driven */}
      <WeatherSection />
    </div>
  );
}
