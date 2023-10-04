import React, { useState, useContext, useEffect } from "react";
import { useCallback } from "react";
import { userIdContext } from "./components/context/userIdContext";

//import { useNavigate } from "react-router-dom";
const URL = "https://openlibrary.org/search.json?title=";
const AppContext = React.createContext();

const AppProvider = ({ children }) => {
  const [searchTerm, setSearchTerm] = useState("the lost world");
  const [books, setBooks] = useState([]);
  const [books2, setBooks2] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resultTitle, setResultTitle] = useState("");
  //const {email} = useContext(emailContext)
  //const { userId } = useContext(userIdContext);
  //let {BookS, setBookS} = useContext(userIdContext);
  // Now you can use the email variable in this component

  // This will print the updated email whenever it changes
  //console.log("UserId:", userId);

  //const navigate = useNavigate();

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`${URL}${searchTerm}`);
      const data = await response.json();

      const { docs } = data;
      console.log(docs);
      if (docs) {
        const newBooks = docs.slice(0, 20).map((bookSingle) => {
          const {
            key,
            author_name,
            cover_i,
            edition_count,
            first_publish_year,
            title,
          } = bookSingle;

          return {
            id: key,
            author: author_name,
            cover_id: cover_i,
            edition_count: edition_count,
            first_publish_year: first_publish_year,
            title: title,
          };
        });

        setBooks(newBooks);

        if (newBooks.length > 1) {
          setResultTitle("Your Search Result");
        } else {
          setResultTitle("No Search Result Found!");
          console.log("kkkk");
        }
      } else {
        setBooks([]);
        setResultTitle("No Search Result Found!");
      }
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  }, [searchTerm]);

  // const handleClick = async () => {
  //   try {
  //     const requestBody = { userId };
  //     const response = await fetch("/recommend", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify(requestBody),
  //     });
  //     //console.log("anythongmygb")
  //     console.log("Response status:", response.status);

  //     if (!response.ok) {
  //       throw new Error("Network response was not ok");
  //     }

  //     const data = await response.json();
      
  //     console.log("Response:", data);
  //     setBookS(data)
  //     console.log(BookS);
  //     //navigate("/RecommenderedBooks");
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  useEffect(() => {
    fetchBooks();
  }, [searchTerm, fetchBooks]);

  // useEffect(() => {
  //   handleClick();
  // }, [userId]);
  return (
    <AppContext.Provider
      value={{
        loading,
        books,
        setSearchTerm,
        resultTitle,
        setResultTitle,
        books2,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useGlobalContext = () => {
  return useContext(AppContext);
};

export { AppContext, AppProvider };
