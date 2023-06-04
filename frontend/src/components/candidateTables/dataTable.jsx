import React from 'react';
import DataTable from 'react-data-table-component';
import Textarea from '@mui/joy/Textarea';
import CreatableSelect from 'react-select/creatable';

import "./dataTable.css";

const rowClicked = (row, e) => {
    window.location.href = 'http://localhost:3000/candidate/'+row.email;
};


const select_options = [
    { value: "ממתין לטופס", label: "ממתין לטופס" },
    { value: "להתקשר", label: "להתקשר" },
    { value: "חסר התייחסות", label:  "חסר התייחסות" },
];


const columns = (onStatusChange, onGeneralNotesChange) => {
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
        name: 'טלפון', selector: 'phone', sortable: true
    },
    {
        name: 'סטטוס', selector: 'status', sortable: true, 
        cell: row => (
            <div>
                {/* <CreatableSelect isClearable defaultInputValue={row.status} 
                options={select_options} onInputChange={(event) => { onSelect(row.email, event) }} 
                onChange={(event) => { onSelect(row.email, event) }}></CreatableSelect> */}
                {/* <Textarea type="text" name="name" value={row.status} 
                onChange={(event) => { onStatusChange(row.email, event) }} /> */}
                <select value={row.status} onChange={(event) => { onStatusChange(row.email, event)}}>
                    <option value=""></option>
                    <option value="ממתין לטופס">ממתין לטופס</option>
                    <option value="להתקשר">להתקשר</option>
                    <option value="חסר התייחסות">חסר התייחסות</option>
                    <option value="הוסר">הוסר</option>

                </select>
            </div>
        )
    },

    {
        name: 'הערות', selector: 'general_notes', sortable: true,
        cell: row => (
            <div>
                <Textarea type="text" name="name" value={row.general_notes} 
                onChange={(event) => { onGeneralNotesChange(row.email, event) }} />
            </div>
        )
    },
    {
        name: 'ציון', selector: 'average_grade', sortable: true
    },

];
}

const conditionalRowStyles = [
    {
        when: row => row.missing,
        style: {
            backgroundColor: "#87CEFA",
        }
    }
];


const minimumRows = 0;

const data_table = (data, onStatusChange, onGeneralNotesChange) => {
    const emptyRows = []; //Array(minimumRows - data.length).fill({});
    return (
        <div className="candidate-table">
            <DataTable
                className='table'
                columns={columns(onStatusChange, onGeneralNotesChange)}
                data={[...data,...emptyRows]}
                // pagination
                highliightOnHover
                selectableRows
                onRowClicked={rowClicked}
                persistTableHead
                selectableRowsHighlight
                fixedHeader
                conditionalRowStyles={conditionalRowStyles}
            />
        </div>
    );
};

export default data_table;