import { default as React, useState } from "react";
import { Navbar } from "react-bootstrap";
import { Link } from "react-scroll";
import { useNavigate } from 'react-router-dom';
import { siteLogo } from "../../global";
import { Navigate } from "react-router-dom";

const Header = ({ header }) => {
  const [fix, setFix] = useState(false);
  const navigate = useNavigate();
function handleClick(link){
  
navigate(link);
}
  function SetFixed() {
    if (window.scrollY >= 100) {
      setFix(true);
    } else {
      setFix(false);
    }
  }
  window.addEventListener("scroll", SetFixed);
  return (
    <header className={fix ? "header navbar_fixed" : "header"}>
      <div className="container">
        <div className="row">
          <Navbar bg="none" expand="lg">
            <a className="navbar-brand" href="/">
              <img src="../assets/images/siteLogo.jpg" alt={siteLogo.alt} style={{height : "45px"}}/>
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
                {header.menu?.map((data, i) => (
                  
                    // <Link
                    
                    //   activeClass="active"
                    //   className="benefits nav-link"
                    //   to={`${data.link}`}
                    //   spy={true}
                    //   isDynamic={false}
                    //   hashSpy={false}
                    //   spyThrottle={500}
                    //   smooth={true}
                    //   duration={500}
                    //   offset={-60}
                    // >
                      <li className="nav-item" key={i} onClick={() => handleClick(data.link)}>{data.title}</li>
                    // </Link>
                  
                ))}
              </ul>
            </Navbar.Collapse>
          </Navbar>
        </div>
      </div>
    </header>
  );
};

export default Header;
