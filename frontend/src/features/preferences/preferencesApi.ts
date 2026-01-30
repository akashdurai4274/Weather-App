import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { AxiosError } from "axios";
import api from "../../lib/axios";
import type {
  PreferencesResponse,
  UpdatePreferencesRequest,
  ApiError,
} from "../../types/api";

const PREFS_KEY = ["preferences"] as const;

export function usePreferencesQuery() {
  return useQuery<PreferencesResponse>({
    queryKey: PREFS_KEY,
    queryFn: async () => {
      const res = await api.get<PreferencesResponse>("/preferences");
      return res.data;
    },
  });
}

export function useUpdatePreferencesMutation() {
  const queryClient = useQueryClient();
  return useMutation<PreferencesResponse, AxiosError<ApiError>, UpdatePreferencesRequest>({
    mutationFn: async (data) => {
      const res = await api.put<PreferencesResponse>("/preferences", data);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PREFS_KEY });
    },
  });
}
