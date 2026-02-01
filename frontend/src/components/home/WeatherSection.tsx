import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/app/hooks";
import {
  setSelectedCity,
  setSelectedCoords,
  setWeatherDescription,
} from "@/features/weather/weatherSlice";
import {
  useCurrentWeatherQuery,
  useForecastQuery,
} from "@/features/weather/weatherApi";
import { usePreferencesQuery } from "@/features/preferences/preferencesApi";
import { useGeolocation } from "@/hooks/useGeolocation";
import { CurrentWeather } from "@/components/weather/CurrentWeather";
import { DailyForecast } from "@/components/weather/DailyForecast";
import { HourlyForecast } from "@/components/weather/HourlyForecast";
import { WeatherAlerts } from "@/components/weather/WeatherAlerts";
import { Skeleton } from "@/components/ui/skeleton";

export function WeatherSection() {
  const dispatch = useAppDispatch();
  const { selectedCity, selectedLat, selectedLon } =
    useAppSelector((state) => state.weather);
  const { position, loading: geoLoading } = useGeolocation();
  const { data: prefs } = usePreferencesQuery();

  // Determine what location to use: preferences > geolocation > default
  useEffect(() => {
    console.log("[Weather] State:", { selectedCity, selectedLat, geoLoading, position, prefs: prefs?.default_city });
    if (selectedCity || selectedLat) return;

    if (prefs?.default_city) {
      console.log("[Weather] Using pref city:", prefs.default_city);
      dispatch(setSelectedCity(prefs.default_city));
    } else if (position && !geoLoading) {
      console.log("[Weather] Using geolocation:", position.lat, position.lon);
      dispatch(setSelectedCoords({ lat: position.lat, lon: position.lon }));
    } else if (!geoLoading) {
      console.log("[Weather] Fallback to London");
      dispatch(setSelectedCity("London"));
    }
  }, [prefs, position, geoLoading, selectedCity, selectedLat, dispatch]);

  // Only enable queries once a definitive location has been set in Redux
  const hasLocation = !!(selectedCity || selectedLat);

  // Build query params
  const queryParams = selectedCity
    ? { city: selectedCity }
    : selectedLat && selectedLon
      ? { lat: selectedLat, lon: selectedLon }
      : { city: "London" };

  console.log("[Weather] Query params:", queryParams);

  const enabled = hasLocation;

  const {
    data: currentWeather,
    isLoading: currentLoading,
    error: currentError,
  } = useCurrentWeatherQuery(queryParams, enabled);

  const { data: forecast, isLoading: forecastLoading } = useForecastQuery(
    queryParams,
    enabled,
  );

  // Update background based on weather
  useEffect(() => {
    if (currentWeather?.data.description) {
      dispatch(setWeatherDescription(currentWeather.data.description));
    }
  }, [currentWeather, dispatch]);


  if (!hasLocation || (currentLoading && !currentWeather)) {
    return (
      <div className="space-y-4">
        <Skeleton className="w-full h-64" />
        <Skeleton className="w-full h-48" />
        <Skeleton className="w-full h-48" />
      </div>
    );
  }

  if (currentError) {
    return (
      <div className="py-12 text-center">
        <h2 className="text-xl font-semibold text-destructive">
          Failed to load weather data
        </h2>
        <p className="mt-2 text-muted-foreground">
          Please check your connection and try again.
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
        {/* Current Weather */}
        {currentWeather && (
          <CurrentWeather
            data={currentWeather.data}
            dataSource={currentWeather.data_source}
          />
        )}

        {/* Alerts */}
        {forecast?.alerts && forecast.alerts.length > 0 && (
          <WeatherAlerts alerts={forecast.alerts} />
        )}

        {/* Hourly Forecast */}
        {forecastLoading ? (
          <Skeleton className="w-full h-40" />
        ) : (
          forecast && <HourlyForecast hours={forecast.hourly} />
        )}

        {/* 5-Day Forecast */}
        {forecastLoading ? (
          <Skeleton className="w-full h-64" />
        ) : (
          forecast && <DailyForecast days={forecast.daily} />
        )}
      </div>
    </div>
  );
}
