import React from 'react';
import Header from "./header";
import cover from "../assets/img.png";
import middal from "../assets/img_10.png"
const Evaluation = () => {
    return (
        <div className={"pb-[100px]"}>
            <div className={"Header"}>
                <div className={"pl-[32px]"}>
                    <Header />
                </div>
                <img src={cover} alt="" style={{width:"95px", height:"95px"}}/>
            </div>
            <div className={"flex flex-col justify-end box-border pr-[32px]"}>
                <p className={"text-end font-roboto font-normal text-[24px]"}>
                    مرحبًا  <span className={"text-amber-300"}>ريم</span>
                </p>
            </div>
            <div className={"mt-[24px] pl-[32px] flex flex-col w-full pr-[100px] gap-[16px]"}>
                <p className={"text-start font-roboto not-italic font-normal text-[22px] leading-[28px] flex items-center text-black"}>
                    level 1
                </p>

            </div>
            <div className={"mt-[48px] gap-4 flex flex-col justify-center items-center"}>
                <p className={"success"}>
                    You are amazing! 🌟 You got most of the answers right!
                    💡 Keep trying, you are smart and hardworking.
                    Next time, you’ll be the star of the class! ⭐🎉
                </p>
                <svg width="99" height="92" viewBox="0 0 99 92" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M67.7531 91.1375C55.8422 94.0125 50.7375 88.2625 50.7375 88.2625C50.7375 88.2625 51.6656 79.35 63.7312 76.475C71.9297 74.4625 87.3984 78.4875 87.3984 78.4875C87.3984 78.4875 75.9516 89.125 67.7531 91.1375Z" fill="#83BF4F"/>
                    <path d="M32.4844 83.375C44.3953 86.25 49.5 80.5 49.5 80.5C49.5 80.5 48.5719 71.5875 36.5062 68.7125C28.3078 66.7 12.8391 70.725 12.8391 70.725C12.8391 70.725 24.2859 81.3625 32.4844 83.375Z" fill="#83BF4F"/>
                    <path d="M49.5 40.25V92" stroke="#75A843" />
                    <path d="M77.8078 28.175C70.2281 35.2187 54.6047 40.25 51.975 37.95C49.5 35.65 54.7594 20.9875 62.4938 13.9437C73.1672 4.02499 88.4813 18.2562 77.8078 28.175Z" fill="#FFD68D"/>
                    <path d="M21.1922 52.325C28.7719 45.2812 44.3953 40.25 47.025 42.55C49.5 44.85 44.086 59.3687 36.5063 66.5562C25.8328 76.475 10.5188 62.2437 21.1922 52.325Z" fill="#FFD68D"/>
                    <path d="M62.4938 66.5562C54.9141 59.5125 49.5 44.9937 51.975 42.55C54.45 40.25 70.2282 45.1375 77.8079 52.325C88.4813 62.2437 73.1672 76.475 62.4938 66.5562Z" fill="#FFD68D"/>
                    <path d="M36.5063 13.9437C44.086 20.9875 49.5 35.5062 47.025 37.95C44.55 40.25 28.7719 35.2187 21.1922 28.175C10.5188 18.2562 25.8328 4.02499 36.5063 13.9437Z" fill="#FFD68D"/>
                    <path d="M78.7359 50.3125C67.9078 50.3125 53.0578 43.5562 53.0578 40.25C53.0578 36.9437 67.9078 30.1875 78.7359 30.1875C93.8953 30.1875 93.8953 50.3125 78.7359 50.3125Z" fill="#FFE9AB"/>
                    <path d="M20.2641 30.1875C31.0922 30.1875 45.9422 36.9437 45.9422 40.25C45.9422 43.5562 31.0922 50.3125 20.2641 50.3125C5.10469 50.3125 5.10469 30.1875 20.2641 30.1875Z" fill="#FFE9AB"/>
                    <path d="M38.6719 67.4187C38.6719 57.3562 45.9422 43.5562 49.5 43.5562C53.0578 43.5562 60.3281 57.3562 60.3281 67.4187C60.3281 81.5062 38.6719 81.5062 38.6719 67.4187Z" fill="#FFE9AB"/>
                    <path d="M60.3281 13.0812C60.3281 23.1437 53.0578 36.9437 49.5 36.9437C45.9422 36.9437 38.6719 23.1437 38.6719 13.0812C38.6719 -1.00625 60.3281 -1.00625 60.3281 13.0812Z" fill="#FFE9AB"/>
                    <path d="M49.5 54.05C57.7015 54.05 64.35 47.8715 64.35 40.25C64.35 32.6285 57.7015 26.45 49.5 26.45C41.2986 26.45 34.65 32.6285 34.65 40.25C34.65 47.8715 41.2986 54.05 49.5 54.05Z" fill="#F29A2E"/>
                </svg>
                <p className={"success"}>
                    Amazing ,you earned  the H letter bage ⭐🎉
                </p>
                <img src={middal} className={"w-[339px] h-[310px]"}/>
            </div>

        </div>
    );
};

export default Evaluation;