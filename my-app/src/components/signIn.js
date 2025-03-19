import React, { useState } from 'react';
import Header from "./header";
import "./design.css";
import {useNavigate} from "react-router-dom";

const SignIp = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    return (
        <div className={"box-border flex flex-col justify-center items-center"}>
            <div className={"w-full box-border pt-[20px] pl-[57px]"}>
                <Header />
            </div>
            <h3 className={"signup_header mt-[100px]"}>
                تسجيل الدخول
            </h3>
            <h4 className={"signup_text mt-[16px]"}>
                مرحبًا بعودتك! الرجاء إدخال التفاصيل الخاصة بك.
            </h4>
            <h3 className={"signup_header mt-[48px]"}>
                ما هو الايميل الخاص بك؟
            </h3>
            <div className={"mt-[32px] Input"}>
                <input
                    className={"outline-0 text-center w-full border-0"}
                    type={"text"}
                    placeholder={"الايميل"}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <svg onClick={() => setEmail("")} width="16" height="16" viewBox="0 0 16 16" fill="none"
                     xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4L4 12M4 4L12 12" stroke="#1E1E1E" strokeWidth="1.6" strokeLinecap="round"
                          strokeLinejoin="round"/>
                </svg>
            </div>
            <h3 className={"signup_header mt-[48px]"}>
                ما هو كلمه السر ؟
            </h3>
            <div className={"mt-[32px] Input"}>
                <input
                    className={"outline-0 text-center w-full border-0"}
                    type="password"
                    placeholder={"كلمة السر"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <svg onClick={() => setPassword("")} width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4L4 12M4 4L12 12" stroke="#1E1E1E" strokeWidth="1.6" strokeLinecap="round"
                          strokeLinejoin="round"/>
                </svg>
            </div>

            <button onClick={() => navigate("/home")} className={"mt-[62px] ml-[640px] next-btn"}>
                الدخول
            </button>
            <div className={"h-8 w-[20px]"}>

            </div>
        </div>
    );
};

export default SignIp;