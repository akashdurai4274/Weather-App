import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden text-white rounded-xl bg-gradient-to-br from-sky-500 via-blue-600 to-indigo-700">
      <div className="px-6 py-16 sm:px-12 lg:px-16">
        <div className="max-w-4xl">
          <h1 className="text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
            Real-Time Weather <br />
            <span className="text-sky-200">Smarter. Faster. Cleaner.</span>
          </h1>

          <p className="max-w-2xl mt-6 text-lg sm:text-xl text-sky-100">
            Track current conditions, hourly updates, and 5-day forecasts with
            precision. Personalized by your location and preferences.
          </p>

          {/* <div className="flex flex-wrap gap-4 mt-8">
            <Link to="/search">
              <Button
                size="lg"
                className="text-blue-700 bg-white hover:bg-sky-100"
              >
                Search City
              </Button>
            </Link>

            <Link to="/watchlist">
              <Button
                size="lg"
                variant="outline"
                className="text-white border-white hover:bg-white/10"
              >
                View Watchlist
              </Button>
            </Link>
          </div> */}
        </div>
      </div>

      {/* Decorative blur */}
      <div className="absolute rounded-full -top-24 -right-24 h-72 w-72 bg-white/20 blur-3xl" />
      <div className="absolute rounded-full -bottom-24 -left-24 h-72 w-72 bg-white/10 blur-3xl" />
    </section>
  );
}
