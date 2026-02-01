import type { DailyForecast as DailyForecastType } from "@/types/api";
import { formatTemp, formatDate } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface DailyForecastProps {
  days: DailyForecastType[];
  units?: string;
}

export function DailyForecast({ days, units = "metric" }: DailyForecastProps) {
  if (days.length === 0) return null;

  return (
    <Card className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-lg">5-Day Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {days.map((day) => (
            <div
              key={day.date}
              className="flex items-center justify-between rounded-lg bg-muted/50 p-3"
            >
              <div className="flex items-center gap-3 min-w-0">
                <img
                  src={`https://www.weatherbit.io/static/img/icons/${day.icon}.png`}
                  alt={day.description}
                  className="w-10 h-10 flex-shrink-0"
                />
                <div className="min-w-0">
                  <p className="font-medium text-sm">{formatDate(day.date)}</p>
                  <p className="text-xs text-muted-foreground truncate">
                    {day.description}
                  </p>
                </div>
              </div>
              <div className="text-right flex-shrink-0">
                <span className="font-semibold">
                  {formatTemp(day.temp_high, units)}
                </span>
                <span className="text-muted-foreground ml-2">
                  {formatTemp(day.temp_low, units)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
