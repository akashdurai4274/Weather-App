import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface WeatherState {
  selectedCity: string | null;
  selectedLat: number | null;
  selectedLon: number | null;
  selectedHourIndex: number | null;
  weatherDescription: string;
}

const initialState: WeatherState = {
  selectedCity: null,
  selectedLat: null,
  selectedLon: null,
  selectedHourIndex: null,
  weatherDescription: "",
};

const weatherSlice = createSlice({
  name: "weather",
  initialState,
  reducers: {
    setSelectedCity: (state, action: PayloadAction<string>) => {
      state.selectedCity = action.payload;
      state.selectedLat = null;
      state.selectedLon = null;
      state.selectedHourIndex = null;
    },
    setSelectedCoords: (
      state,
      action: PayloadAction<{ lat: number; lon: number }>
    ) => {
      state.selectedLat = action.payload.lat;
      state.selectedLon = action.payload.lon;
      state.selectedCity = null;
      state.selectedHourIndex = null;
    },
    setSelectedHourIndex: (state, action: PayloadAction<number | null>) => {
      state.selectedHourIndex = action.payload;
    },
    setWeatherDescription: (state, action: PayloadAction<string>) => {
      state.weatherDescription = action.payload;
    },
    resetWeather: () => initialState,
  },
});

export const {
  setSelectedCity,
  setSelectedCoords,
  setSelectedHourIndex,
  setWeatherDescription,
  resetWeather,
} = weatherSlice.actions;
export default weatherSlice.reducer;
