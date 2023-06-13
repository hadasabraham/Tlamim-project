import React, { useEffect, useState, Component } from "react";
import data_table from "./candidateTables/dataTable";
import SearchField from "./candidateTables/searchField";
import Header from './Header';
import './CandidatesTable.css';
import Button from '@mui/joy/Button';
import Textarea from '@mui/joy/Textarea';
import Popup from 'reactjs-popup';
// class StagePopUp extends Component {
//     state = {
//         name: "",
//         number: ""
//     };
//     handleName = (event) => {
//         this.setState({ name: event.target.value });
//     };
//     handleNumber = (event) => {
//         this.setState({ number: event.target.value });
//     };
//     handleClick = () => {

//         this.props.toggle(this.state.number, this.state.name);
//     };
//     render() {
//         return (
//             <div style={{ display: "grid", gridTemplateColumns: "0fr 3fr 3fr" }}>
//                 <Button className="submit" onClick={this.handleClick}>הוסף</Button>
//                 <Textarea className="textbox" type="text" name="name" placeholder={"שם השלב"} onChange={this.handleName} />
//                 <Textarea className="textbox" type="text" name="name" placeholder={"מספר השלב"} onChange={this.handleNumber} />
//             </div>
//         );
//     }
// }

class PopUp extends Component
{
    state = {
        name: ""
    };
    handleName = (event) => {
        this.setState({ name: event.target.value});
    }; 
    handleClick = () => {

        this.props.toggle(this.state.name);
    };
    render() {
        return (
            <div style={{ display: "grid", gridTemplateColumns: "0fr 3fr" }}>
                <Button className="submit" onClick={this.handleClick}>יצא</Button>
                <Textarea className="textbox" type="text" name="name" placeholder={"שם הקובץ"} onChange={this.handleName} />
            </div>
            
            // <div className="modal">
            //     <div className="modal_content">
            //         <span className="close" onClick={() => this.props.toggle(false)}>
            //             &times;
            //         </span>
            //         <form>
            //             <label>
            //                 Snapshot Name:
            //                 <input type="text" name="name" onChange={this.handleName} />
            //             </label>
            //             <button className="submit" onClick={this.handleClick}>submit</button>
            //         </form>
            //     </div>
            // </div>
        );
    }
}

export default function CandidatesTable() {
    const [candidates_list, setCandidateList] = useState([])
    const [cond, setCond] = useState("הכול")
    const fetchTodos = async (value) => {
        const response = await fetch("http://localhost:8001/candidates/search/" + value)
        const data = await response.json()
        setCandidateList(data)
    }
    const [state, setState] = useState(false)
    const [menu, setMenu] = useState(false)
    const onMenu = () => {
        setMenu(!menu);
        //
    }
    const handleSearch = (value) => {
        if (value === "")
        {
            setCond("הכול")
            fetchTodos("הכול")
        }
        else
        {
            setCond(value)
            fetchTodos(value) 
        }
    }
    const refresh = () =>
    {
        fetchTodos(cond) 
    }

    const onStatusChange = async (email, event) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "status_parameter": { "email": email, "status": event.target.value } })
        };
        await fetch('http://localhost:8001/set/status', requestOptions);
        refresh(); 
    };

    const onGeneralNotesChange = async (email, event) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "notes_parameter": { "email": email, "notes": event.target.value } })
        };
        await fetch('http://localhost:8001/set/general_notes', requestOptions);
        refresh();
    };

    const onExport = () => {
        setState(!state);
        //
    }

    const onToggle = async (value) => {
        if (value === false)
        {
            onExport();
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "export": { "name": value, "condition": cond } })
        };
        await fetch('http://localhost:8001/export/', requestOptions);
        onExport(); 
    };

    const onRefresh = async () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "request": {} })
        };
        await fetch('http://localhost:8001/refresh/all', requestOptions);
        fetchTodos("הכול");
    };

    useEffect(() => {
        refresh();
    }, [])
    
    const onAddStage = () => {
        window.location.href = 'http://localhost:3000/addStages';
    };

    const buttons = () => {
        return (
            <div>
                <Popup trigger=
                    {<Button>יצא לאקסל</Button>}
                    position="left center">
                    {
                        close => (
                            <div>
                                <PopUp toggle={onToggle}></PopUp>
                            </div>
                        )
                    }
                </Popup>
                <> </>
                <Button className="export" onClick={onAddStage}>ערוך שלבים</Button>
                <> </>
                <Button className="export" onClick={onRefresh}>רענן</Button>
            </div>
        );
    };

    return (
        <div>
            {Header("מועמדים", buttons)}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 3fr 10fr 3fr 1fr" }}>
                {/* <div className="but_hoder">
                    <Popup trigger=
                        {<Button>יצא לאקסל</Button>}
                        position="right center">
                        {
                            close => (
                                <div>
                                    <PopUp toggle={onToggle}></PopUp>
                                </div>
                            )
                        }
                    </Popup>
                </div> */}
                <div></div>
                <div></div>
                <SearchField placeholder="Search candidates" onChange={handleSearch} />
                <div></div>
                <div></div>
                {/* <div className="but_hoder">
                    <Button className="export" onClick={onRefresh}>רענן</Button>
                </div> */}
            </div>
            {/* {state ? <PopUp toggle={onToggle} /> : null} */}
            {data_table(candidates_list, onStatusChange, onGeneralNotesChange)}
            {/* <Button className="export" onClick={onAddStage}>ערוך שלבים</Button> */}
        </div>
    )
}