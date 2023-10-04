//import bgImg from '../assets/img1.jpg';
import { useForm } from 'react-hook-form';
import './Register.css';
import axios from 'axios';
import React, { useState, useEffect } from "react";

export default function Register() {
    const { register, handleSubmit, watch, formState: { errors } } = useForm();
    const sendPostRequest = async (data) => {
        try {
          const response = await axios.post('http://localhost:5000/register', {
            
            "email": data.username,
            "password": data.password
          });
      
        console.log('Response:', response.data);
        } catch (error) {
          console.error('Error:', error);
        }
      };
      const onSubmit = (data) => {
        sendPostRequest(data);
        console.log(data)
      };
    
    
    
    
       

    // console.log(watch('username'));
    
  return (
    <section className='.b'>
        <div className="register">
            <div className="col-1">
                <h2>Sign Up</h2>
                <span>register and enjoy the service</span>

                <form id='form' className='flex flex-col' onSubmit={handleSubmit(onSubmit)}>
                    <input type="text" {...register("username")} placeholder='username' />
                    <input type="text" {...register("password")} placeholder='password' />
                    {errors.mobile?.type === "required" && "Mobile Number is required"}
                    {errors.mobile?.type === "maxLength" && "Max Length Exceed"}
                    <button className='btn'>Sign Up</button>
                </form>

            </div>
            <div className="col-2">
                <img src='../assets/images/Wallpaper.jpeg' alt="" className='.mg'/>
            </div>
        </div>
    </section>
  )
};
