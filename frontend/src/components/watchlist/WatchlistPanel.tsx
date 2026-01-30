import { useState } from "react";
import toast from "react-hot-toast";
import type { AxiosError } from "axios";
import {
  useWatchlistQuery,
  useAddToWatchlistMutation,
  useRemoveFromWatchlistMutation,
} from "@/features/watchlist/watchlistApi";
import { useAppDispatch } from "@/app/hooks";
import { setSelectedCity } from "@/features/weather/weatherSlice";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { LoadingSpinner } from "../common/LoadingSpinner";
import { EmptyState } from "../common/EmptyState";
import type { ApiError } from "@/types/api";

export function WatchlistPanel() {
  const [cityInput, setCityInput] = useState("");
  const dispatch = useAppDispatch();

  const { data: watchlist, isLoading } = useWatchlistQuery();
  const { mutateAsync: addToWatchlist, isPending: isAdding } = useAddToWatchlistMutation();
  const { mutateAsync: removeFromWatchlist } = useRemoveFromWatchlistMutation();

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = cityInput.trim();
    if (!trimmed) return;

    try {
      await addToWatchlist({ city_name: trimmed });
      toast.success(`${trimmed} added to watchlist`);
      setCityInput("");
    } catch (err) {
      const apiErr = err as AxiosError<ApiError>;
      toast.error(apiErr.response?.data?.detail || "Failed to add to watchlist");
    }
  };

  const handleRemove = async (id: string, cityName: string) => {
    try {
      await removeFromWatchlist(id);
      toast.success(`${cityName} removed from watchlist`);
    } catch {
      toast.error("Failed to remove from watchlist");
    }
  };

  const handleViewWeather = (cityName: string) => {
    dispatch(setSelectedCity(cityName));
  };

  if (isLoading) {
    return <LoadingSpinner className="py-12" />;
  }

  return (
    <div className="space-y-6">
      {/* Add City Form */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Add to Watchlist</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAdd} className="flex gap-2">
            <Input
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              placeholder="Enter city name..."
              className="flex-1"
            />
            <Button type="submit" disabled={isAdding || !cityInput.trim()}>
              {isAdding ? "Adding..." : "Add"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Watchlist Items */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            Your Locations ({watchlist?.count ?? 0})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!watchlist?.items.length ? (
            <EmptyState
              title="No locations saved"
              description="Add cities to your watchlist to quickly check their weather"
            />
          ) : (
            <div className="space-y-2">
              {watchlist.items.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between rounded-lg bg-muted/50 p-3"
                >
                  <div>
                    <p className="font-medium">{item.location.city_name}</p>
                    {item.location.country_code && (
                      <p className="text-xs text-muted-foreground">
                        {item.location.country_code}
                      </p>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() =>
                        handleViewWeather(item.location.city_name)
                      }
                    >
                      View
                    </Button>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() =>
                        handleRemove(item.id, item.location.city_name)
                      }
                    >
                      Remove
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
