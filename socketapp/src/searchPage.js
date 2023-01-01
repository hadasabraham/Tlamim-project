import React from "react";
import data_table from "./dataTable";
import { Button } from 'react-native';
import "./search.css"

const search_page = (button_handler, table_data) => {
    return (
        <div>
            <button className="refresh" onClick={button_handler}>🔄</button>
            {data_table(table_data)}
        </div>
    )
};



export default search_page;