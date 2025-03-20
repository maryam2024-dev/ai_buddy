import React from 'react';
import "./design.css"
import Header from "./header";
import robot from "../assets/WhatsApp Image 2025-03-16 at 10.05.38 PM.jpeg"
import {useNavigate} from "react-router-dom";

const Splash = () => {
    const navigate = useNavigate();
    const logIn = () => {
        navigate("/signin");
    }
    const signUp = () => {
        navigate("/signup");
    }
    return (
        <div>
            <div className={"header"}>
                <Header />
                <div className={"flex flex-row gap-[47px] h-[119px] align-top"}>
                    <button className={"sign-btn"} onClick={signUp}>
                        التسجيل
                    </button>
                    <button className={"sign-btn"} onClick={logIn}>
                        الدخول
                    </button>
                </div>
            </div>
            <div className={"flex flex-row justify-between"}>
                <div>
                    <img className={"w-[343px] h-[436px] pt-[40px]"} src={robot} alt="sss"/>
                </div>
                <div className={"flex flex-col pr-[120px] max-w-[60%] text-end"}>
                    <h4 className={"about"}>
                        :
                        نبذة عن الموقع
                    </h4>
                    <p className={"info pr-[16px]"}><br/>
                        يهدف هذا الموقع إلى تطوير تجربة تعليمية مبتكرة للأطفال باستخدام الذكاء الاصطناعي التوليدي (GenAI) لإنشاء تمارين رياضية، أنشطة لتعلم الحروف، وقصص تفاعلية ذات مغزى باللغتين العربية والإنجليزية. سيركز النظام على تقديم قصص أخلاقية تفاعلية تساعد الأطفال على تعلم القيم المهمة مثل الصدق، اللطف، والصبر بطريقة ممتعة وجذابة.
                    </p>
                    <h4 className={"about"}><br/>
                        :
                        الميزات الأساسية

                    </h4>
                    <p className={"info"}><br/>
                        - إنشاء محتوى تعليمي بالذكاء الاصطناعي: تمارين رياضية، أنشطة لتعلم الحروف، وقصص تفاعلية.<br/>
                        - تقييم تفاعلي وتحفيزي: ألعاب تعليمية، مكافآت، وتشجيع مستمر.
                        <br/>- دعم ثنائي اللغة (العربية والإنجليزية): يساعد الأطفال على إتقان اللغتين بسهولة.
                        <br/>- تفاعل مع الذكاء الاصطناعي: يمكن للأطفال طرح الأسئلة، تلقي التلميحات، والمشاركة في صياغة القصة.
                    </p>
                    <h4 className={"about"}><br/>
                        :
                        الرؤية

                    </h4>
                    <p className={"info"}><br/>
                        يسعى هذا المشروع إلى دمج التكنولوجيا بالتعليم لجعل التعلم أكثر متعة، تفاعلية، وذات معنى، مما يساعد الأطفال على اكتساب مهارات أكاديمية وأخلاقية تؤهلهم للمستقبل.
                    </p>
                </div>

            </div>
            <div className={"flex justify-end pr-[82px]"}>
                <button className={"start"} onClick={signUp}>!
                    هيا بنا لنبدأ
                </button>
            </div>
        </div>
    );
};

export default Splash;