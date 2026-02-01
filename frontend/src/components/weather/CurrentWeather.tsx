import type { CurrentWeatherData } from "@/types/api";
import { formatTemp } from "@/lib/utils";
import { useAppSelector } from "@/app/hooks";
import { Card, CardContent } from "../ui/card";
import { Badge } from "../ui/badge";

interface CurrentWeatherProps {
  data: CurrentWeatherData;
  units?: string;
  dataSource?: string;
}

function DataSourceBadge({ source }: { source: string }) {
  const role = useAppSelector((state) => state.auth.role);
  if (role !== "ADMIN") return null;

  const isLive = source === "live";
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${
        isLive
          ? "bg-green-100 text-green-800 border border-green-300"
          : "bg-amber-100 text-amber-800 border border-amber-300"
      }`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${isLive ? "bg-green-500" : "bg-amber-500"}`}
      />
      {isLive ? "LIVE API" : "MOCK DATA"}
    </span>
  );
}

export function CurrentWeather({ data, units = "metric", dataSource }: CurrentWeatherProps) {
  return (
    <Card className="overflow-hidden bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
      <CardContent className="p-6">
        {dataSource && (
          <div className="flex justify-end mb-2">
            <DataSourceBadge source={dataSource} />
          </div>
        )}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          {/* Location & Main Temp */}
          <div>
            <h2 className="text-2xl font-bold">
              {data.city_name}, {data.country_code}
            </h2>
            <p className="text-6xl font-light mt-2">
              {formatTemp(data.temp, units)}
            </p>
            <p className="text-muted-foreground mt-1">
              Feels like {formatTemp(data.feels_like, units)}
            </p>
            <Badge className="mt-2">{data.description}</Badge>
          </div>

          {/* Weather Icon */}
          <div className="flex items-center justify-center">
            <img
              src={`https://www.weatherbit.io/static/img/icons/${data.icon}.png`}
              alt={data.description}
              className="w-24 h-24"
            />
          </div>
        </div>

        {/* Details Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 mt-6">
          <DetailItem label="Humidity" value={`${data.humidity}%`} />
          <DetailItem label="Wind" value={`${data.wind_speed} m/s`} />
          <DetailItem label="Direction" value={data.wind_direction} />
          {data.visibility !== null && (
            <DetailItem label="Visibility" value={`${data.visibility} km`} />
          )}
          {data.pressure !== null && (
            <DetailItem label="Pressure" value={`${data.pressure} hPa`} />
          )}
          {data.uv_index !== null && (
            <DetailItem label="UV Index" value={data.uv_index.toString()} />
          )}
          {data.clouds !== null && (
            <DetailItem label="Cloud Cover" value={`${data.clouds}%`} />
          )}
          {data.aqi !== null && (
            <DetailItem label="Air Quality" value={data.aqi.toString()} />
          )}
          {data.sunrise && <DetailItem label="Sunrise" value={data.sunrise} />}
          {data.sunset && <DetailItem label="Sunset" value={data.sunset} />}
        </div>
      </CardContent>
    </Card>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-muted/50 p-3">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="text-sm font-semibold">{value}</p>
    </div>
  );
}
