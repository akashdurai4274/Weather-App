import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getWeatherBgClass(description: string): string {
  const desc = description.toLowerCase();
  if (desc.includes("thunder") || desc.includes("storm")) return "weather-bg-thunderstorm";
  if (desc.includes("rain") || desc.includes("drizzle")) return "weather-bg-rain";
  if (desc.includes("snow") || desc.includes("sleet") || desc.includes("ice")) return "weather-bg-snow";
  if (desc.includes("cloud") || desc.includes("overcast")) return "weather-bg-cloudy";
  if (desc.includes("clear") || desc.includes("sun") || desc.includes("few clouds")) return "weather-bg-clear";
  return "weather-bg-default";
}

export function formatTemp(temp: number, units: string = "metric"): string {
  const symbol = units === "imperial" ? "F" : "C";
  return `${Math.round(temp)}°${symbol}`;
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

export function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}
