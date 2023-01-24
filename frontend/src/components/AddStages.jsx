import React, { useEffect, useState, Component } from "react";
import DataTable from 'react-data-table-component';
import Header from './Header';

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
            <div className="modal">
                <div className="modal_content">
                    <span className="close" onClick={() => this.props.toggle(false, false)}>
                        &times;
                    </span>
                    <form>
                        <label>
                            stage number:
                            <input type="text" name="name" onChange={this.handleNumber} />
                        </label>
                        <label>
                            stage name:
                            <input type="text" name="name" onChange={this.handleName} />
                        </label>
                        <button className="submit" onClick={this.handleClick}>submit</button>
                    </form>
                </div>
            </div>
        );
    }
}

class FormPopUp extends Component {
    state = {
        number: "",
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
                            <input type="text" name="name" onChange={this.handleNumber} />
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
        const response = await fetch("http://localhost:8001/stages/forms")
        const data = await response.json()
        setStageList(data)
    }
    useEffect(() => {
        fetchTodos()
    }, [])
    const addStage = () => {
        setsState(!sstate);
    }

    const addform = () => {
        setfState(!fstate);
    }

    const onStageToggle = async (number, name) => {
        if (number === false) {
            addStage();
            return ;
        }
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "stage_parameter": { "stage_index": number, "stage_name": name } })
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
            body: JSON.stringify({ "form_parameter": { "stage_index": number, "form_id": indx, "form_link": link} })
        };
        await fetch('http://localhost:8001/add/form', requestOptions);
        addStage();
    }

    const onClick = () => {
        window.location.href = 'http://localhost:3000';
    }

    const columns = [
        {
            name: "מספר השלב", selector: "stage_index", 
        },
        {
            name: "שם השלב", selector: "stage_name", 
        }
    ];

    const rowClicked = (row, e) => {
        const links = [];
        row.data.form_links.forEach((data) => {
            links.push(<a href={data}>{data}</a>)
        })
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
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={rowClicked}

            />
            <button onClick={onClick}>back</button>
            <button onClick={addStage}>addStage</button>
            {sstate ? <StagePopUp toggle={onStageToggle} /> : null}
            <button onClick={addform}>addform</button>
            {fstate ? <FormPopUp toggle={onFormToggle} /> : null}
        </div>
    );
}