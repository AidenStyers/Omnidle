import { useState } from "react";

export default function GuessInput({ options, guesses, onSubmit, disabled }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  const guessedNames = guesses.map((g) => g.name);
  const filtered = options.filter(
    (o) =>
      o.name.toLowerCase().includes(query.toLowerCase()) &&
      !guessedNames.includes(o.name)
  );

  function handleSelect(name) {
    onSubmit(name);
    setQuery("");
    setOpen(false);
  }

  return (
    <div className="guess-input">
      <input
        type="text"
        placeholder="Search..."
        value={query}
        disabled={disabled}
        onChange={(e) => { setQuery(e.target.value); setOpen(true); }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
      />
      {open && query && filtered.length > 0 && (
        <ul className="suggestions">
          {filtered.map((o) => (
            <li key={o.name} onMouseDown={() => handleSelect(o.name)}>
              {o.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
