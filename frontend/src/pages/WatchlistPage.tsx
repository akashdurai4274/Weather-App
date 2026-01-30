import { useAppSelector } from "@/app/hooks";
import { useCurrentWeatherQuery } from "@/features/weather/weatherApi";
import { WatchlistPanel } from "@/components/watchlist/WatchlistPanel";
import { CurrentWeather } from "@/components/weather/CurrentWeather";
import { getWeatherBgClass } from "@/lib/utils";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";

export function WatchlistPage() {
  const { selectedCity } = useAppSelector((state) => state.weather);

  const {
    data: weather,
    isLoading,
  } = useCurrentWeatherQuery({ city: selectedCity! }, !!selectedCity);

  const bgClass = weather
    ? getWeatherBgClass(weather.data.description)
    : "";

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Left: Watchlist */}
      <div>
        <WatchlistPanel />
      </div>

      {/* Right: Selected City Weather */}
      <div>
        {selectedCity && (
          <div className={`weather-bg ${bgClass} rounded-lg p-4`}>
            {isLoading ? (
              <LoadingSpinner className="py-12" />
            ) : weather ? (
              <CurrentWeather data={weather.data} dataSource={weather.data_source} />
            ) : null}
          </div>
        )}
        {!selectedCity && (
          <div className="flex items-center justify-center h-64 rounded-lg border-2 border-dashed">
            <p className="text-muted-foreground">
              Select a city from your watchlist to view weather
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
