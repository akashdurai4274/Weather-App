import { useQuery } from "@tanstack/react-query";
import api from "../../lib/axios";
import { WEATHER_STALE_TIME } from "../../lib/queryClient";
import type { CurrentWeatherResponse, ForecastResponse } from "../../types/api";

export interface WeatherQuery {
  city?: string;
  lat?: number;
  lon?: number;
}

export function useCurrentWeatherQuery(params: WeatherQuery, enabled = true) {
  return useQuery<CurrentWeatherResponse>({
    queryKey: ["weather", "current", params],
    queryFn: async () => {
      const res = await api.get<CurrentWeatherResponse>("/weather/current", { params });
      return res.data;
    },
    enabled,
    staleTime: WEATHER_STALE_TIME,
    refetchInterval: WEATHER_STALE_TIME,
  });
}

export function useForecastQuery(params: WeatherQuery, enabled = true) {
  return useQuery<ForecastResponse>({
    queryKey: ["weather", "forecast", params],
    queryFn: async () => {
      const res = await api.get<ForecastResponse>("/weather/forecast", { params });
      return res.data;
    },
    enabled,
    staleTime: WEATHER_STALE_TIME,
    refetchInterval: WEATHER_STALE_TIME,
  });
}
