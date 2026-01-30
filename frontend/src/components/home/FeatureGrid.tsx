import { CloudSun, MapPin, Bell, ShieldCheck } from "lucide-react";

const features = [
  {
    icon: CloudSun,
    title: "Live Weather",
    description:
      "Accurate real-time conditions powered by trusted data sources.",
  },
  {
    icon: MapPin,
    title: "Location Based",
    description: "Automatic weather updates using your current location.",
  },
  {
    icon: Bell,
    title: "Alerts",
    description: "Stay informed with severe weather alerts and warnings.",
  },
  {
    icon: ShieldCheck,
    title: "Secure",
    description: "JWT-based authentication and protected APIs.",
  },
];

export function FeatureGrid() {
  return (
    <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {features.map((f) => (
        <div
          key={f.title}
          className="p-6 transition border shadow-sm rounded-xl bg-card hover:shadow-md"
        >
          <f.icon className="w-8 h-8 text-primary" />
          <h3 className="mt-4 text-lg font-semibold">{f.title}</h3>
          <p className="mt-2 text-sm text-muted-foreground">{f.description}</p>
        </div>
      ))}
    </section>
  );
}
