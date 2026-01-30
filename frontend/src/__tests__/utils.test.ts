import { getWeatherBgClass, formatTemp } from "../lib/utils";

describe("getWeatherBgClass", () => {
  it("returns thunderstorm class for thunderstorm descriptions", () => {
    expect(getWeatherBgClass("Thunderstorm")).toBe("weather-bg-thunderstorm");
    expect(getWeatherBgClass("Heavy storm")).toBe("weather-bg-thunderstorm");
  });

  it("returns rain class for rain descriptions", () => {
    expect(getWeatherBgClass("Light rain")).toBe("weather-bg-rain");
    expect(getWeatherBgClass("Drizzle")).toBe("weather-bg-rain");
  });

  it("returns snow class for snow descriptions", () => {
    expect(getWeatherBgClass("Heavy snow")).toBe("weather-bg-snow");
    expect(getWeatherBgClass("Sleet")).toBe("weather-bg-snow");
  });

  it("returns cloudy class for cloudy descriptions", () => {
    expect(getWeatherBgClass("Overcast clouds")).toBe("weather-bg-cloudy");
    expect(getWeatherBgClass("Broken cloud")).toBe("weather-bg-cloudy");
  });

  it("returns clear class for clear descriptions", () => {
    expect(getWeatherBgClass("Clear sky")).toBe("weather-bg-clear");
    expect(getWeatherBgClass("Sunny")).toBe("weather-bg-clear");
  });

  it("returns default class for unknown descriptions", () => {
    expect(getWeatherBgClass("Foggy")).toBe("weather-bg-default");
  });
});

describe("formatTemp", () => {
  it("formats metric temperature", () => {
    expect(formatTemp(20.5, "metric")).toBe("21°C");
  });

  it("formats imperial temperature", () => {
    expect(formatTemp(68.2, "imperial")).toBe("68°F");
  });

  it("defaults to metric", () => {
    expect(formatTemp(15)).toBe("15°C");
  });
});
