import { QueryClient } from "@tanstack/react-query";

export const WEATHER_STALE_TIME = 5 * 60 * 1000; // 5 min — matches backend mock bucket

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: WEATHER_STALE_TIME,
      gcTime: 10 * 60 * 1000, // keep in GC for 10 min
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
