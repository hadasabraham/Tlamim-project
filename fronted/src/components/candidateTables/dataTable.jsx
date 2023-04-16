import React from 'react';
import DataTable from 'react-data-table-component';


import "./dataTable.css";

const rowClicked = (row, e) => {
    window.location.href = 'http://localhost:3000/candidate/'+row.email;
};





const columns = (onSelect) => {
    return [
    {
        name: 'אימייל', selector: 'email', sortable: true,
    },
    {
        name: 'שם', selector: 'name', sortable: true
    },
    { 
        name: 'שלב', selector: 'stage', sortable: true 
    },
    {
        name: 'סטטוס', selector: 'status', sortable: true, 
        cell: row => (
            <div>
                <select value={row.status} onChange={(event) => {onSelect(row.email, event)}}>
                    <option value="אין">אין</option>
                    <option value="בתהליך">בתהליך</option>
                    <option value="סיים שלב">סיום שלב</option>
                </select>
            </div>
        )
    },
    {
        name: 'שינוי אחרון', selector: 'last_modify', sortable: true
    },
    {
        name: 'טלפון', selector: 'phone', sortable: true
    }
];
}


const data_table = (data, onSelect) => {
    return (
        <div className="candidate-table">
            <DataTable
                columns={columns(onSelect)}
                data={data}
                pagination
                highliightOnHover
                selectableRows
                onRowClicked={rowClicked}
                persistTableHead
                selectableRowsHighlight
                fixedHeader
            />
        </div>
    );
};

export default data_table;