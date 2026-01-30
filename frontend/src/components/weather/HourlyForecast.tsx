import { useAppDispatch, useAppSelector } from "@/app/hooks";
import {
  setSelectedHourIndex,
  setWeatherDescription,
} from "@/features/weather/weatherSlice";
import type { HourlyForecast as HourlyForecastType } from "@/types/api";
import { formatTemp, formatTime, cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface HourlyForecastProps {
  hours: HourlyForecastType[];
  units?: string;
}

export function HourlyForecast({ hours, units = "metric" }: HourlyForecastProps) {
  const dispatch = useAppDispatch();
  const selectedIndex = useAppSelector(
    (state) => state.weather.selectedHourIndex
  );

  if (hours.length === 0) return null;

  // Show first 24 hours
  const displayHours = hours.slice(0, 24);

  const handleHourClick = (index: number, description: string) => {
    dispatch(setSelectedHourIndex(index));
    dispatch(setWeatherDescription(description));
  };

  return (
    <Card className="bg-white/80 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-lg">Hourly Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex overflow-x-auto gap-2 pb-2 -mx-2 px-2">
          {displayHours.map((hour, index) => (
            <button
              key={hour.timestamp}
              onClick={() => handleHourClick(index, hour.description)}
              className={cn(
                "flex flex-col items-center min-w-[80px] rounded-lg p-3 transition-colors cursor-pointer",
                selectedIndex === index
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted/50 hover:bg-muted"
              )}
            >
              <span className="text-xs">{formatTime(hour.timestamp)}</span>
              <img
                src={`https://www.weatherbit.io/static/img/icons/${hour.icon}.png`}
                alt={hour.description}
                className="w-8 h-8 my-1"
              />
              <span className="font-semibold text-sm">
                {formatTemp(hour.temp, units)}
              </span>
              {hour.pop !== null && hour.pop > 0 && (
                <span className="text-xs opacity-70">{hour.pop}%</span>
              )}
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
