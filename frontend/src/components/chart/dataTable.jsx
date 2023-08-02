import React from 'react';
import DataTable from 'react-data-table-component';
import TextareaAutosize from '@mui/base/TextareaAutosize';
import CreatableSelect from 'react-select/creatable';
import "./dataTable.css";

const rowClicked = (row, e) => {
    window.location.href = `http://localhost:3000/candidate/${row.email}`;
};

const columns = (onStatusChange, onGeneralNotesChange) => {
    return [
        {
            name: 'אימייל',
            selector: 'email',
            sortable: true,
            width: '15%',
        },
        {
            name: 'שם',
            selector: 'name',
            sortable: true,
            width: '10%',
        },
        {
            name: 'שלב',
            selector: 'stage',
            sortable: true,
            width: '10%',
        },
        {
            name: 'טלפון',
            selector: 'phone',
            sortable: true,
            width: '10%',
        },
        {
            name: 'ציון',
            selector: 'average_grade',
            sortable: true,
            width: '7%',
        },
        {
            name: 'סטטוס',
            selector: 'status',
            sortable: true,
            width: '15%',
            cell: row => (
                <div className="nice-select">
                    <select value={row.status} onChange={event => onStatusChange(row.email, event)}>
                        <option value="" />
                        <option value="ממתין לטופס">ממתין לטופס</option>
                        <option value="להתקשר">להתקשר</option>
                        <option value="חסר התייחסות">חסר התייחסות</option>
                        <option value="הוסר">הוסר</option>
                    </select>
                </div>
            ),
        },
        {
            name: 'הערות',
            selector: 'general_notes',
            sortable: true,
            cell: row => (
                <TextareaAutosize
                    value={row.general_notes}
                    onChange={event => {
                        onGeneralNotesChange(row.email, event);
                    }}
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
            ),
        },
    ];
};

const conditionalRowStyles = [
    {
        when: row => row.missing,
        style: {
            backgroundColor: '#87CEFA',
        },
    },
];

const customStyles = {
    cells: {
        style: {
            width: 'fit-content',
        },
    },
};

const dataTable = (data, onStatusChange, onGeneralNotesChange) => {
    const emptyRows = []; // Array(minimumRows - data.length).fill({});
    return (
        <div className="candidate-table">
            <DataTable
                className="table"
                columns={columns(onStatusChange, onGeneralNotesChange)}
                data={[...data, ...emptyRows]}
                pagination
                pointerOnHover
                onRowClicked={rowClicked}
                persistTableHead
                fixedHeader
                conditionalRowStyles={conditionalRowStyles}
                customStyles={customStyles}
                highlightOnHover
            />
        </div>
    );
};

export default dataTable;
