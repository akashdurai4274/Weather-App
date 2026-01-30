import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { AxiosError } from "axios";
import api from "../../lib/axios";
import type {
  AddWatchlistRequest,
  WatchlistItem,
  WatchlistResponse,
  ApiError,
} from "../../types/api";

const WATCHLIST_KEY = ["watchlist"] as const;

export function useWatchlistQuery() {
  return useQuery<WatchlistResponse>({
    queryKey: WATCHLIST_KEY,
    queryFn: async () => {
      const res = await api.get<WatchlistResponse>("/watchlist");
      return res.data;
    },
  });
}

export function useAddToWatchlistMutation() {
  const queryClient = useQueryClient();
  return useMutation<WatchlistItem, AxiosError<ApiError>, AddWatchlistRequest>({
    mutationFn: async (data) => {
      const res = await api.post<WatchlistItem>("/watchlist", data);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: WATCHLIST_KEY });
    },
  });
}

export function useRemoveFromWatchlistMutation() {
  const queryClient = useQueryClient();
  return useMutation<void, AxiosError<ApiError>, string>({
    mutationFn: async (id) => {
      await api.delete(`/watchlist/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: WATCHLIST_KEY });
    },
  });
}
