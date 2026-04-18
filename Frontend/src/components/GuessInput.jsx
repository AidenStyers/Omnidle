import { useState } from "react";

export default function GuessInput({ options, guesses, onSubmit, disabled, attributes }) {
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
          <li className="suggestions-header">
            <div className="guess-row">
              <div className="cell cell--name">Option</div>
              {attributes.map((attr) => (
                <div key={attr} className="cell cell--header">{attr}</div>
              ))}
            </div>
          </li>
          {filtered.map((o) => (
            <li key={o.name} onMouseDown={() => handleSelect(o.name)} className="suggestion-row">
              <div className="guess-row">
                <div className="cell cell--name">{o.name}</div>
                {attributes.map((attr) => (
                  <div key={attr} className="cell cell--neutral">
                    {String(o[attr])}
                  </div>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
