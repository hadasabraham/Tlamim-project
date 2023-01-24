import React from "react";
import './Header.css'

const onCandidates = () => {
    window.location.href = 'http://localhost:3000';
}

const onAddStage = () => {
    window.location.href = 'http://localhost:3000/addStages';
};


const Header = (title) => {
    return (
        <div style={{ display: "grid", gridTemplateColumns: "8fr 1fr" }}>

            <div className = "Header" >
                <a>{title}</a>
            </div >

            <div className="Menu" >
                <a onClick={onCandidates}>מועמדים</a>
                <> | </>
                <a onClick={onAddStage}>הוספת שלב</a>
            </div>
        </div>
    );
};

export default Header;