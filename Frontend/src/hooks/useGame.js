import { useState } from "react";
import { allOptions, ANSWER, todaysTopic } from "../data/placeholder";

// Swap these fetch calls for real API calls when backend is ready
export function useGame() {
  const [guesses, setGuesses] = useState([]);
  const [won, setWon] = useState(false);

  const topic = todaysTopic;
  const options = allOptions;

  function getResult(guess) {
    const answer = allOptions.find((o) => o.name === ANSWER);
    return topic.attributes.map((attr) => {
      const guessVal = guess[attr];
      const answerVal = answer[attr];
      const correct = guessVal === answerVal;

      let hint = "wrong";
      if (correct) hint = "correct";
      else if (typeof guessVal === "number" && typeof answerVal === "number") {
        hint = guessVal < answerVal ? "higher" : "lower";
      }

      return { attr, value: String(guessVal), hint };
    });
  }

  function submitGuess(name) {
    if (won || guesses.some((g) => g.name === name)) return;
    const guess = allOptions.find((o) => o.name === name);
    if (!guess) return;

    const result = getResult(guess);
    const isWin = result.every((r) => r.hint === "correct");
    setGuesses((prev) => [...prev, { name, result }]);
    if (isWin) setWon(true);
  }

  return { topic, options, guesses, won, submitGuess };
}
