import React, { useState, useContext, useEffect } from "react";
import data from "../data/hero.json";
import MailchimpSubscribe from "react-mailchimp-subscribe";
import { useNavigate } from "react-router-dom";
import { emailContext, userIdContext } from "./context/userIdContext";

export function SubscribeForm({}) {
  const [ email, setEmail ] = useState("");
  const { userId, setuserId } = useContext(userIdContext);
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleClick(link) {
    navigate(link);
  }
  const login = async () => {
    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      //console.log(password)
      setuserId(data.id)
      console.log("Response:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    login();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <input
          className="heroInput"
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          placeholder="Your Email"
        />
        <p className="z">-zz</p>
        <input
          className="heroInput"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          placeholder="Your Password"
        />
        <button type="submit" className="" id="sub">
          <span>subscribe</span>
        </button>
        <p></p>
        <span className="r">
          if you do not have an acoount, please register
        </span>
        <button
          type="submit"
          className="rr"
          onClick={() => handleClick("/register")}
        >
          <span>sign up</span>
        </button>
      </div>
    </form>
  );
}

const Hero = ({ isBg }, { data1 }) => {
  const { herov1 } = data;
  console.log(data1?.message);
  return (
    <section
      id="hero"
      className={`hero hero__padding overflow-hidden position-relative ${
        isBg === "yes" ? "bg-one" : ""
      }`}
    >
      <div className="circle x1"></div>
      <div className="circle x2"></div>
      <div className="circle x3"></div>
      <div className="circle x4"></div>
      <div className="circle x5"></div>
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-6 m-0px-b md-m-30px-b">
            <div className="hero__content position-relative">
              <div className="badge-text mb-2 text-uppercase">
                {herov1.subtitle}
              </div>
              <h1 className="display-4 mb-4 text-capitalize">{herov1.title}</h1>
              <p className="text-muted mb-5 fs-5">{herov1.description}</p>
              <MailchimpSubscribe
                render={({ subscribe, status, message }) => (
                  <SubscribeForm
                    name={data1}
                    status={status}
                    message={message}
                    onValidated={(formData) => subscribe(formData)}
                  />
                )}
              />
            </div>
          </div>
          <div className="col-lg-6">
            <div className="hero__images text-center">
              <img className="img-fluid" src={herov1.image} alt="" />
              <div className="hero__images--badge">
                <span>
                  <span className="hero__images--badge--text1">
                    {herov1.tagTitle}
                  </span>
                  <span className="hero__images--badge--text2">
                    {herov1.tagText}
                  </span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
