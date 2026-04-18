import type { AttrResult, Guess, HintType } from "../data/types";

function HintCell({ value, hint }: { value: string; hint: HintType }) {
  const icons: Record<HintType, string> = { correct: "✓", higher: "↑", lower: "↓", wrong: "✗" };
  return (
    <div className={`cell cell--${hint}`}>
      <span className="cell-value">{value}</span>
      <span className="cell-hint">{icons[hint]}</span>
    </div>
  );
}

function GuessRow({ name, result, attributes }: { name: string; result: AttrResult[]; attributes: string[] }) {
  return (
    <div className="guess-row">
      <div className="cell cell--name">{name}</div>
      {attributes.map((attr) => {
        const col = result.find((r) => r.attr === attr)!;
        return <HintCell key={attr} value={col.value} hint={col.hint} />;
      })}
    </div>
  );
}

function HeaderRow({ attributes }: { attributes: string[] }) {
  return (
    <div className="guess-row guess-row--header">
      <div className="cell cell--name">Guess</div>
      {attributes.map((attr) => (
        <div key={attr} className="cell cell--header">{attr}</div>
      ))}
    </div>
  );
}

interface Props {
  guesses: Guess[];
  attributes: string[];
}

export default function GameBoard({ guesses, attributes }: Props) {
  if (guesses.length === 0) return null;
  return (
    <div className="game-board">
      <HeaderRow attributes={attributes} />
      {guesses.map((g) => (
        <GuessRow key={g.name} name={g.name} result={g.result} attributes={attributes} />
      ))}
    </div>
  );
}
