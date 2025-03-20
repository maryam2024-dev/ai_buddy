import React, { useState, useEffect } from "react";
import Header from "./header";
import cover from "../assets/img.png";

const Story = () => {
    const [story, setStory] = useState("");
    const [imagePath, setImagePath] = useState("");

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/normal-story/generate?category=Gratitude&size=Short", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setStory(data.story);
                setImagePath(data.image_path);
            })
            .catch((error) => console.error("Error fetching story:", error));
    }, []);

    return (
        <div>
            <div className="Header">
                <div className="pl-[32px]">
                    <Header />
                </div>
                <img src={cover} alt="Cover" style={{ width: "95px", height: "95px" }} />
            </div>

            <div className="flex w-full justify-center mt-[32px]">
                <p className="story">{story || "Loading story..."}</p>
            </div>

            {imagePath && (
                <div className="flex w-full justify-center mt-[16px]">
                    <img src={imagePath} alt="Story Illustration" className="w-[300px] h-auto" />
                </div>
            )}

            <button className="mt-[62px] ml-[70%] next-btn">تقدم</button>
        </div>
    );
};

export default Story;
