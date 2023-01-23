import React, { useEffect, useState, Component } from "react";
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
    return (
        <div>
            {Header("Add Stages")}
            <button onClick={onClick}>back</button>
            <button onClick={addStage}>addStage</button>
            {sstate ? <StagePopUp toggle={onStageToggle} /> : null}
            <button onClick={addform}>addform</button>
            {fstate ? <FormPopUp toggle={onFormToggle} /> : null}
        </div>
    );
}