import React, { useState, useEffect } from 'react';
import { Select, MenuItem, FormControl, InputLabel, CircularProgress } from '@mui/material'

const LoginForm = () => {
    const [username, setUsername] = useState('');
    const [year, setYear] = useState('');
    const [yearList, setYearList] = useState([]);
    const [yearSelected, setYearSelected] = useState(""); 
    const [loading, setLoading] = useState(false); // Loading state


    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8001/stages")
        const data = await response.json()
        // setYear(data.year);
        setYearList(data.year_list);
    }
    useEffect(() => {
        fetchTodos()
    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // You can perform any necessary validation or authentication logic here

        console.log('Submitted username:', username);
        console.log('Submitted year:', year);

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        };
        setLoading(true);
        await fetch(`http://localhost:8001/database/change/${year}`, requestOptions);
        setLoading(false);
        window.location.href = 'http://localhost:3000/candidates';
    };

    // const Login = async () => {
        
    // }

    return (
    <div style={styles.container}>
        <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.formGroup}>
                <label htmlFor="username" style={styles.label}>
                    Username:
                </label>
                <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={styles.input}
                    required
                />
            </div>
            <div style={styles.formGroup}>
                <label htmlFor="year" style={styles.label}>
                    Year:
                </label>
                <FormControl style={styles.select}>
                    <InputLabel id="demo-simple-select-label">בחר שנה</InputLabel>
                    <Select
                        id="demo-simple-select"
                        value={year}
                        onChange={(e) => {
                            setYear(e.target.value);
                            setYearSelected(e.target.value !== 'בחר שנה' ? "123" : "");
                        }}
                        required
                        label="בחר שנה">
                        {yearList.map((val) =>
                            <MenuItem value={val}>{val}</MenuItem>
                        )}
                    </Select>
                </FormControl>
            </div>
            <button type="submit" style={styles.button}>
                כניסה
            </button>
        </form>
        {loading &&
            <div style={styles.loadingOverlay} >
                <CircularProgress /> {/* Loading animation */}
            </div >
        }
    </div>
    );
};

const styles = {
    container: {
        position: 'relative',
    },
    loadingOverlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.8)', // Semi-transparent background color
        zIndex: 9999,
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        margin: 'auto',
        width: '300px',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        backgroundColor: '#f8f8f8',
    },
    formGroup: {
        marginBottom: '15px',
        width: '100%',
    },
    label: {
        fontWeight: 'bold',
        marginBottom: '5px',
    },
    hidden:
    {
        width: '0px',
        hight: '0px',
    },
    input: {
        width: '100%',
        padding: '8px',
        fontSize: '14px',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
    select: {
        width: '100%',
        // padding: '8px',
        fontSize: '14px',
        // border: '1px solid #ccc',
        borderRadius: '4px',
    },
    button: {
        width: '100%',
        padding: '10px',
        fontSize: '16px',
        fontWeight: 'bold',
        color: '#fff',
        backgroundColor: '#007bff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    },
};

export default LoginForm;
