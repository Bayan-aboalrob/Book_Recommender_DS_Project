import React, { useState, useContext, useEffect } from "react";
import Navbar from "../Navbar/Navbar";
//import SearchForm from "../SearchForm/SearchForm";
import "./Header2.css";
import SearchForm from '../SearchForm/SearchForm';
import { useNavigate } from 'react-router-dom';
//import Header from '../global/Header';
import { userIdContext } from "../context/userIdContext";
//import RecommenderedBooks from '../BookList/RecommenderedBooks';
const Header2 = () => {
  //const {zYes, setzYes} = useState([]);
  const navigate = useNavigate();
  function handleClick2(link){
    
    navigate(link);
    }
  const {setBookS} = useContext(userIdContext);
  const { userId } = useContext(userIdContext);
  const handleClick = async () => {
    try {
      const requestBody = { userId };
      const response = await fetch("/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });
      //console.log("anythongmygb")
      console.log("Response status:", response.status);

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      
      console.log("Response:", data);
      setBookS(data)
      navigate("/RecommenderedBooks");
    } catch (error) {
      console.error("Error:", error);
    }
  };
  return (
    <div className='holder'>
        <header className='header'>
        <div className="container">
        <div className="row">
          <Navbar bg="none" expand="lg">
            <a className="navbar-brand" href="/">
              <img src="../assets/images/siteLogo.jpg" alt="" style={{height : "45px"}}/>
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
        </div>
      </div>
            <div className='header-content flex flex-c text-center text-white' style={{margin: '0px auto', padding: '1px', color: 'white', backgroundColor: "#f5ebe6"}}>
              <div style={{marginTop : '120px'}}>
              <h2 className='find'>Find your book of <span className="choice">choice.</span></h2><br />
              <p className="ifYou">If you would like to see the recommended books</p>
              <button className = "reco" onClick={() => handleClick('/RecommenderedBooks')}>Recommended Books</button>
              {/* <Link to={{ pathname: '/RecommenderedBooks', state: { zYes } }}>
              </Link> */}
              <SearchForm/>
              </div>
               
            </div>
        </header>
    </div>
  )
}


                

export default Header2