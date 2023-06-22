import { Helmet } from 'react-helmet-async';
import { filter } from 'lodash';
import { sentenceCase } from 'change-case';
import React, { useEffect, useState, Component } from "react";
import Textarea from '@mui/joy/Textarea';
// @mui
import {
  Card,
  Table,
  Stack,
  Paper,
  Avatar,
  Button,
  Popover,
  Checkbox,
  TableRow,
  MenuItem,
  TableBody,
  TableCell,
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
import dataTable from '../components/chart/dataTable';
// sections
import { UserListHead, UserListToolbar } from '../sections/@dashboard/user';
// mock
import USERLIST from '../_mock/user';
import SvgColor from '../components/svg-color';

// ----------------------------------------------------------------------

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(array, comparator, query) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query) {
    return filter(array, (_user) => _user.name.toLowerCase().indexOf(query.toLowerCase()) !== -1);
  }
  return stabilizedThis.map((el) => el[0]);
}

export default function UserPage() {
  const [generalnotes, setGeneralNotes] = useState("")
  const [candidateslist, setCandidateList] = useState([])
  const [cond, setCond] = useState("הכול")
  const fetchTodos = async (value) => {
    const response = await fetch(`http://localhost:8001/candidates/search/${value}`)
    const data = await response.json()
    setCandidateList(data)
  }
  const [state, setState] = useState(false)
  const [menu, setMenu] = useState(false)
  const onMenu = () => {
    setMenu(!menu);
  }
  const handleSearch = (value) => {
    if (value === "") {
      setCond("הכול")
      fetchTodos("הכול")
    }
    else {
      setCond(value)
      fetchTodos(value)
    }
  }
  const refresh = () => {
    fetchTodos(cond)
  }

  const onStatusChange = async (email, event) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "status_parameter": { "email": email, "status": event.target.value } })
    };
    await fetch('http://localhost:8001/set/status', requestOptions);
    refresh();
  };

  const onGeneralNotesChange = async (email, event) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "notes_parameter": { "email": email, "notes": event.target.value } })
    };
    await fetch('http://localhost:8001/set/general_notes', requestOptions);
    refresh();
  };

  const onExport = () => {
    setState(!state);
  }

  const onToggle = async (value) => {
    if (value === false) {
      onExport();
      return;
    }
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "export": { "name": value, "condition": cond } })
    };
    await fetch('http://localhost:8001/export/', requestOptions);
    onExport();
  };

  const onRefresh = async () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "request": {} })
    };
    await fetch('http://localhost:8001/refresh/all', requestOptions);
    fetchTodos("הכול");
  };

  useEffect(() => {
    refresh();
  }, [])

  const onAddStage = () => {
    window.location.href = 'http://localhost:3000/addStages';
  };







  const [open, setOpen] = useState(null);

  const [page, setPage] = useState(0);

  const [selected, setSelected] = useState([]);

  const [filterName, setFilterName] = useState('');

  const handleCloseMenu = () => {
    setOpen(null);
  };

  const handleFilterByName = (event) => {
    setPage(0);
    setFilterName(event.target.value);
  };

  return (
    <>
      <Helmet>
        <title> Candidates | tlamim </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Button variant="contained" startIcon={<Iconify icon="eva:refresh-fill" />} onClick={onRefresh}>
            רענן
          </Button>
          <Typography variant="h4" gutterBottom>
            <Stack direction="row" alignItems="right">
              מועמדים
              <img src={'/assets/icons/navbar/ic_user.svg'} alt="מועמדים" style={{ width: 40, height: 40 }} />
            </Stack>
          </Typography>
        </Stack>

        <Card>
          <UserListToolbar numSelected={selected.length} filterName={filterName} onFilterName={handleFilterByName} setFilters={handleSearch}/>

          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              {/* <dataTable data={candidateslist} onStatusChange={onStatusChange} sentGeneralNotes={onGeneralNotesChange}/> */}
              {dataTable(candidateslist, onStatusChange, onGeneralNotesChange)}
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

        <MenuItem key={2} sx={{ color: 'error.main' }}>
          <Iconify icon={'eva:trash-2-outline'} sx={{ mr: 2 }} />
          Delete
        </MenuItem>
      </Popover>
    </>
  );
}
