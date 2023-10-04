//import bgImg from '../assets/img1.jpg';
import { useForm } from 'react-hook-form';
import './Register.css';
import axios from 'axios';
import Navbar from "../Navbar/Navbar";
import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from "react";

export default function Register() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const navigate = useNavigate();
  function handleClick2(link){
    
    navigate(link);
    }
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
    
    <section className='b w-100'>
      <Navbar bg="none" expand="lg">
            <a className="navbar-brand" href="/">
              <img src="../assets/images/siteLogo.jpg" alt="" style={{height : "55px"}}/>
            </a>
            <Navbar.Toggle aria-controls="navbarSupportedContent">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </Navbar.Toggle>
            <Navbar.Collapse id="navbarSupportedContent">
              <ul className="navbar-nav menu ms-lg-auto">
                
                      <li className='homeButton'  onClick={() => handleClick2('/')} style={{backgroundColor : "black"}}>Home</li>
                   
              </ul>
            </Navbar.Collapse>
          </Navbar>
      <div className='row'>

        <div className="col-6 register">
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
        <div className="col-6">
          <img src='../assets/images/download.jpeg' alt="" className='mg' />
        </div>
      </div>

    </section>
  )
};