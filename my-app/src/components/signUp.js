import React from 'react';
import Header from "./header";
import "./design.css"
const SignUp = () => {
    return (
        <div className={"flex w-[100vw] flex-col justify-center items-center"}>
            <div className={"w-full pt-[20px] pl-[57px]"}>
                <Header/>
            </div>
            <h3 className={"signup_header mt-[100px]"}>
                تسجيل حساب جديد
            </h3>
            <h4 className={"signup_text mt-[16px]"}>
                مرحبًا بك! الرجاء إدخال التفاصيل الخاصة بك لإنشاء حساب جديد.
            </h4>
            <h3 className={"signup_header mt-[48px]"}>
                ما هو اسمك ؟
            </h3>
            <div className={"mt-[32px] Input"}>
                <input className={"outline-0 text-center w-full border-0"} type={"text"} placeholder={"اسم أحد  الوالدين او المدرس "}/>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4L4 12M4 4L12 12" stroke="#1E1E1E" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <button className={"mt-[62px] ml-[640px] next-btn"}>تقدم</button>
        </div>
    );
};

export default SignUp;