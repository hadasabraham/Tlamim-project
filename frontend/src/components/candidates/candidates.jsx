import React, { useEffect, useState } from "react";
import DataTable from 'react-data-table-component';
import Header from '../Header';
//import TcpSocket from 'react-native-tcp-socket';
import './candidates.css';


const passed_str = (passed) => {
    if (passed === 'True')
    {
        return 'עבר';
    }
    return "בתהליך";
}

const columns = (onSelect) => [
    {
        name: 'שלב', selector: 'stage_index', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'center' }}>{row.stage_index}</div>
    },
    {
        name: 'ציון', selector: 'grade', sortable: true, 
        cell: row => 
            <div style={{ fontSize: 20, textAlign: 'center' }}>
                <select value={row.grade_info[0]?.grade} onChange={(event) => { onSelect(row.stage_index, row.grade_info[0]?.passed, row.grade_info[0]?.notes ,event) }}>
                    <option value="">-</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                    <option value="9">9</option>
                    <option value="10">10</option>
                </select>
            </div>
    },
    {
        name: 'מצב', selector: 'passed', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'center' }}>{passed_str(row.grade_info[0]?.passed)}</div>
    }, 
    {
        name: 'שינוי אחרון', selector: 'timestamp', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'center' }}>{row.grade_info[0]?.timestamp}</div>
    }

];


const showAnswer = ( {data} ) => {
    const ret = (
        <div>
            <p>{data.answer}</p>
        </div>
    );
    return ret;
};



function OnExpendedRow({data}, email) {
    const [_notes, setNotes] = useState(data.grade_info[0]?.notes);
    const [passed, setPassed] = useState('False');
    if (data.grade_info[0]?.grade === 'True') {
        setPassed('True');
    }
    const onClick = async () => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "grade_parameter":
                {
                    "email": email, "stage_index": parseInt(data.stage_index, 10),
                    "score": parseFloat(data.grade_info[0]?.grade, 10), "notes": _notes, "passed": passed
                }
            })
        };
        await fetch('http://localhost:8001/update/grades', requestOptions);
    };

    return (
        <>
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 4fr" }}>
                <textarea className="input" type="text" value={_notes} onChange={event => setNotes(event.target.value)} />
                <button className="commit" onClick={onClick}>עדכן</button>
                <h3 className='qa_title'>הערות</h3>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "4fr 4fr" }}>
            <DataTable className='stage_qa'
                columns={[{ selector: 'title', sortable: true, }]}
                data={data.general}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>כללי</h3>
            <DataTable className='stage_qa'
                columns={[{ selector: 'title', sortable: true }]}
                data={data.private}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>אישי</h3>
            <DataTable className='stage_qa'
                columns={[{ selector: 'title', sortable: true }]}
                data={data.forms}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>טפסים</h3>
        </div>
        </>
    );
};


function status (stat) {
    if (stat === "")
    {
        return "אין";
    }
    return stat;
} 


// const onClick = () => {
//     window.location.href = 'http://localhost:3000';
// }

const _candidate = (data, onSelect, onNextLevel) => {
    return (
        <div className="candidate">
            {Header(data.email + ' - ' + data.name)}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr" }}>
                <button className="next_stage" onClick={() => onNextLevel(data)}>עבור שלב</button>
                <h1 className='stage_info'>סטטוס : {status(data.status)}</h1>
                <h1 className='stage_info'>שלב : {data.stage}</h1>
            </div>
            <DataTable className='candidate_table'
                columns={columns(onSelect)}
                data={data.stages}
                pagination
                highliightOnHover
                persistTableHead
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={(e) => OnExpendedRow(e, data.email)}
                customTheme={{
                    rows: {
                        fontSize: '50px'
                    }
                }}
            />
            <DataTable className='all_nodes'
                columns={[{"name": "הערות"}]}
                data={[{}]}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={(e) => <p className="allnotes">{data.all_notes}</p>}
            />
            
        </div>
    );
};

export default function Candidate({ email }) {
    const [candidates_info, setCandidate] = useState([]);
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8001/candidate/entire_info/"+email)
        const data = await response.json()
        setCandidate(data)
    };

    const onSelect = async (stage_index, passed, notes, event) => {
        const _passed = 'False';
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "grade_parameter": 
            {
                "email": email, "stage_index": parseInt(stage_index, 10), 
                "score": parseFloat(event.target.value, 10) , "notes": notes, "passed": _passed} })
        };
        await fetch('http://localhost:8001/update/grades', requestOptions);
        fetchTodos();
    };

    const onNextLevel = async (data) => {
        const passed = 'True';
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "grade_parameter":
                {
                    "email": data.email, "stage_index": parseInt(data.stage, 10),
                    "score": parseFloat(data.stages[parseInt(data.stage, 10)]?.grade_info[0]?.grade, 10), "notes": data.stages[parseInt(data.stage, 10)]?.grade_info[0]?.notes, "passed": passed
                }
            })
        };
        await fetch('http://localhost:8001/update/grades', requestOptions);
        fetchTodos();
    };


    useEffect(() => {
        fetchTodos()
    }, [])
    return (
        <>
            {_candidate(candidates_info, onSelect, onNextLevel)}
        </>
    )
}

