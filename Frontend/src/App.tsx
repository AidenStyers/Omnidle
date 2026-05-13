import { useGame } from './hooks/useGame'
import TopicHeader from './components/TopicHeader'
import GuessInput from './components/GuessInput'
import GameBoard from './components/GameBoard'
import './App.css'

export default function App() {
  const { topic, options, guesses, won, submitGuess } = useGame()

  return (
    <div className="app">
      <TopicHeader topic={topic} />
      <main className="game">
        {won ? (
          <div className="banner banner--win">You got it in {guesses.length}!</div>
        ) : (
          <GuessInput
            options={options}
            guesses={guesses}
            onSubmit={submitGuess}
            disabled={won}
            attributes={topic.attributes}
          />
        )}
        <GameBoard guesses={guesses} attributes={topic.attributes} />
      </main>
    </div>
  )
}
