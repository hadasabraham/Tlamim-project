import React from 'react';
import DataTable from 'react-data-table-component';
import Textarea from '@mui/joy/Textarea';
import TextareaAutosize from '@mui/base/TextareaAutosize';
import CreatableSelect from 'react-select/creatable';

import "./dataTable.css";

const rowClicked = (row, e) => {
    window.location.href = `http://localhost:3000/candidate/${row.email}`;
};


// const selectOptions = [
//     { value: "ממתין לטופס", label: "ממתין לטופס" },
//     { value: "להתקשר", label: "להתקשר" },
//     { value: "חסר התייחסות", label:  "חסר התייחסות" },
// ];

// const StageIcon = ({ stage, size = 24, color = '#000000' }) => {
//     const getIconPath = () => {
//         switch (stage) {
//             case 'ממתין לטופס':
//                 return (
//                     <path
//                         d="M12 2C6.486 2 2 6.486 2 12c0 5.514 4.486 10 10 10s10-4.486 10-10c0-5.514-4.486-10-10-10zm0 18.75C7.624 20.75 3.25 16.376 3.25 12S7.624 3.25 12 3.25 20.75 7.624 20.75 12 16.376 20.75 12 20.75zm3.79-10.073l-6.415 6.392a.577.577 0 0 1-.818 0L8.464 15.58a.58.58 0 0 1 .818-.82l1.727 1.726 5.604-5.586a.58.58 0 0 1 .82.818z"
//                         fill={color}
//                     />
//                 );
//             case 'להתקשר':
//                 return (
//                     <path
//                         d="M14.832 14.862c.247-.247.682-.195.912.136l1.139 1.139c.331.33.383.665.136.912l-1.083 1.084c-2.152 2.153-5.823 2.138-8.02-.058-2.232-2.23-2.35-5.836-.276-8.01l1.084-1.083c.248-.247.583-.195.912.135l1.139 1.14c.331.33.383.665.136.912l-1.41 1.41c-1.13 1.129-1.125 2.964.007 4.092l2.088 2.09z"
//                         fill={color}
//                     />
//                 );
//             case 'חסר התייחסות':
//                 return (
//                     <path
//                         d="M12 2C6.486 2 2 6.486 2 12c0 5.514 4.486 10 10 10s10-4.486 10-10c0-5.514-4.486-10-10-10zm0 18.75C7.624 20.75 3.25 16.376 3.25 12S7.624 3.25 12 3.25 20.75 7.624 20.75 12 16.376 20.75 12 20.75zm0-14.375a.625.625 0 1 0 0 1.25.625.625 0 0 0 0-1.25zm0 2.5c-.345 0-.625.28-.625.625v5c0 .345.28.625.625.625s.625-.28.625-.625v-5c0-.345-.28-.625-.625-.625z"
//                         fill={color}
//                     />
//                 );
//             default:
//                 return null;
//         }
//     };

//     return (
//         <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24">
//             {getIconPath()}
//         </svg>
//     );
// };


const columns = (onStatusChange, onGeneralNotesChange) => {
    return [
    {
            name: 'אימייל', selector: 'email', sortable: true, width: '15%'
    },
    {
        name: 'שם', selector: 'name', sortable: true, width: '10%'
    },
    { 
        name: 'שלב', selector: 'stage', sortable: true, width: "10%" 
    },
    {
        name: 'טלפון', selector: 'phone', sortable: true, width: "10%" 
    },
    {
        name: 'ציון', selector: 'average_grade', sortable: true, width: '7%' 
    },
    {
        name: 'סטטוס', selector: 'status', sortable: true, width: "15%" ,
        cell: row => (
            <div className="nice-select">
                <select value={row.status} onChange={(event) =>  onStatusChange(row.email, event)}>
                    <option value=""/>
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


const dataTable = (data, onStatusChange, onGeneralNotesChange) => {
    const emptyRows = []; // Array(minimumRows - data.length).fill({});
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

export default dataTable;