"use client";

import { useState, useEffect } from "react";

// --- Types ---
type Difficulty = "easy" | "medium" | "hard";

interface TriviaQuestion {
  category: string;
  type: "multiple" | "boolean";
  difficulty: string;
  question: string; // HTML encoded string
  correct_answer: string;
  incorrect_answers: string[];
}

interface ProcessedQuestion extends TriviaQuestion {
  shuffled_answers: string[];
}

// --- Utility: Decode HTML Entities ---
// OpenTDB returns strings like "Entertainment: Video Games &amp; Others"
function decodeHtml(html: string) {
  const txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}

export default function TriviaGame() {
  // --- State ---
  const [gameState, setGameState] = useState<"start" | "loading" | "playing" | "finished">("start");
  const [questions, setQuestions] = useState<ProcessedQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  
  // UI State for the current turn
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isAnswerChecked, setIsAnswerChecked] = useState(false);

  // Settings
  const [difficulty, setDifficulty] = useState<Difficulty>("medium");
  const [amount, setAmount] = useState(5);

  // --- Actions ---

  const fetchQuestions = async () => {
    setGameState("loading");
    setScore(0);
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setIsAnswerChecked(false);

    try {
      // Connect to your FastAPI Backend
      const res = await fetch(
        `http://localhost:8000/trivia?amount=${amount}&difficulty=${difficulty}`
      );
      
      if (!res.ok) throw new Error("Failed to fetch questions");

      const data = await res.json();
      
      // We need to shuffle answers immediately upon fetching
      // otherwise re-renders will shuffle them constantly
      const processed: ProcessedQuestion[] = data.results.map((q: TriviaQuestion) => {
        const allAnswers = [...q.incorrect_answers, q.correct_answer];
        // Fisher-Yates Shuffle
        for (let i = allAnswers.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [allAnswers[i], allAnswers[j]] = [allAnswers[j], allAnswers[i]];
        }
        return { ...q, shuffled_answers: allAnswers };
      });

      setQuestions(processed);
      setGameState("playing");
    } catch (error) {
      console.error(error);
      alert("Error fetching questions. Make sure FastAPI is running!");
      setGameState("start");
    }
  };

  const handleAnswerClick = (answer: string) => {
    if (isAnswerChecked) return; // Prevent changing answer after selection
    
    setSelectedAnswer(answer);
    setIsAnswerChecked(true);

    const currentQuestion = questions[currentIndex];
    const isCorrect = answer === currentQuestion.correct_answer;

    if (isCorrect) {
      setScore((prev) => prev + 1);
    }

    // Wait 1.5 seconds then move to next question
    setTimeout(() => {
      if (currentIndex + 1 < questions.length) {
        setCurrentIndex((prev) => prev + 1);
        setSelectedAnswer(null);
        setIsAnswerChecked(false);
      } else {
        setGameState("finished");
      }
    }, 1500);
  };

  // --- Render Components ---

  if (gameState === "start") {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
        <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md text-center">
          <h1 className="text-3xl font-bold text-blue-600 mb-6">Trivia Master</h1>
          
          <div className="mb-4 text-left">
            <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
            <select 
              value={difficulty} 
              onChange={(e) => setDifficulty(e.target.value as Difficulty)}
              className="w-full p-2 border rounded-md text-black"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="mb-6 text-left">
            <label className="block text-sm font-medium text-gray-700 mb-1">Questions</label>
            <select 
              value={amount} 
              onChange={(e) => setAmount(Number(e.target.value))}
              className="w-full p-2 border rounded-md text-black"
            >
              <option value="5">5 Questions</option>
              <option value="10">10 Questions</option>
              <option value="20">20 Questions</option>
            </select>
          </div>

          <button 
            onClick={fetchQuestions}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition"
          >
            Start Quiz
          </button>
        </div>
      </main>
    );
  }

  if (gameState === "loading") {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-xl text-blue-600 animate-pulse font-semibold">Loading Questions...</div>
      </main>
    );
  }

  if (gameState === "finished") {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
        <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md text-center">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Game Over!</h2>
          <p className="text-gray-600 mb-6">Your Score</p>
          <div className="text-6xl font-black text-blue-600 mb-6">
            {score} <span className="text-2xl text-gray-400">/ {questions.length}</span>
          </div>
          <button 
            onClick={() => setGameState("start")}
            className="w-full bg-gray-800 hover:bg-gray-900 text-white font-bold py-3 rounded-lg transition"
          >
            Play Again
          </button>
        </div>
      </main>
    );
  }

  // --- Playing State ---
  const currentQ = questions[currentIndex];

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="bg-blue-600 p-4 flex justify-between text-white font-semibold">
          <span>{currentQ.category}</span>
          <span>{currentIndex + 1} / {questions.length}</span>
        </div>

        {/* Question */}
        <div className="p-8">
          <h3 className="text-xl font-medium text-gray-800 mb-8 leading-relaxed">
            {decodeHtml(currentQ.question)}
          </h3>

          <div className="space-y-3">
            {currentQ.shuffled_answers.map((ans, idx) => {
              const isSelected = selectedAnswer === ans;
              const isCorrect = ans === currentQ.correct_answer;
              
              // Styling logic based on game state
              let btnClass = "w-full text-left p-4 rounded-lg border-2 transition-all font-medium ";
              
              if (isAnswerChecked) {
                if (isCorrect) {
                  btnClass += "bg-green-100 border-green-500 text-green-800";
                } else if (isSelected && !isCorrect) {
                  btnClass += "bg-red-100 border-red-500 text-red-800";
                } else {
                  btnClass += "bg-gray-50 border-gray-200 text-gray-400 opacity-50";
                }
              } else {
                btnClass += "bg-white border-gray-200 hover:border-blue-500 hover:bg-blue-50 text-gray-700";
              }

              return (
                <button
                  key={idx}
                  onClick={() => handleAnswerClick(ans)}
                  disabled={isAnswerChecked}
                  className={btnClass}
                >
                  {decodeHtml(ans)}
                </button>
              );
            })}
          </div>
        </div>

        {/* Score Footer */}
        <div className="p-4 bg-gray-50 border-t flex justify-between items-center text-sm text-gray-500">
          <span>Difficulty: <span className="capitalize text-gray-800">{currentQ.difficulty}</span></span>
          <span>Current Score: <span className="font-bold text-blue-600 text-lg">{score}</span></span>
        </div>
      </div>
    </main>
  );
}