import React, { useState, useContext, useEffect } from "react";
import { Link , useLocation} from 'react-router-dom';
import "./BookList.css";
import Navbar from '../Navbar/Navbar';
import Book2 from './Book2';
import { useGlobalContext } from '../../context.';
import { userIdContext } from "../context/userIdContext";

const RecommenderedBooks = () => {
  
  const {BookS} = useContext(userIdContext);
  console.log("zayn")
  return (
    <section className='booklist'>
      <Navbar/>
      <div className='container'>
        <div className='section-title'>
          <h2>Recommendered Books</h2>
        </div>
        <div className='booklist-content grid'>
          {
            BookS.map((item) => {
              return (
                <Book2 itemData={item} />
              )
            })
          }
        </div>
      </div>
    </section>
  )
}

export default RecommenderedBooks