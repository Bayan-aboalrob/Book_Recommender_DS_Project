import React from "react";
import Header from '../global/Header';
import Hero from '../hero';
const MainPage = ({header}, {data}) => {
    return(
        <>
        <Header header= {header}/>
        <Hero isBg='yes' name = {data}/>
        </>
        
    )
}

export default MainPage;