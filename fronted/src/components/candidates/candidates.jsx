import React, { useEffect, useState } from "react";
import DataTable from 'react-data-table-component';
import Header from '../Header';
import Textarea from '@mui/joy/Textarea';
import Button from '@mui/joy/Button';

//import TcpSocket from 'react-native-tcp-socket';
import './candidates.css';


const Checkbox = (passed, email, stage, fetchTodos) => {
    const [isChecked, setIsChecked] = useState(passed);
    const onChange = async () => {
        if (passed === false) {
            setIsChecked(true);
        
            const passed = true;
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    "decision_parameter":
                    {
                        "stage": stage,
                        "email": email,
                        "passed": passed
                    }
                })
            };
            await fetch('http://localhost:8001/set/decision', requestOptions);
            fetchTodos();
        }
    };
    return (
        <div className="checkbox-wrapper">
            <label>
                <input type="checkbox" 
                    checked={isChecked} 
                    onChange={onChange}/>
            </label>
        </div>
    );
};


const columns = (onSelect, email, fetchTodos) => [
    {
        name: 'שלב', selector: 'stage_index', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'right' }}>{row.stage}</div>
    },
    {
        name: 'ציון', selector: 'grade', sortable: true, 
        cell: row => 
            <div style={{ fontSize: 20, textAlign: 'center' }}>
                <select value={row.grade} onChange={(event) => { onSelect(row.stage, row.note ,event) }}>
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
        name: 'מצב', selector: 'passed', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'center' }}>{Checkbox(row.passed, email, row.stage, fetchTodos)}</div>
    }, 
    // {
    //     name: 'שינוי אחרון', selector: 'last_modify', sortable: true, cell: row => <div style={{ fontSize: 20, textAlign: 'center' }}>{row.grade_info[0]?.last_modify}</div>
    // }

];


const showAnswer = ( {data} ) => {
    const ret = (
        <div>
            <Textarea value={data.answer} readOnly={true}/>
        </div>
    );
    return ret;
};



function OnExpendedRow({data}, email) {
    const [_notes, setNotes] = useState(data.notes);
    const [passed, setPassed] = useState('False');
    // if (data.grade_info[0]?.grade === 'True') {
    //     setPassed('True');
    // }
    const onClick = async () => {
        const grade = parseInt(data.grade, 10);
        if (!grade) {
            grade = 0;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "grade_parameter":
                {
                    "email": email, "stage": parseInt(data.stage, 10),
                    "score": grade, "notes": _notes
                }
            })
        };
        // const requestOptions = {
        //     method: 'PUT',
        //     headers: { 'Content-Type': 'application/json' },
            
        //     body: JSON.stringify({
        //         "grade_parameter":
        //         {
        //             "email": email, "stage_index": parseInt(data.stage_index, 10),
        //             "score": parseFloat(data.grade_info[0]?.grade, 10), "notes": , "passed": passed
        //         }
        //     })
        // };
        await fetch('http://localhost:8001/set/grade', requestOptions);
    };

    return (
        <>
        
        <div style={{ display: "grid", gridTemplateColumns: "6fr 1fr 1fr" }}>
                <DataTable className='stage_qa'
                    columns={[{ selector: 'question', sortable: true, }]}
                    data={data.answers}
                    expandableRows
                    expandOnRowClicked
                    expandableRowsComponent={showAnswer}
                />
                <Textarea className="input" type="text" placeholder="הערות" value={_notes} onChange={event => setNotes(event.target.value)} />
                <div className="commit_holder">
                    <Button className="commit" type="submit" onClick={onClick} >עדכן</Button>
                </div>
        </div>
            {/*                <h3 className='qa_title'>הערות</h3>
 <div style={{ display: "grid", gridTemplateColumns: "4fr 4fr" }}>
            <DataTable className='stage_qa'
                    columns={[{ selector: 'question', sortable: true, }]}
                data={data.answers}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>כללי</h3>
            <DataTable className='stage_qa'
                    columns={[{ selector: 'question', sortable: true }]}
                    data={data.answers}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>אישי</h3>
            <DataTable className='stage_qa'
                    columns={[{ selector: 'question', sortable: true }]}
                    data={data.answers}
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={showAnswer}
            />
            <h3 className='qa_title'>טפסים</h3>
        </div> */}
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
const onClick = () => {
    window.location.href = 'http://localhost:3000';
}

const _candidate = (data, onSelect, onNextLevel, fetchTodos) => {
    return (
        <div className="candidate">
            {Header(data.email + ' - ' + data.name)}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr" }}>
                <h1 className='stage_info'>סטטוס : {status(data.status)}</h1>
                <h1 className='stage_info'>שלב : {data.current_stage}</h1>
            </div>
            <DataTable className='candidate_table'
                columns={columns(onSelect, data.email, fetchTodos)}
                data={data.stages_info}
                pagination
                highliightOnHover
                persistTableHead
                expandableRows
                expandOnRowClicked
                expandableRowsComponent={(e) => OnExpendedRow(e, data.email)}
                customTheme={{
                    rows: {
                        textAlign: 'right',
                        fontSize: '50px'
                    }
                }}
            />
            <div className="">
                <Button onClick={onClick}>back</Button>
            </div>
        </div>
    );
    /*
    <div style={{ display: "grid", gridTemplateColumns: "1fr 3fr" }}>
                
                <DataTable className='all_nodes'
                    columns={[{ "name": "הערות" }]}
                    data={[{}]}
                    expandableRows
                    expandOnRowClicked
                    expandableRowsComponent={(e) => <p className="allnotes">{data.notes}</p>}
                />
            </div>
    */
};

export default function Candidate({ email }) {
    const [candidates_info, setCandidate] = useState([]);
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8001/candidate/"+email)
        const data = await response.json()
        setCandidate(data)
    };

    const onSelect = async (stage_index, notes, event) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "grade_parameter": 
            {
                "email": email, "stage": parseInt(stage_index, 10), 
                "score": parseInt(event.target.value, 10) , "notes": notes} })
        };
        await fetch('http://localhost:8001/set/grade', requestOptions);
        fetchTodos();
    };

    const onNextLevel = async (data) => {
        const passed = true;
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "decision_parameter":
                {
                    "stage": data.current_stage,
                    "email": data.email, 
                    "passed": passed
                }
            })
        };
        await fetch('http://localhost:8001/set/decision', requestOptions);
        fetchTodos();
    };


    useEffect(() => {
        fetchTodos()
    }, [])


    return (
        <>
            {_candidate(candidates_info, onSelect, onNextLevel, fetchTodos)}
        </>
    )
}

