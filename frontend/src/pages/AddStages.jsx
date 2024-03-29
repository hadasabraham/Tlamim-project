import React, { useEffect, useState, Component } from "react";
import { Helmet } from 'react-helmet-async';
import { filter } from 'lodash';
import { sentenceCase } from 'change-case';
import Textarea from '@mui/joy/Textarea';
import DataTable from 'react-data-table-component';
import { styled, alpha } from '@mui/material/styles';
import Popup from 'reactjs-popup';


// @mui
import {
    Toolbar,
    Card,
    Table,
    Stack,
    Select,
    Paper,
    Avatar,
    Button,
    Popover,
    Checkbox,
    TableRow,
    MenuItem,
    TableBody,
    TableCell,
    FormControl,
    InputLabel,
    Container,
    Typography,
    IconButton,
    TableContainer,
    TablePagination,
} from '@mui/material';
// components
import Label from '../components/label';
import Iconify from '../components/iconify';
import Scrollbar from '../components/scrollbar';
// sections
import { UserListHead, UserListToolbar } from '../sections/@dashboard/user';
// mock
import USERLIST from '../_mock/user';
import SvgColor from '../components/svg-color';
// import Button from '@mui/joy/button';
import "./AddStage.css"

const StyledButton = styled(Button)(({ theme }) => ({
    marginLeft: '10px',
    
}));

const StyledButtonS = styled(Button)(({ theme }) => ({
    marginLeft: '340px'
}));

const StyledStack = styled(Stack)(({ theme }) => ({
    display: 'flex',
    justifyContent: 'space-between',
    padding: theme.spacing(0, 1, 0, 3),
}));

const StyledRoot = styled(Toolbar)(({ theme }) => ({
    height: 96,
    display: 'flex',
    justifyContent: 'space-between',
    padding: theme.spacing(0, 1, 0, 3),
    justifyContent: 'right',
}));

const MainStyledRoot = styled(Toolbar)(({ theme }) => ({
    height: 96,
    display: 'flex',
    justifyContent: 'space-between',
    padding: theme.spacing(0, 1, 0, 3),
}));

class StagePopUp extends Component {
    constructor(props) {
        // Required step: always call the parent class' constructor
        super(props);

        // Set the state directly. Use props if necessary.
        this.state = {
            name: "",
            number: ""
        };
    }

    handleName = (event) => {
        this.setState({ name: event.target.value });
    };

    handleNumber = (event) => {
        this.setState({ number: event.target.value });
    };

    handleClick = () => {

        this.props.toggle(this.state.number, this.state.name);
    };

    render() {
        return (
            <StyledRoot>
                <Button variant="contained" startIcon={<Iconify icon="eva:refresh-fill" />} onClick={this.handleClick}>
                    הוסף                
                </Button>
                <textarea className="textbox" placeholder={"שם השלב"} onChange={this.handleName} style={{
                    fontSize: '16px',
                    borderRadius: '5px',
                    border: '1px solid #ccc',
                    resize: 'none',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                    width: 'fit-content',
                    height: '35px',
                    fontFamily: 'Arial, sans-serif',
                }} />
                <textarea className="textbox" placeholder={"מספר השלב"} onChange={this.handleNumber} style={{
                    fontSize: '16px',
                    borderRadius: '5px',
                    border: '1px solid #ccc',
                    resize: 'none',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                    width: 'fit-content',
                    height: '35px',
                    fontFamily: 'Arial, sans-serif',
                }} />
            </StyledRoot>
        );
    }
}

