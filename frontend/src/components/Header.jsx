import React from "react";
import Button from '@mui/joy/Button';
import Popup from 'reactjs-popup';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import './Header.css'


const onCandidates = () => {
    window.location.href = 'http://localhost:3000';
}

const onAddStage = () => {
    window.location.href = 'http://localhost:3000/addStages';
};



function Header (title, buttons) {
    const [alignment, setAlignment] = React.useState(window.location.pathname);

    const handleChange = (
        event,
        newAlignment
    ) => {
        setAlignment(newAlignment);
        if (newAlignment === '/') {
            onCandidates();
        }
        else if (newAlignment === '/addStages'){
            onAddStage();
        }
    };

    return (
            // <ToggleButtonGroup
            //     className="but_header"
            //     sizeLarge
            //     color="primary"
            //     value={alignment}
            //     exclusive
            //     onChange={handleChange}
            //     aria-label="label"
            //     fullWidth
            // >
            //     <ToggleButton size="large" value="/addStages">שלבים</ToggleButton>
            //     <ToggleButton size="large" value="/">מועמדים</ToggleButton>
            // </ToggleButtonGroup>    
        <header className="title-header">
            
            <h1 className="title">{title}</h1>
            {buttons()}
            
        </header>
    // <div style={{ display: "grid", gridTemplateColumns: "8fr 1fr" }}>
        
    //     {/* <div className = "Header" >
    //         <a>{title}</a>
    //     </div > */}
        
    //     {/* <div className="MenuHolder">
    //         <Popup trigger=
    //             {<a className="Header" onClick={onCandidates}>|||</a>}
    //             position="bottom right">
    //             {
    //             close => (
    //                 <div className="Menu">
    //                     <div>
    //                         <a onClick={onCandidates}>מועמדים</a>

    //                     </div>
    //                     <div>
    //                         --------------
    //                     </div>
    //                     <div>
    //                     <a onClick={onAddStage}>הוספת שלב</a>
    //                     </div>
    //                 </div>
    //             )
    //         }
    //         </Popup>
            
    //     </div> */}
    // </div>
);
}

export default Header;