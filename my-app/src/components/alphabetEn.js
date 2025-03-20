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
    const [correctWord, setCorrectWord] = useState("");
    const [imageUrls, setImageUrls] = useState([]); // Ensure it's an array from the start

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/alpabet-eng/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ level: 1 }),
        })
            .then((response) => response.json())
            .then((data) => {
                setLevel(data.level);
                setQuestion(data.question);
                setExercise(data.exercise);
                setCorrectWord(data.correct_word);

                // ✅ Ensure imageUrls is an array
                const images = Array.isArray(data.image_url) ? data.image_url : [data.image_url];
                setImageUrls(images);
            })
            .catch((error) => console.error("Error fetching exercise:", error));
    }, []);

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
                </div>
            </div>

            <button onClick={() => navigate("/eval")} className="mt-[62px] ml-[70%] next-btn">
                Next
            </button>
        </div>
    );
};

export default AlphabetEn;
