import React, {useEffect, useState} from 'react';
import Header from "./header";
import cover from "../assets/img.png";
import giraffe from "../assets/img_5.png"
import elephant from "../assets/img_6.png"
import parrot from "../assets/img_7.png"
import {useNavigate} from "react-router-dom";
const Alphabet = () => {
    const navigate = useNavigate();

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
                    exercise: [{"correct":true,"arabic":"كلب","english":"dog"},{"correct":false,"arabic":"قطة","english":"cat"},{"correct":false,"arabic":"دجاجة","english":"chicken"}],
                    correct_word: "cat",
                    image_url: "http://127.0.0.1:8000/static\\english_alphabetic_learning_images\\english_level_1_20250321003519.png",
                    question: "أي من هذه الكلمات تطابق الصورة؟",
                }
                : level === 2
                    ? {
                        level: 2,
                        exercise: { words:["كتاب","نوم","ماء","سما"], "letters":["ك","ن","م","س"] },
                        image_url: null,
                        question: "طابق الكلمات مع الحروف الصحيحة.",
                    }
                    : level === 3
                        ? {
                            level: 3,
                            exercise: [{"correct":true,"arabic":"يأكل","english":"eating"},{"correct":false,"arabic":"يغني","english":"singing"},{"correct":false,"arabic":"يقرأ","english":"reading"}],
                            correct_word: "read",
                            image_url: "http://127.0.0.1:8000/static\\english_alphabetic_learning_images\\english_level_3_20250321003603.png",
                            question: "أي من هذه الأفعال يناسب الصورة؟",
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
        setSelectedAnswer(ex.arabic); // Track selected answer
        if (ex.correct) {
            setShowMessage("عمل رائع اجابه صحيحه"); // Show congrats message
            setIsNextEnabled(true); // Enable "Next" button
        } else {
            setShowMessage("اعد المحاوله اجابه خطأ"); // Show wrong message
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
                setShowMessage("عمل رائع كل الاجابات صحيحه");
                setIsNextEnabled(true);
            } else {
                setShowMessage("اعد المحاوله بعض الاجابات خطأ");
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
            <div className={"Header"}>
                <div className={"pl-[32px]"}>
                    <Header />
                </div>
                <img src={cover} alt="" style={{width:"95px", height:"95px"}}/>
            </div>
            <div className={"flex flex-col justify-end box-border pr-[32px]"}>
                <p className={"text-end font-roboto font-normal text-[24px]"}>
                    مرحبًا <span className={"text-amber-300"}>ريم</span>
                </p>
            </div>
            <div className={"mt-[24px] w-full flex flex-col pr-[100px] gap-[16px]"}>
                <p className={"text-end font-roboto not-italic font-normal text-[22px] leading-[28px] text-black"}>
                    اختبار اللغة العربية
                </p>
                <p className={"text-end font-roboto not-italic font-normal text-[22px] leading-[28px] text-black"}>
                    المستوي {level === 1? "الاول" : level === 2? "الثاني" : "الثالث"  }
                </p>
            </div>
            <div className={"flex w-full justify-center mt-[32px]"}>
                <div className={"w-[755px] font-roboto font-normal text-[24px] leading-[32px] flex flex-col items-center justify-center text-[#000000]"}>
                    <p>
                        {question}
                    </p>
                    <div className="mt-[32px] flex flex-row justify-between w-full">
                        {imageUrls.length > 0 ? (
                            imageUrls.map((img, index) => (
                                <img key={index} src={img} alt={`Option ${index + 1}`} style={{ width: "188px", height: "172px" }} />
                            ))
                        ) : (
                            <p>جاري التحميل...</p>
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
                                        <option value="" disabled>اختر حرفا</option>
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
                                        className={`cursor-pointer ${selectedAnswer === ex.arabic ? "font-bold" : ""}`}
                                        onClick={() => handleAnswerClick(ex)}
                                    >
                                        {ex.arabic}
                                    </p>
                                ))
                            ) : (
                                <p>جاري التحميل...</p>
                            )
                        )}
                    </div>
                    {showMessage && <p className={`mt-[16px] text-[20px] ${ showMessage.includes("صحيحه")? "text-green-500":"text-red-600"}`}>{showMessage}</p>}
                </div>
            </div>
            <button
                onClick={handleNextClick}
                className={`mt-[62px] ml-[70%] next-btn ${!isNextEnabled ? "opacity-50 cursor-not-allowed" : ""}`}
                disabled={!isNextEnabled}
            >
                تقدم
            </button>
            {/*<button onClick={() => navigate("/eval")} className={"mt-[62px] ml-[70%] next-btn"}></button>*/}
        </div>
    );
};

export default Alphabet;