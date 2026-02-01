import { CloudSun, MapPin, Bell, ShieldCheck, Thermometer, Wind } from "lucide-react";

const features = [
  {
    icon: CloudSun,
    title: "Live Weather",
    description: "Accurate real-time conditions powered by trusted data sources.",
    color: "text-amber-500",
    bg: "bg-amber-500/10",
  },
  {
    icon: MapPin,
    title: "Location Based",
    description: "Automatic weather updates using your current location.",
    color: "text-emerald-500",
    bg: "bg-emerald-500/10",
  },
  {
    icon: Bell,
    title: "Alerts",
    description: "Stay informed with severe weather alerts and warnings.",
    color: "text-red-500",
    bg: "bg-red-500/10",
  },
  {
    icon: ShieldCheck,
    title: "Secure",
    description: "JWT-based authentication and protected APIs.",
    color: "text-blue-500",
    bg: "bg-blue-500/10",
  },
  {
    icon: Thermometer,
    title: "Detailed Metrics",
    description: "Temperature, humidity, UV index, and more at a glance.",
    color: "text-purple-500",
    bg: "bg-purple-500/10",
  },
  {
    icon: Wind,
    title: "Wind & Air Quality",
    description: "Wind speed, direction, and air quality information.",
    color: "text-cyan-500",
    bg: "bg-cyan-500/10",
  },
];

export function FeatureGrid() {
  return (
    <section>
      <h2 className="text-2xl font-bold text-center mb-8">Why Choose Us</h2>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((f) => (
          <div
            key={f.title}
            className="p-6 transition border shadow-sm rounded-xl bg-card hover:shadow-lg hover:-translate-y-1 duration-200"
          >
            <div className={`inline-flex p-3 rounded-lg ${f.bg}`}>
              <f.icon className={`w-6 h-6 ${f.color}`} />
            </div>
            <h3 className="mt-4 text-lg font-semibold">{f.title}</h3>
            <p className="mt-2 text-sm text-muted-foreground">{f.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
