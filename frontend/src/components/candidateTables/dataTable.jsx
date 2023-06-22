import React, { useState } from 'react';
import DataTable from 'react-data-table-component';
import Textarea from '@mui/joy/Textarea';
import TextareaAutosize from '@mui/base/TextareaAutosize';
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



const conditionalRowStyles = [
    {
        when: row => row.missing,
        style: {
            backgroundColor: "#87CEFA",
        }
    }
];


const customStyles = {
    cells: {
        style: {
            width: 'fit-content',
        },
    },
};


const data_table = (data, onStatusChange, sentGeneralNotes) => {
    const emptyRows = []; //Array(minimumRows - data.length).fill({});

    const [generalNotes, changeGeneralNotes] = useState(data.map(
        (r) => ({ [r.email]: [r.general_notes, 0, Date.now()]})
    ));

    const onGeneralNotesChange = React.useCallback((email, notes) => {
        changeGeneralNotes(...generalNotes, {email: [notes, generalNotes[email][1]+1]});
        if (generalNotes[email][1] === 10 || Date.now() > 10000 + generalNotes[email][2])
        {
            sentGeneralNotes(email, notes);
            changeGeneralNotes(...generalNotes, { email: [notes, 0, Date.now()] });
        }
    }, []);

    const columns = (onStatusChange, onGeneralNotesChange) => {
        return [
            {
                name: 'אימייל', selector: 'email', sortable: true, width: '12%'
            },
            {
                name: 'שם', selector: 'name', sortable: true, width: "10%"
            },
            {
                name: 'שלב', selector: 'stage', sortable: true, width: "7%"
            },
            {
                name: 'טלפון', selector: 'phone', sortable: true, width: "10%"
            },
            {
                name: 'ציון', selector: 'average_grade', sortable: true, width: '7%'
            },
            {
                name: 'סטטוס', selector: 'status', sortable: true, width: "12%",
                cell: row => (
                    <div className="nice-select">
                        {/* <CreatableSelect isClearable defaultInputValue={row.status} 
                options={select_options} onInputChange={(event) => { onSelect(row.email, event) }} 
                onChange={(event) => { onSelect(row.email, event) }}></CreatableSelect> */}
                        {/* <Textarea type="text" name="name" value={row.status} 
                onChange={(event) => { onStatusChange(row.email, event) }} /> */}
                        <select value={row.status} onChange={(event) => { onStatusChange(row.email, event) }}>
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
                name: 'הערות', selector: 'general_notes', sortable: true, // width: "52%",
                cell: row => (
                    <textarea
                        value={row.general_notes}
                        onChange={(event) => { onGeneralNotesChange(row.email, event) }}
                        placeholder="הערות"
                        rows={1}
                        cols={50}
                        style={{
                            padding: '7px',
                            fontSize: '16px',
                            borderRadius: '5px',
                            border: '1px solid #ccc',
                            resize: 'none',
                            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                            width: 'fit-content',
                            fontFamily: 'Arial, sans-serif',
                        }}
                    />
                )
            },


        ];
    }






    return (
        <div className="candidate-table">
            <DataTable
                className='table'
                columns={columns(onStatusChange, onGeneralNotesChange)}
                data={[...data,...emptyRows]}
                // pagination
                highliightOnHover
                // selectableRows
                onRowClicked={rowClicked}
                persistTableHead
                // selectableRowsHighlight
                fixedHeader
                conditionalRowStyles={conditionalRowStyles}
                customStyles={customStyles}
            />
        </div>
    );
};

export default data_table;