import React from 'react';
//import LoaderImg from "../../images/loader.svg";
import "./Loading.css";

const Loading = () => {
  const LoaderImg = "../images/loader.svg"
  return (
    <div style={{marginTop : '200px' , marginLeft : '600px'}}>
      <img src = '../assets/images/loader.svg' alt = "loader" />
    </div>
  )
}

export default Loading