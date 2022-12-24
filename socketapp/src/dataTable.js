import React from 'react';
import DataTable from 'react-data-table-component';
//import TcpSocket from 'react-native-tcp-socket';

const rowClicked = (row, e) => {
};

const columns = [
    {
        name: 'Name', selector: 'nane', sortable: true,
        cell: row => (
            <div data-tag="allowRowEvents">
                <div aria-hidden="true" onClick={rowClicked}>
                    {row.name}
                </div>
            </div>
        ),
    },
    { email: 'Email', selector: 'email', sortable: true },
    { status: 'Status', selector: 'status', sortable: true }
];


const onExpendedRow = ({ data }) => {

    return (
        <>
            <p>hello</p>
            <p>{data.hide}</p>
            <p>1</p>
            <p>2</p>
        </>
    );
};

const data_table = (data) => {
    return (
        <div className="candidate-table">
            <DataTable
                title='Candidates'
                columns={columns}
                data={data}
                pagination
                highliightOnHover
                selectableRows
                onRowClicked={rowClicked}
                persistTableHead
                selectableRowsHighlight
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={onExpendedRow}
            />
        </div>
    );
};

export default data_table;
