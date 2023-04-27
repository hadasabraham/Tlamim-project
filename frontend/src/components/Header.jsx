import React from "react";
import './Header.css'
import Button from '@mui/joy/Button';
import Popup from 'reactjs-popup';


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
            
            <div className="MenuHolder">
                <Popup trigger=
                    {<a className="Header" onClick={onCandidates}>|||</a>}
                    position="bottom right">
                    {
                    close => (
                        <div className="Menu">
                            <div>
                                <a onClick={onCandidates}>מועמדים</a>

                            </div>
                            <div>
                                --------------
                            </div>
                            <div>
                            <a onClick={onAddStage}>הוספת שלב</a>
                            </div>
                        </div>
                    )
                }
                </Popup>
                
            </div>
        </div>
    );
};

export default Header;