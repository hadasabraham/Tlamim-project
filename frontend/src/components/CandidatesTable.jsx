import React, { useEffect, useState } from "react";

import data_table from "./candidateTables/dataTable";
import SearchField from "./candidateTables/searchField";
import Header from './Header';



export default function CandidatesTable() {
    const [candidates_list, setCandidateList] = useState([])
    const fetchTodos = async (value) => {
        const response = await fetch("http://localhost:8001/candidates/query/" + value)
        const data = await response.json()
        setCandidateList(data)
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
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "dits": { "email": email, "status": event.target.value } })
        };
        await fetch('http://localhost:8001/update/status', requestOptions);
        fetchTodos("הכול"); 
    };

    useEffect(() => {
        fetchTodos("הכול")
    }, [])
    return (
        <div>
            {Header("מועמדים")}
            <SearchField placeholder="Search candidates" onChange={handleSearch} />
            {data_table(candidates_list, onSelect)}
        </div>
    )
}