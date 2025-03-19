import React from 'react';
import Header from "./header";
import cover from "../assets/img.png";
import giraffe from "../assets/img_5.png"
import elephant from "../assets/img_6.png"
import parrot from "../assets/img_7.png"
import {useNavigate} from "react-router-dom";
const AlphabetEn = () => {
    const navigate = useNavigate();
    return (
        <div>
            <div className={"Header"}>
                <div className={"pl-[32px]"}>
                    <Header />
                </div>
                <img src={cover} alt="" style={{width:"95px", height:"95px"}}/>
            </div>
            <div className={"flex flex-col justify-end box-border pl-[32px]"}>
                <p className={"text-start font-roboto font-normal text-[24px]"}>
                    Welcome <span className={"text-amber-300"}>ريم</span>
                </p>
            </div>
            <div className={"mt-[24px]  flex flex-col w-full pl-[100px] gap-[16px]"}>
                <p className={"text-start font-roboto not-italic font-normal text-[22px] leading-[28px] text-black"}>
                    English Test
                </p>
                <p className={"text-start font-roboto not-italic font-normal text-[22px] leading-[28px] text-black"}>
                    level 1
                </p>
            </div>
            <div className={"flex w-full justify-center mt-[32px]"}>
                <div className={"w-[755px] font-roboto font-normal text-[24px] leading-[32px] flex flex-col items-center justify-center text-[#000000]"}>
                    <p>
                        Which of this animals start with letter E?
                    </p>
                    <div className={"mt-[32px] flex flex-row justify-between w-full"}>
                        <img src={giraffe} style={{width:"188px", height:"172px"}}/>
                        <img src={elephant} style={{width:"188px", height:"172px"}}/>
                        <img src={parrot} style={{width:"188px", height:"172px"}}/>
                    </div>
                </div>
            </div>
            <button onClick={() => navigate("eval")} className={"mt-[62px] ml-[70%] next-btn"}>next</button>
        </div>
    );
};

export default AlphabetEn;