import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import MainPage from "./components/pages/MainPage";
import BookPage from "./components/pages/BookPage";
import { AppProvider } from "./context.";
import AOS from "aos";
import BookList from "./components/BookList/BookList";
import RecommenderedBooks from "./components/BookList/RecommenderedBooks";
import Register from "./components/Register/Register";
import "./assets/css/aos.css";
import "./assets/css/margins-paddings.css";
import headerData from "./data/header.json";
import React, { useState, useEffect } from "react";
import { userIdContext } from "./components/context/userIdContext";

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}
function App() {
  const [data, setData] = useState({});
  const { header } = headerData;
  useEffect(() => {
    AOS.init();
    AOS.refresh();
  }, []);
  const [userId, setuserId] = useState("");
  const [BookS, setBookS] = useState([]);
  return (
    <userIdContext.Provider value={{ userId, setuserId , BookS, setBookS}}>
      <AppProvider>
        <BrowserRouter>
          <ScrollToTop />
          <Routes>
            <Route
              path="/"
              element={<MainPage header={header} name={data} />}
            />
            <Route path="/book" element={<BookPage header={header} />} />
            <Route path="/bookList" element={<BookList />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/RecommenderedBooks"
              element={<RecommenderedBooks />}
            />
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </userIdContext.Provider>
  );
}
/*<div
      className="
      section-wrapper"
    >
      <div id="preLoader"></div>  </div>*/
export default App;
