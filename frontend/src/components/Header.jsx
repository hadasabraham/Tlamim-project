import React from "react";
import './Header.css'

const Header = (title) => {
    return (
        <div className = "Header" >
            <a>{title}</a>
        </div >
    );
};

export default Header;