import type { WeatherAlert } from "@/types/api";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";

interface WeatherAlertsProps {
  alerts: WeatherAlert[];
}

export function WeatherAlerts({ alerts }: WeatherAlertsProps) {
  if (alerts.length === 0) return null;

  return (
    <Card className="border-destructive bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-lg text-destructive">
          Weather Alerts
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {alerts.map((alert, index) => (
          <div key={index} className="rounded-lg border border-destructive/50 p-4">
            <div className="flex items-center gap-2 mb-2">
              <h4 className="font-semibold">{alert.title}</h4>
              {alert.severity && (
                <Badge variant="warning">{alert.severity}</Badge>
              )}
            </div>
            <p className="text-sm text-muted-foreground">
              {alert.description}
            </p>
            {alert.expires && (
              <p className="text-xs text-muted-foreground mt-2">
                Expires: {alert.expires}
              </p>
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
