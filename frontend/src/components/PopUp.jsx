import React, { useState } from 'react';
import Button from '@mui/joy/Button';


function PopupButton(text, func, butt) {
    // const [showPopup, setShowPopup] = useState(false);

    // const handleAction = () => {
    //     func();
    //     setShowPopup(false);
    // };
    const openPopupWindow = () => {
        const confirmation = window.confirm(text);
        if (confirmation) {
            func();
        }
    };
    return (
        <div>
            <Button onClick={openPopupWindow}>{butt}</Button>
        </div>
    );
    // return (
    //     <div>
    //         <Button onClick={() => setShowPopup(true)}>Open Popup</Button>

    //         {showPopup && (
    //             <div className="popup">
    //                 <div className="popup-content">
    //                     <h2>{text}</h2>
    //                     <button onClick={handleAction}>Yes</button>
    //                     <button onClick={() => setShowPopup(false)}>No</button>
    //                 </div>
    //             </div>
    //         )}
    //     </div>
    // );
}

export default PopupButton;
