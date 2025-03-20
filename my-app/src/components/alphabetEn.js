import React, { useState, useEffect } from "react";
import Header from "./header";
import cover from "../assets/img.png";
import { useNavigate } from "react-router-dom";

const AlphabetEn = () => {
    const navigate = useNavigate();

    // Initial states
    const [level, setLevel] = useState(1);
    const [question, setQuestion] = useState("");
    const [exercise, setExercise] = useState([]);
    const [imageUrls, setImageUrls] = useState([]);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [showMessage, setShowMessage] = useState("");
    const [isNextEnabled, setIsNextEnabled] = useState(false);
    const [selectedLetters, setSelectedLetters] = useState({});

    useEffect(() => {
        // fetch("http://127.0.0.1:8000/api/alpabet-eng/generate", {
//     method: "POST",
//     headers: {
//         "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ level: level }),
// })
//     .then((response) => response.json())
//     .then((data) => {
//         setLevel(data.level);
//         setQuestion(data.question);
//         setExercise(data.exercise);
//         setCorrectWord(data.correct_word);
//
//         // ✅ Ensure imageUrls is an array
//         const images = Array.isArray(data.image_url) ? data.image_url : [data.image_url];
//         setImageUrls(images);
//     })
//     .catch((error) => console.error("Error fetching exercise:", error));

        const data =
            level === 1
                ? {
                    level: 1,
                    exercise: [
                        { correct: true, english: "cat" },
                        { correct: false, english: "dog" },
                        { correct: false, english: "bird" },
                    ],
                    correct_word: "cat",
                    image_url: "http://127.0.0.1:8000/static\\english_alphabetic_learning_images\\english_level_1_20250321003519.png",
                    question: "Which of these words matches the image?",
                }
                : level === 2
                    ? {
                        level: 2,
                        exercise: { words: ["Ape", "Bee", "Cat", "Dog"], letters: ["A", "B", "C", "D"] },
                        image_url: null,
                        question: "Match the words with the correct letters.",
                    }
                    : level === 3
                        ? {
                            level: 3,
                            exercise: [
                                { correct: false, english: "jump", translation: "jumping" },
                                { correct: true, english: "read", translation: "reading" },
                                { correct: false, english: "write", translation: "writing" },
                            ],
                            correct_word: "read",
                            image_url: "http://127.0.0.1:8000/static\\english_alphabetic_learning_images\\english_level_3_20250321003603.png",
                            question: "Which of these verbs matches the image?",
                        }
                        : "";

        if (level <= 3) {
            setLevel(data.level);
            setQuestion(data.question);
            setExercise(data.exercise);
            setImageUrls(data.image_url ? [data.image_url] : []); // Ensure imageUrls is an array
            setSelectedAnswer(null); // Reset selected answer
            setShowMessage(""); // Reset message
            setIsNextEnabled(false); // Disable "Next" button
        } else if (level > 3) {
            navigate("/eval");
        }
    }, [level]);

    const handleAnswerClick = (ex) => {
        setSelectedAnswer(ex.english); // Track selected answer
        if (ex.correct) {
            setShowMessage("Congrats! You got it right!"); // Show congrats message
            setIsNextEnabled(true); // Enable "Next" button
        } else {
            setShowMessage("Wrong answer. Try again!"); // Show wrong message
            setIsNextEnabled(false); // Disable "Next" button
        }
    };

    const handleLetterSelect = (word, letter) => {
        // Update selected letters
        const updatedLetters = { ...selectedLetters, [word]: letter };
        setSelectedLetters(updatedLetters);
        // Check if all words have been matched with their correct letters
        if (level === 2 && exercise.words && exercise.letters) {
            const allCorrect = exercise.words.every(
                (word, index) => updatedLetters[word] === exercise.letters[index]
            );
            if (allCorrect) {
                setShowMessage("Correct! All words matched.");
                setIsNextEnabled(true);
            } else {
                setShowMessage("Wrong! Some words are mismatched.");
                setIsNextEnabled(false);
            }
        }
    };

    // Shuffle letters for dropdowns
    const shuffleLetters = (letters) => {
        return [...letters].sort(() => Math.random() - 0.5);
    };

    const handleNextClick = () => {
        if (isNextEnabled) {
            setLevel((level) => level + 1);
        }
    };

    return (
        <div>
            <div className="Header">
                <div className="pl-[32px]">
                    <Header />
                </div>
                <img src={cover} alt="Cover" style={{ width: "95px", height: "95px" }} />
            </div>

            <div className="flex flex-col justify-end box-border pl-[32px]">
                <p className="text-start font-roboto font-normal text-[24px]">
                    Welcome <span className="text-amber-300">ريم</span>
                </p>
            </div>

            <div className="mt-[24px] flex flex-col w-full pl-[100px] gap-[16px]">
                <p className="text-start font-roboto not-italic font-normal text-[22px] leading-[28px] text-black">
                    English Test
                </p>
                <p className="text-start font-roboto not-italic font-normal text-[22px] leading-[28px] text-black">
                    Level {level}
                </p>
            </div>

            <div className="flex w-full justify-center mt-[32px]">
                <div className="w-[755px] font-roboto font-normal text-[24px] leading-[32px] flex flex-col items-center justify-center text-[#000000]">
                    <p>{question || "Loading question..."}</p>
                    <div className="mt-[32px] flex flex-row justify-between w-full">
                        {imageUrls.length > 0 ? (
                            imageUrls.map((img, index) => (
                                <img key={index} src={img} alt={`Option ${index + 1}`} style={{ width: "188px", height: "172px" }} />
                            ))
                        ) : (
                            <p>Loading images...</p>
                        )}
                    </div>
                    <div className="mt-[32px] flex flex-row justify-between w-full">
                        {level === 2 && exercise.words && exercise.letters ? (
                            exercise.words.map((word, index) => (
                                <div key={index} className="flex items-center gap-[16px]">
                                    <p>{word}</p>
                                    <select
                                        className="p-[8px] border border-gray-300 rounded"
                                        onChange={(e) => handleLetterSelect(word, e.target.value)}
                                        value={selectedLetters[word] || ""}
                                    >
                                        <option value="" disabled>Select a letter</option>
                                        {shuffleLetters(exercise.letters).map((letter, idx) => (
                                            <option key={idx} value={letter}>
                                                {letter}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            ))
                        ) : (
                            exercise.length > 0 ? (
                                exercise.map((ex, index) => (
                                    <p
                                        key={index}
                                        className={`cursor-pointer ${selectedAnswer === ex.english ? "font-bold" : ""}`}
                                        onClick={() => handleAnswerClick(ex)}
                                    >
                                        {ex.english}
                                    </p>
                                ))
                            ) : (
                                <p>Loading options...</p>
                            )
                        )}
                    </div>
                    {showMessage && <p className={`mt-[16px] text-[20px] ${ showMessage.includes("Congrats!") || showMessage.includes("Correct!") ? "text-green-500":"text-red-600"}`}>{showMessage}</p>}
                </div>
            </div>

            <button
                onClick={handleNextClick}
                className={`mt-[62px] ml-[70%] next-btn ${!isNextEnabled ? "opacity-50 cursor-not-allowed" : ""}`}
                disabled={!isNextEnabled}
            >
                Next
            </button>
        </div>
    );
};

export default AlphabetEn;