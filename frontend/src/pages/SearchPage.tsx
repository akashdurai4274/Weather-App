import { useState } from "react";
import toast from "react-hot-toast";
import type { AxiosError } from "axios";
import { useCurrentWeatherQuery, useForecastQuery } from "@/features/weather/weatherApi";
import { useAddToWatchlistMutation } from "@/features/watchlist/watchlistApi";
import { getWeatherBgClass } from "@/lib/utils";
import { SearchBar } from "@/components/weather/SearchBar";
import { CurrentWeather } from "@/components/weather/CurrentWeather";
import { DailyForecast } from "@/components/weather/DailyForecast";
import { HourlyForecast } from "@/components/weather/HourlyForecast";
import { WeatherAlerts } from "@/components/weather/WeatherAlerts";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { EmptyState } from "@/components/common/EmptyState";
import { Button } from "@/components/ui/button";
import type { ApiError } from "@/types/api";

export function SearchPage() {
  const [searchCity, setSearchCity] = useState<string | null>(null);

  const {
    data: currentWeather,
    isLoading: currentLoading,
    error: currentError,
  } = useCurrentWeatherQuery({ city: searchCity! }, !!searchCity);

  const {
    data: forecast,
    isLoading: forecastLoading,
  } = useForecastQuery({ city: searchCity! }, !!searchCity);

  const { mutateAsync: addToWatchlist, isPending: isAdding } = useAddToWatchlistMutation();

  const handleSearch = (city: string) => {
    setSearchCity(city);
  };

  const handleAddToWatchlist = async () => {
    if (!currentWeather) return;
    try {
      await addToWatchlist({
        city_name: currentWeather.data.city_name,
        country_code: currentWeather.data.country_code,
        latitude: currentWeather.data.lat,
        longitude: currentWeather.data.lon,
      });
      toast.success(`${currentWeather.data.city_name} added to watchlist`);
    } catch (err) {
      const apiErr = err as AxiosError<ApiError>;
      toast.error(apiErr.response?.data?.detail || "Failed to add to watchlist");
    }
  };

  const bgClass = currentWeather
    ? getWeatherBgClass(currentWeather.data.description)
    : "";

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="flex justify-center">
        <SearchBar onSearch={handleSearch} placeholder="Search for a city..." />
      </div>

      {/* Results */}
      {!searchCity && (
        <EmptyState
          title="Search for a city"
          description="Enter a city name to see current weather and forecasts"
        />
      )}

      {currentLoading && <LoadingSpinner className="py-12" />}

      {currentError && (
        <div className="text-center py-12">
          <h3 className="text-lg font-semibold text-destructive">
            City not found
          </h3>
          <p className="text-muted-foreground mt-1">
            Please check the city name and try again.
          </p>
        </div>
      )}

      {currentWeather && (
        <div className={`weather-bg ${bgClass} -mx-6 px-6 py-6 rounded-lg`}>
          <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
            {/* Add to Watchlist Button */}
            <div className="flex justify-end">
              <Button
                onClick={handleAddToWatchlist}
                variant="secondary"
                disabled={isAdding}
              >
                {isAdding ? "Adding..." : "Add to Watchlist"}
              </Button>
            </div>

            <CurrentWeather data={currentWeather.data} dataSource={currentWeather.data_source} />

            {forecast?.alerts && forecast.alerts.length > 0 && (
              <WeatherAlerts alerts={forecast.alerts} />
            )}

            {forecastLoading ? (
              <LoadingSpinner className="py-8" />
            ) : (
              forecast && (
                <>
                  <HourlyForecast hours={forecast.hourly} />
                  <DailyForecast days={forecast.daily} />
                </>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}
