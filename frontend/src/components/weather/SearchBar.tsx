import { useState, useCallback } from "react";
import { useAppDispatch } from "@/app/hooks";
import { setSelectedCity } from "@/features/weather/weatherSlice";
// import { useDebounce } from "@/hooks/useDebounce";
import { Input } from "../ui/input";
import { Button } from "../ui/button";

interface SearchBarProps {
  onSearch: (city: string) => void;
  placeholder?: string;
}

export function SearchBar({
  onSearch,
  placeholder = "Search city...",
}: SearchBarProps) {
  const [query, setQuery] = useState("");
  const dispatch = useAppDispatch();
  // const debouncedQuery = useDebounce(query, 500);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      const trimmed = query.trim();
      if (trimmed) {
        dispatch(setSelectedCity(trimmed));
        onSearch(trimmed);
      }
    },
    [query, dispatch, onSearch],
  );

  return (
    <form onSubmit={handleSubmit} className="flex w-full max-w-lg gap-2">
      <Input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="flex-1"
      />
      <Button type="submit" disabled={!query.trim()}>
        Search
      </Button>
    </form>
  );
}
