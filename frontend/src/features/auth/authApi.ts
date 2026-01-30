import { useMutation } from "@tanstack/react-query";
import type { AxiosError } from "axios";
import api from "../../lib/axios";
import type {
  LoginRequest,
  SignupRequest,
  TokenResponse,
  UserResponse,
  ApiError,
} from "../../types/api";

export function useSignupMutation() {
  return useMutation<UserResponse, AxiosError<ApiError>, SignupRequest>({
    mutationFn: async (data) => {
      const res = await api.post<UserResponse>("/auth/signup", data);
      return res.data;
    },
  });
}

export function useLoginMutation() {
  return useMutation<TokenResponse, AxiosError<ApiError>, LoginRequest>({
    mutationFn: async (data) => {
      const res = await api.post<TokenResponse>("/auth/login", data);
      return res.data;
    },
  });
}

export function useRefreshTokenMutation() {
  return useMutation<TokenResponse, AxiosError<ApiError>, { refresh_token: string }>({
    mutationFn: async (data) => {
      const res = await api.post<TokenResponse>("/auth/refresh", data);
      return res.data;
    },
  });
}
