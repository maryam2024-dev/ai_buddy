import React, { useState } from "react";

const ArabicAlphabetQuiz = () => {
  const questions = [
    {
      letter: "أ",
      choices: ["https://arabcodeweek2023.alecso.org/competition/activities/mzu/1cub/images/2ahpi1l5kclk44a0g.jpg", "lion.png", "rabbit.png"],
      correct: 0,
    },
    {
      letter: "ب",
      choices: ["banana.png", "car.png", "house.png"],
      correct: 0,
    },
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const prevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-100 p-4">
      <h1 className="text-2xl font-bold mb-6">Math Quiz</h1>
      <div className="text-3xl font-bold mb-4">5 + 4</div>
      <div className="grid grid-cols-3 gap-4 mb-6">
          <button className="p-2 bg-white rounded-xl shadow-md">
            <img src={"https://i.ytimg.com/vi/mu6mw8aqDCQ/maxresdefault.jpg"} alt="choice" className="w-16 h-16" />
          </button>
          <button className="p-2 bg-white rounded-xl shadow-md">
            <img src={"https://thumbs.dreamstime.com/z/kid-s-hand-showing-number-five-sign-fingers-icon-counting-education-childrens-vector-illustration-digit-163181916.jpg"} alt="choice" className="w-16 h-16" />
          </button>
          <button className="p-2 bg-white rounded-xl shadow-md">
            <img src={"https://i.ytimg.com/vi/rSoYRFYT3fA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBX-8ohZES3xz78LB7sSdpgL_2sRA"} alt="choice" className="w-16 h-16" />
          </button>
      </div>
      <div className="flex gap-4">
        <button onClick={prevQuestion} className="p-2 bg-gray-300 rounded-lg shadow">Back</button>
        <button onClick={nextQuestion} className="p-2 bg-green-300 rounded-lg shadow">Next</button>
      </div>
    </div>
  );
};

export default ArabicAlphabetQuiz;