export default function AddStages() {
    const [sstate, setsState] = useState(false);
    const [fstate, setfState] = useState(false);
    const [stageList, setStageList] = useState([]);
    const [year, setYear] = useState("")
    const [yearList, setYearList] = useState([]);

    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8001/stages")
        const data = await response.json()
        setStageList(data.info);
        setYear(data.year);
        setYearList(data.year_list);
    }
    useEffect(() => {
        fetchTodos()
    }, [])
    const addStage = () => {
        fetchTodos();
    }

    const addform = () => {
        setfState(!fstate);
    }
    
    const updateYear = async (year) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        };
        await fetch(`http://localhost:8001/database/change/${year}`, requestOptions);
        addStage();
    }

    const yearChange = (event) => {
        setYear(event.target.value);
        updateYear(event.target.value);
    };


    const onFormToggle = async (number, indx, link) => {
        if (number === false) {
            addStage();
            return;
        }
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "form_parameter": { "form_id": indx, "form_link": link, "stage_index": number } })
        };
        await fetch('http://localhost:8001/add/form', requestOptions);
        addStage();
    }

    const onRefresh = async () => {
        const confirmation = window.confirm('האם ברצונך לאפס את המערכת?');
        if (!confirmation) {
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "request": {} })
        };
        await fetch('http://localhost:8001/clear', requestOptions);
        fetchTodos();
    }

    const onClick = () => {
        window.location.href = 'http://localhost:3000';
    }

    const onStageRemove = async (stageNumber) => {
        const confirmation = window.confirm('האם ברצונך להסיר שלב זה?');
        if (!confirmation) {
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        };
        await fetch(`http://localhost:8001/remove/stage/${stageNumber}`, requestOptions);
        addStage();
    }

    const useRows = (row) => {
        const [id, setId] = useState(NaN);
        const [link, setLink] = useState(NaN);
        const handleId = (event) => {
            setId(event.target.value);
        };
        const handleLink = (event) => {
            setLink(event.target.value);
        };
        const onAddLink = (event) => {
            onFormToggle(row.index, id, link);
        };
        if (row.forms === 0 || row.forms.length === 0) {
            return (
                <Stack direction="row">
                    <textarea className="textbox" placeholder={"form id"} onChange={handleId} style={{
                        fontSize: '16px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        resize: 'none',
                        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                        width: 'fit-content',
                        height: '35px',
                        fontFamily: 'Arial, sans-serif',
                        marginLeft: '5px'
                    }} />
                    <textarea className="textbox" placeholder={"form link"} onChange={handleLink} style={{
                        fontSize: '16px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        resize: 'none',
                        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                        width: 'fit-content',
                        height: '35px',
                        fontFamily: 'Arial, sans-serif',
                        marginLeft: '5px'
                    }} />
                    <StyledButton variant="contained" className="addform" onClick={onAddLink}>הוספה</StyledButton>
                    <StyledButton variant="contained" onClick={() => onStageRemove(row.index)}>הסר שלב</StyledButton> 
                </Stack>
            );
        }
        return (
            <Stack direction="row">
                <StyledButtonS variant="contained" onClick={() => window.open(row.forms[0]?.link)}>פתח טופס</StyledButtonS> 
                <Button variant="contained" onClick={() => onStageRemove(row.index)}>הסר שלב</Button> 

            </Stack>
        );
    }

    const columns = [
        {
            name: "מספר השלב", selector: "index", width: "20%",
        },
        {
            name: "שם השלב", selector: "name", width: "20%",
        },
        {
            cell: useRows
        }
    ];

    const useRowClicked = (row, e) => {
        const [id, setId] = useState(NaN);
        const [link, setLink] = useState(NaN);
        const handleId = (event) => {
            setId(event.target.value);
        };
        const handleLink = (event) => {
            setLink(event.target.value);
        };
        const onClick = (event) => {
            onFormToggle(row.data.index, id, link);
        };
        const links = [];
        row.data.forms.forEach((data) => {
            links.push(<a className="link" href={data.link}>Open Form</a>)
        })
        if (links === 0)
        {
            return (
                <div style={{ display: "grid", gridTemplateColumns: "3fr 3fr 3fr" }}>
                    <Textarea type="text" name="name" placeholder={"form id"} onChange={handleId} />
                    <Textarea type="text" name="name" placeholder={"form link"} onChange={handleLink} />
                    <button className="submit" onClick={onClick}>submit</button>
                </div>
            );
        }
        return (
            <div>
                {links}
            </div>
        );
    };

    const [open, setOpen] = useState(null);

    const [page, setPage] = useState(0);

    const [selected, setSelected] = useState([]);

    const [filterName, setFilterName] = useState('');

    const [name, setName] = useState("");

    const [number, setNumber] = useState('');

    const handleCloseMenu = () => {
        setOpen(null);
    };

    const handleFilterByName = (event) => {
        setPage(0);
        setFilterName(event.target.value);
    };


    const handleName = (event) => {
        setName(event.target.value);
    };

    const handleNumber = (event) => {
        setNumber(event.target.value);
    };

    const onStageToggle = async (number, name) => {
        setsState(false);
        if (number === false) {
            addStage();
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "stage_parameter": { "index": number, "name": name, "msg": "msg" } })
        };
        await fetch('http://localhost:8001/add/stage', requestOptions);
        addStage();
    }

    const onReqDup = async (event) => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        };
        await fetch(`http://localhost:8001/dup/forms/${event.target.value}`, requestOptions);
        addStage();
    }


    return (
        <>
      <Helmet>
        <title> Stages | tlamim </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Button variant="contained" startIcon={<Iconify icon="eva:refresh-fill" />} onClick={onRefresh}>
            איתחול מערכת
          </Button>
          <Typography variant="h4" gutterBottom>
            <Stack direction="row" alignItems="right">
              שלבים
              <img src={'/assets/icons/navbar/ic_stages.svg'} alt="שלבים" style={{ width: 40, height: 40 }} />
            </Stack>
          </Typography>
        </Stack>

        <Card>
            <MainStyledRoot>
                {/* <Button variant="contained" startIcon={<Iconify icon="eva:arrow-fill" />} onClick={addStage}>
                    איתחול מערכת
                </Button>   */}
                <FormControl>
                    <InputLabel id="demo-simple-select-label">בחר שנה</InputLabel>
                    <Select
                    id="demo-simple-select"
                    value={year}
                    label="בחר שנה"
                    onChange={yearChange}>
                        {yearList.map((val) =>
                            <MenuItem value={val}>{val}</MenuItem>
                        )}
                    </Select>
                </FormControl>
                {sstate && <StyledRoot>
                    <Button variant="contained" startIcon={<Iconify icon="eva:arrow-left-fill" />} onClick={() => onStageToggle(number, name)}>
                        הוסף
                    </Button>
                    <textarea className="textbox" placeholder={"שם השלב"} onChange={handleName} style={{
                        fontSize: '16px',
                        lineHeight: '25px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        resize: 'none',
                        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                        width: 'fit-content',
                        height: '35px',
                        fontFamily: 'Arial, sans-serif',
                        marginLeft: '10px'
                    }} />
                    <textarea className="textbox" placeholder={"מספר השלב"} onChange={handleNumber} style={{
                        fontSize: '16px',
                        lineHeight: '25px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        resize: 'none',
                        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                        width: 'fit-content',
                        height: '35px',
                        fontFamily: 'Arial, sans-serif',
                        marginLeft: '10px'
                    }} />
                </StyledRoot>}    
                <Button variant="contained" startIcon={<Iconify icon="eva:plus-fill" />} onClick={() => setsState(!sstate)}>
                    הוספת שלב
                </Button>
            </MainStyledRoot>

          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
                <DataTable className="candidate-table"
                    columns={columns}
                    data={stageList}

                />
                {stageList.length === 0 && 
                    <FormControl fullWidth sx={{ alignItems: "center", mb: "6px"}}>
                        <strong>באפשרותך לשכפל תהליך משנה אחרת</strong>
                    <FormControl>
                    <Select
                            id="demo-simple-select"
                            value={"בחר שנה"}
                            onChange={onReqDup}>
                                <MenuItem value="בחר שנה">בחר שנה</MenuItem>
                            {yearList.map((val) =>
                                <MenuItem value={val}>{val}</MenuItem>
                            )}
                        </Select>
                    </FormControl>
                    </FormControl>
                }
            </TableContainer>
          </Scrollbar>

        </Card>
      </Container>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 1,
            width: 140,
            '& .MuiMenuItem-root': {
              px: 1,
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <MenuItem key={1}>
          <Iconify icon={'eva:edit-fill'} sx={{ mr: 2 }} />
          Edit
        </MenuItem>

        <MenuItem key={2}sx={{ color: 'error.main' }}>
          <Iconify icon={'eva:trash-2-outline'} sx={{ mr: 2 }} />
          Delete
        </MenuItem>
      </Popover>
    </>
        
    );
}