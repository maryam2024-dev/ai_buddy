import React from 'react';
import Header from "./header";
import cover from "../assets/img.png"
import story from "../assets/img_1.png"
import math from "../assets/img_2.png"
import arabic from "../assets/img_3.png"
import english from "../assets/img_4.png"
import {useNavigate} from "react-router-dom";
const Home = () => {
    const navigate = useNavigate();
    return (
        <div >
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
                <p className={"text-end font-roboto font-normal text-[24px]"}>.....
                    استعد لاستكشاف المعرفة بطريقة ممتعة ومسلية
                </p>
            </div>
            <div className={"pl-[10%] pr-[10%] mt-[24px] flex flex-row justify-between w-full"}>
                <div className={"Card"} onClick={() => navigate("/story")}>
                    <div className={"flex flex-col justify-end items-center p-0 w-[208px] h-[247px] bg-[#E3E3E3]"}>
                        <img style={{width:"174px", height:"174px"}} src={story} alt={""}/>
                    </div>
                    <p className={"text-center w-full"}>
                        قصص تعليميه
                    </p>
                    <p className={"text-center"}>
                        📚 قصة قبل النوم استمع إلى حكايات هادئة تساعدك
                        على النوم براحة.
                    </p>
                </div>
                <div className={"Card"}>
                    <div className={"flex flex-col justify-end items-center p-0 w-[208px] h-[247px] bg-[#E3E3E3]"}>
                        <img style={{width:"174px", height:"174px", marginBottom:"8px"}} src={math} alt={""}/>
                    </div>
                    <p className={"text-center w-full"}>
                        تعلم الرياضيات
                    </p>
                    <p className={"text-center"}>
                        استكشف الأرقام وتعلم العد من
                        خلال الألعاب المسلية</p>
                </div>
                <div className={"Card"} onClick={() => navigate("/alphabet-ar")}>
                    <div className={"flex flex-col justify-end items-center p-0 w-[208px] h-[247px] bg-[#E3E3E3]"}>
                        <img style={{width:"174px", height:"174px", marginBottom:"8px"}} src={arabic} alt={""}/>
                    </div>
                    <p className={"text-center"}> اكتشف الحروف العربية مع النطق والتمارين الممتعة!</p>
                </div>
                <div className={"Card"} onClick={() => navigate("/alphabet-en")}>
                    <div className={"flex flex-col justify-end items-center p-0 w-[208px] h-[247px] bg-[#E3E3E3]"}>
                        <img style={{width:"174px", height:"174px", marginBottom:"8px"}} src={english} alt={""}/>
                    </div>
                    <p className={"text-center"}>تعلم الحروف الإنجليزية بطريقة سهلة وتفاعلية!  </p>
                </div>
            </div>
        </div>
    );
};

export default Home;