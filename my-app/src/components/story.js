import React from 'react';
import Header from "./header";
import cover from "../assets/img.png";
const Story = () => {
    return (
        <div>
            <div className={"Header"}>
                <div className={"pl-[32px]"}>
                    <Header />
                </div>
                <img src={cover} alt="" style={{width:"95px", height:"95px"}}/>
            </div>

            <div className={"flex w-full justify-center mt-[32px]"}>
                <p className={"story"}>
                    Once upon a time, in a small village, lived a kind little boy named Omar.
                    He always helped others and shared what he had
                    One day, Omar saw an old man struggling to carry a heavy bag. Without hesitation, he ran to help him.
                </p>
            </div>
            <button className={"mt-[62px] ml-[70%] next-btn"}>تقدم</button>
        </div>
    );
};

export default Story;