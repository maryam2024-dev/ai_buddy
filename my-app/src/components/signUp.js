import React, { useState } from 'react';
import Header from "./header";
import "./design.css";
import boy from "../assets/img_8.png";
import girl from "../assets/img_9.png";
import {useNavigate} from "react-router-dom";
const SignUp = () => {
    const [state, setState] = useState(0);
    const [name, setName] = useState("");
    const [kidName, setKidName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [gender, setGender] = useState("")
    const navigate = useNavigate();

    const info = [
        {
            title: "ما هو اسمك ؟",
            placeholder: "اسم أحد الوالدين او المدرس",
            value: name,
            setValue: setName
        },
        {
            title: "ما هو اسم طفلك ؟",
            placeholder: "اسم الطفل",
            value: kidName,
            setValue: setKidName
        },
        {
            title: "عنوان البريد الإلكتروني",
            placeholder: "عنوان البريد الإلكتروني للوصي",
            value: email,
            setValue: setEmail
        },
        {
            title: "كلمة المرور",
            placeholder: "كلمة المرور",
            value: password,
            setValue: setPassword
        },
        {
            title: "تأكيد كلمة المرور",
            placeholder: "تأكيد كلمة المرور",
            value: confirmPassword,
            setValue: setConfirmPassword
        },
        {
            title: "ما هو جنس طفلك؟",
            placeholder: "",
            value: confirmPassword,
            setValue: setConfirmPassword
        }
    ];

    const handleNext = () => {
        if (state < info.length - 1) {
            if (state === 3)
                setState(state => state +2);
            else
                setState(state + 1);
        } else {
            // Handle form submission here
            if (password !== confirmPassword) {
                alert("كلمة المرور وتأكيدها غير متطابقين");
                return;
            }
            // You can now send the data to your backend or handle it as needed
            console.log({
                name,
                kidName,
                email,
                password
            });
            navigate("/home")
        }
    };

    const handleInputChange = (state, e) => {
        info[state].setValue(e.target.value);
    };
    const handleClear = (state) => {
        info[state].setValue("");
    };

    return (
        <div className={"box-border flex flex-col justify-center items-center"}>
            <div className={"w-full box-border pt-[20px] pl-[57px]"}>
                <Header />
            </div>
            <h3 className={"signup_header mt-[100px]"}>
                تسجيل حساب جديد
            </h3>
            <h4 className={"signup_text mt-[16px]"}>
                مرحبًا بك! الرجاء إدخال التفاصيل الخاصة بك لإنشاء حساب جديد.
            </h4>
            <h3 className={"signup_header mt-[48px]"}>
                {info[state].title}
            </h3>
            {state !== 5 && <div className={"mt-[32px] Input"}>
                <input
                    className={"outline-0 text-center w-full border-0"}
                    type={state === 3 || state === 4 ? "password" : "text"}
                    placeholder={info[state].placeholder}
                    value={info[state].value}
                    onChange={(e) => handleInputChange(state, e)}
                />
                <svg onClick={() => handleClear(state)} width="16" height="16" viewBox="0 0 16 16" fill="none"
                     xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4L4 12M4 4L12 12" stroke="#1E1E1E" strokeWidth="1.6" strokeLinecap="round"
                          strokeLinejoin="round"/>
                </svg>
            </div>}
            {
                state === 5 && <div className={"mt-[32px] flex flex-row gap-[148px]"}>
                    <img src={boy} onClick={()=> setGender("boy")} className={"w-[204px] h-[204px] cursor-pointer"}/>
                    <img src={girl} onClick={()=> setGender("girl")} className={"w-[204px] h-[204px] cursor-pointer"}/>
                </div>
            }
            {
                state === 3 && (
                    <>
                        <h3 className={"signup_header mt-[48px]"}>
                            {info[4].title}
                        </h3>
                        <div className={"mt-[32px] Input"}>
                            <input
                                className={"outline-0 text-center w-full border-0"}
                                type="password"
                                placeholder={info[4].placeholder}
                                value={info[4].value}
                                onChange={(e) => handleInputChange(4,e)}
                            />
                            <svg onClick={() => handleClear(4)} width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 4L4 12M4 4L12 12" stroke="#1E1E1E" strokeWidth="1.6" strokeLinecap="round"
                                      strokeLinejoin="round"/>
                            </svg>
                        </div>
                    </>
                )
            }
            <button className={"mt-[62px] ml-[640px] next-btn"} onClick={handleNext}>
                {state < info.length - 1 ? "تقدم" : "سجل"}
            </button>
            {state > 2 && <div className={"h-8 w-[20px]"}>

            </div>}
        </div>
    );
};

export default SignUp;