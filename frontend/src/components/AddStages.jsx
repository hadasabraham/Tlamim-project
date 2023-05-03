import React, { useEffect, useState, Component } from "react";
import DataTable from 'react-data-table-component';
import Header from './Header';
import Button from '@mui/joy/Button';
import Textarea from '@mui/joy/Textarea';
import Popup from 'reactjs-popup';

import "./AddStage.css"

class StagePopUp extends Component {
    state = {
        name: "",
        number: ""
    };
    handleName = (event) => {
        this.setState({ name: event.target.value });
    };
    handleNumber = (event) => {
        this.setState({ number: event.target.value });
    };
    handleClick = () => {

        this.props.toggle(this.state.number, this.state.name);
    };
    render() {
        return (
                <div style={{ display: "grid", gridTemplateColumns: "0fr 3fr 3fr"}}>
                    <Button className="submit" onClick={this.handleClick}>הוסף</Button>
                    <Textarea className="textbox" type="text" name="name" placeholder={"שם השלב"} onChange={this.handleName} />
                    <Textarea className="textbox" type="text" name="name" placeholder={"מספר השלב"} onChange={this.handleNumber} />
                </div>
        );
    }
}

class FormPopUp extends Component {
    state = {
        number: "stage number",
        id: "",
        link: "",
    };
    handleNumber = (event) => {
        this.setState({ number: event.target.value });
    };
    handleId = (event) => {
        this.setState({ id: event.target.value });
    };
    handleLink = (event) => {
        this.setState({ link: event.target.value });
    };
    handleClick = () => {

        this.props.toggle(this.state.number, this.state.id, this.state.link);
    };
    render() {
        return (
            <div className="modal">
                <div className="modal_content">
                    <span className="close" onClick={() => this.props.toggle(false, false, false)}>
                        &times;
                    </span>
                    <form>
                        <label>
                            stage number:
                            <input type="text" name="name" placeholder={"stage number"} onChange={this.handleNumber} />
                        </label>
                        <label>
                            form id:
                            <input type="text" name="name" onChange={this.handleId} />
                        </label>
                        <label>
                            form link:
                            <input type="text" name="name" onChange={this.handleLink} />
                        </label>
                        <button className="submit" onClick={this.handleClick}>submit</button>
                    </form>
                </div>
            </div>
        );
    }
}




export default function AddStages() {
    const [sstate, setsState] = useState(false);
    const [fstate, setfState] = useState(false);
    const [stage_list, setStageList] = useState([])
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8001/stages")
        const data = await response.json()
        setStageList(data)
    }
    useEffect(() => {
        fetchTodos()
    }, [])
    const addStage = () => {
        fetchTodos();
    }

    const addform = () => {
        setfState(!fstate);
    }

    const onStageToggle = async (number, name, close) => {
        close();
        if (number === false) {
            addStage();
            return ;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "stage_parameter": { "index": number, "name": name, "msg": "msg" } })
        };
        await fetch('http://localhost:8001/add/stage', requestOptions);
        addStage(); 
    }

    const onFormToggle = async (number, indx, link) => {
        if (number === false) {
            addStage();
            return;
        }
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "form_parameter": { "form_id": indx, "form_link": link, "stage_index": number } })
        };
        await fetch('http://localhost:8001/add/form/', requestOptions);
        addStage();
    }

    const onClick = () => {
        window.location.href = 'http://localhost:3000';
    }

    const useRows = (row) => {
        const [id, setId] = useState(NaN);
        const [link, setLink] = useState(NaN);
        const handleId = (event) => {
            setId(event.target.value);
        };
        const handleLink = (event) => {
            setLink(event.target.value);
        };
        const onAddLink = (event) => {
            onFormToggle(row.index, id, link);
        };
        if (row.forms == 0) {
            return (
                <div style={{ display: "grid", gridTemplateColumns: "3fr 3fr 3fr" }}>
                    <Textarea type="textbox" name="name" placeholder={"form id"} onChange={handleId} />
                    <Textarea type="textbox" name="name" placeholder={"form link"} onChange={handleLink} />
                    <Button className="addform" onClick={onAddLink}>הוספה</Button>
                </div>
            );
        }
        return (
            <Button className="addform" onClick={() => window.open(row.forms[0]?.link)}> פתח טופס</Button>
        );
    }

    const columns = [
        {
            name: "מספר השלב", selector: "index", 
        },
        {
            name: "שם השלב", selector: "name", 
        },
        {
            cell: useRows
        }
    ];

    const useRowClicked = (row, e) => {
        const [id, setId] = useState(NaN);
        const [link, setLink] = useState(NaN);
        const handleId = (event) => {
            setId(event.target.value);
        };
        const handleLink = (event) => {
            setLink(event.target.value);
        };
        const onClick = (event) => {
            onFormToggle(row.data.index, id, link);
        };
        const links = [];
        row.data.forms.forEach((data) => {
            links.push(<a className="link" href={data.link}>Open Form</a>)
        })
        if (links == 0)
        {
            return (
                <div style={{ display: "grid", gridTemplateColumns: "3fr 3fr 3fr" }}>
                    <Textarea type="text" name="name" placeholder={"form id"} onChange={handleId} />
                    <Textarea type="text" name="name" placeholder={"form link"} onChange={handleLink} />
                    <Button className="submit" onClick={onClick}>submit</Button>
                </div>
            );
        }
        return (
            <div>
                {links}
            </div>
        );
    };

    return (
        <div>
            
            {Header("הוספת שלב")}
            <DataTable className="candidate-table"
                columns={columns}
                data={stage_list}
                // expandableRows
                // expandOnRowClicked
                // expandableRowsComponent={useRowClicked}

            />
            <div className="buttons"> 
                <Popup trigger=
                    {<Button onClick={addStage}>הוסף שלב</Button>}
                    position="left center">
                    {
                        
                        close => (
                            <div>
                                <StagePopUp toggle={(number, name) => onStageToggle(number, name, close)}></StagePopUp>
                            </div>
                        )
                    }
                </Popup>
                <> </>
                <Button onClick={onClick}>חזור</Button>
            </div>
        </div>
    );
    // <div className='modal'>
                        //     <div className='content'>
                        //         Welcome to GFG!!!
                        //     </div>
                        //     <div>
                        //         <button onClick=
                        //             {() => close()}>
                        //             Close modal
                        //         </button>
                        //     </div>
                        // </div>
    // {sstate ? <StagePopUp toggle={onStageToggle} /> : null}
}