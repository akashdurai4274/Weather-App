import { useState, useEffect } from "react";

interface GeoPosition {
  lat: number;
  lon: number;
}

interface UseGeolocationResult {
  position: GeoPosition | null;
  error: string | null;
  loading: boolean;
}

export function useGeolocation(): UseGeolocationResult {
  const [position, setPosition] = useState<GeoPosition | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!navigator.geolocation) {
      console.log("[Geo] Not supported");
      setError("Geolocation not supported");
      setLoading(false);
      return;
    }

    console.log("[Geo] Requesting location...");
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        console.log("[Geo] Success:", latitude, longitude);
        setPosition({ lat: latitude, lon: longitude });
        setLoading(false);
      },
      (err) => {
        console.log("[Geo] Error:", err.code, err.message);
        setError("Location access denied");
        setLoading(false);
      },
      { enableHighAccuracy: false, timeout: 5000, maximumAge: 300000 },
    );
  }, []);

  return { position, error, loading };
}
