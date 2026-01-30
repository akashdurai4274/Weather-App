import weatherReducer, {
  setSelectedCity,
  setSelectedCoords,
  setSelectedHourIndex,
  setWeatherDescription,
  resetWeather,
} from "../features/weather/weatherSlice";

describe("weatherSlice", () => {
  const initialState = {
    selectedCity: null,
    selectedLat: null,
    selectedLon: null,
    selectedHourIndex: null,
    weatherDescription: "",
  };

  it("should return the initial state", () => {
    expect(weatherReducer(undefined, { type: "unknown" })).toEqual(initialState);
  });

  it("should handle setSelectedCity", () => {
    const state = weatherReducer(initialState, setSelectedCity("London"));
    expect(state.selectedCity).toBe("London");
    expect(state.selectedLat).toBeNull();
    expect(state.selectedLon).toBeNull();
  });

  it("should handle setSelectedCoords", () => {
    const state = weatherReducer(
      initialState,
      setSelectedCoords({ lat: 51.5, lon: -0.12 })
    );
    expect(state.selectedLat).toBe(51.5);
    expect(state.selectedLon).toBe(-0.12);
    expect(state.selectedCity).toBeNull();
  });

  it("should handle setSelectedHourIndex", () => {
    const state = weatherReducer(initialState, setSelectedHourIndex(5));
    expect(state.selectedHourIndex).toBe(5);
  });

  it("should handle setWeatherDescription", () => {
    const state = weatherReducer(
      initialState,
      setWeatherDescription("Clear sky")
    );
    expect(state.weatherDescription).toBe("Clear sky");
  });

  it("should handle resetWeather", () => {
    const modifiedState = {
      selectedCity: "Paris",
      selectedLat: 48.8,
      selectedLon: 2.3,
      selectedHourIndex: 3,
      weatherDescription: "Cloudy",
    };
    const state = weatherReducer(modifiedState, resetWeather());
    expect(state).toEqual(initialState);
  });
});
