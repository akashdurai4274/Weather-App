// Auth types
export interface SignupRequest {
  username: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  role: string;
}

export interface UserResponse {
  id: string;
  username: string;
  role: string;
  is_active: boolean;
}

// Weather types
export interface CurrentWeatherData {
  city_name: string;
  country_code: string;
  temp: number;
  feels_like: number;
  humidity: number;
  wind_speed: number;
  wind_direction: string;
  description: string;
  icon: string;
  visibility: number | null;
  pressure: number | null;
  uv_index: number | null;
  clouds: number | null;
  sunrise: string | null;
  sunset: string | null;
  aqi: number | null;
  lat: number;
  lon: number;
}

export interface CurrentWeatherResponse {
  data: CurrentWeatherData;
  data_source: string;
}

export interface HourlyForecast {
  timestamp: string;
  temp: number;
  feels_like: number | null;
  humidity: number | null;
  wind_speed: number | null;
  description: string;
  icon: string;
  pop: number | null;
}

export interface DailyForecast {
  date: string;
  temp_high: number;
  temp_low: number;
  humidity: number | null;
  wind_speed: number | null;
  description: string;
  icon: string;
  pop: number | null;
}

export interface WeatherAlert {
  title: string;
  description: string;
  severity: string | null;
  expires: string | null;
  regions: string[];
}

export interface ForecastResponse {
  city_name: string;
  country_code: string;
  lat: number;
  lon: number;
  daily: DailyForecast[];
  hourly: HourlyForecast[];
  alerts: WeatherAlert[];
  data_source: string;
}

// Watchlist types
export interface WatchlistLocation {
  id: string;
  city_name: string;
  country_code: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface WatchlistItem {
  id: string;
  location: WatchlistLocation;
  added_at: string;
}

export interface WatchlistResponse {
  items: WatchlistItem[];
  count: number;
}

export interface AddWatchlistRequest {
  city_name: string;
  country_code?: string;
  latitude?: number;
  longitude?: number;
}

// Preferences types
export interface PreferencesResponse {
  default_city: string | null;
  default_country: string | null;
  default_lat: string | null;
  default_lon: string | null;
  units: string;
}

export interface UpdatePreferencesRequest {
  default_city?: string;
  default_country?: string;
  default_lat?: string;
  default_lon?: string;
  units?: string;
}

// Error type
export interface ApiError {
  detail: string;
}
