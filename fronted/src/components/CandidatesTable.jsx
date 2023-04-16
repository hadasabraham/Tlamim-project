import React, { useEffect, useState, Component } from "react";

import data_table from "./candidateTables/dataTable";
import SearchField from "./candidateTables/searchField";
import Header from './Header';
import './CandidatesTable.css';
import Button from '@mui/joy/Button';


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
            <div className="modal">
                <div className="modal_content">
                    <span className="close" onClick={() => this.props.toggle(false)}>
                        &times;
                    </span>
                    <form>
                        <label>
                            Snapshot Name:
                            <input type="text" name="name" onChange={this.handleName} />
                        </label>
                        <button className="submit" onClick={this.handleClick}>submit</button>
                    </form>
                </div>
            </div>
        );
    }
}

export default function CandidatesTable() {
    const [candidates_list, setCandidateList] = useState([])
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
            fetchTodos("הכול")
        }
        else
        {
            fetchTodos(value) 
        }
    }

    const onSelect = async (email, event) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "status_parameter": { "email": email, "status": event.target.value } })
        };
        await fetch('http://localhost:8001/set/status', requestOptions);
        fetchTodos("הכול"); 
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
            body: JSON.stringify({ "snapshot": { "name": value } })
        };
        await fetch('http://localhost:8001/snapshot', requestOptions);
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
        fetchTodos("הכול")
    }, [])
    return (
        <div>
            {Header("מועמדים")}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 10fr 1fr" }}>
                <div className="but_hoder">
                    <Button className="export" onClick={onExport}>export</Button>
                </div>
                <SearchField placeholder="Search candidates" onChange={handleSearch} />
                <div className="but_hoder">
                    <Button className="export" onClick={onRefresh}>refresh</Button>
                </div>
            </div>
            {state ? <PopUp toggle={onToggle} /> : null}
            {data_table(candidates_list, onSelect)}
        </div>
    )
}