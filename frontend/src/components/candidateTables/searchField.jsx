import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import TypeChecker from 'typeco';
import TextField from '@mui/material/TextField';
import Button from '@mui/joy/Button';
import "./searchField.css";
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

const names = [
    'Oliver Hansen',
    'Van Henry',
    'April Tucker',
    'Ralph Hubbard',
    'Omar Alexander',
    'Carlos Abbott',
    'Miriam Wagner',
    'Bradley Wilkerson',
    'Virginia Andrews',
    'Kelly Snyder',
];

const ENTER_KEY = 13;
const SEARCH_BUTTON_EDGE = 35;

const searchFieldStyle = {
    border: '1px #ddd solid',
    borderRadius: '30px',
    display: 'inline-flex',
    justifyContent: 'space-between',
    height: SEARCH_BUTTON_EDGE,
};

const searchFieldButtonStyle = (disabled) => ({
    height: SEARCH_BUTTON_EDGE - 2, // reduces 2px because of top and bottom border
    width: SEARCH_BUTTON_EDGE - 2,
    outline: 'none',
    backgroundColor: 'white',
    cursor: disabled ? 'auto' : 'pointer',
    padding: 5,
    boxSizing: 'border-box',
    appearance: 'none',
    border: 'none',
    borderLeft: '1px #ddd solid',
    borderRadius: '50px',
});

const searchFieldInputStyle = {
    outline: 'black',
    border: 'none',
    borderRadius: '30px',
    fontSize: 18,
    padding: '0 16px',
    flex: 1,
    color: '#5a5a5a',
    fontWeight: 100,
    height: SEARCH_BUTTON_EDGE - 3,
    width: "max-content",
};

const SearchIcon = () => {
    const iconEdge = Math.ceil(SEARCH_BUTTON_EDGE * 0.60);
    const searchIconStyle = {
        fill: '#727272',
    };
    return (
        <svg
            version="1.1"
            x="0px"
            y="0px"
            width={iconEdge}
            height={iconEdge}
            viewBox="0 0 635 635"
            style={searchIconStyle}
        >
            <g>
                <path d="M255.108,0C119.863,0,10.204,109.66,10.204,244.904c0,135.245,109.659,244.905,244.904,244.905
          c52.006,0,100.238-16.223,139.883-43.854l185.205,185.176c1.671,1.672,4.379,1.672,5.964,0.115l34.892-34.891
          c1.613-1.613,1.47-4.379-0.115-5.965L438.151,407.605c38.493-43.246,61.86-100.237,61.86-162.702
          C500.012,109.66,390.353,0,255.108,0z M255.108,460.996c-119.34,0-216.092-96.752-216.092-216.092
          c0-119.34,96.751-216.091,216.092-216.091s216.091,96.751,216.091,216.091C471.199,364.244,374.448,460.996,255.108,460.996z"
                />
            </g>
        </svg>
    );
};

const SearchField = ({
    classNames,
    searchText,
    placeholder,
    disabled,
    onChange,
    onEnter,
    onSearchClick,
    onBlur,
}) => {
    const [value, setValue] = useState(searchText);
    const [personName, setPersonName] = React.useState([]);

    useEffect(() => {
        setValue(searchText);
    }, [searchText, setValue]);

    const onChangeHandler = (value) => {
        setValue(value);
        if (TypeChecker.isFunction(onChange)) {
            onChange(value);
        }
    };

    const onEnterHandler = useCallback((event) => {
        const isEnterPressed = event.which === ENTER_KEY
            || event.keyCode === ENTER_KEY;
        setPersonName(typeof personName === 'string' ? (personName + event.target.value).split(',') : personName + event.target.value)
        if (isEnterPressed && TypeChecker.isFunction(onEnter)) {
            onEnter(event.target.value, event);
        }
    }, [onEnter]);

    const onSearchClickHandler = useCallback(() => {
        if (TypeChecker.isFunction(onSearchClick)) {
            onSearchClick(value);
        }
    }, [onSearchClick, value]);

    const onBlurHandler = useCallback((event) => {
        if (TypeChecker.isFunction(onBlur)) {
            onBlur(event.target.value, event);
        }
    }, [onBlur]);

    const className = `react-search-field`;

    const handleChange = (event) => {
        const {
            target: { value },
        } = event;
        setPersonName(
            // On autofill we get a stringified value.
            typeof value === 'string' ? value.split(',') : value,
        );
    };
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedKeyword, setSelectedKeyword] = useState("");
    const [keywords, setKeywords] = useState(["אימייל", "שם", "שלב", "סטטוס", "תאריך", "טלפון", "ממתינים לטיפול", "מועמדים שהוסרו"]);
    const [isHidden, setIsHidden] = useState(true)
    const style_inp = () =>{
        if (isHidden) return "hidden";
        return "text";
    };

    const handleSearch = () => {
        // perform search using searchTerm and selectedKeyword
        const tmp_val = `${selectedKeyword}=${value}`;
        if (searchTerm != 0) {
            setSearchTerm(`${searchTerm} ${tmp_val}`.trim());
            onChange(`${searchTerm} ${tmp_val}`.trim());
        }
        else {
            setSearchTerm(`${tmp_val}`.trim());
            onChange(`${tmp_val}`.trim());
        }
        setIsHidden(true);
        setValue("");
    };

    const handleSelectChange = (event) => {
        setSelectedKeyword(event.target.value);
        const tmp_val = event.target.value;
        if (event.target.value !== "ממתינים לטיפול" && event.target.value !== "מועמדים שהוסרו")
        {
            setIsHidden(false);
            return;
        }
        setIsHidden(true);
        setValue("");
        if (searchTerm != 0)
        {
            if (event.target.value === "ממתינים לטיפול")
            {
                setSearchTerm(`${searchTerm} ${"חסרים"}`.trim());
                onChange(`${searchTerm} ${"חסרים"}`.trim());
            }
            else
            {
                setSearchTerm(`${searchTerm} ${"סטטוס=הוסר"}`.trim());
                onChange(`${searchTerm} ${"סטטוס=הוסר"}`.trim());
            }

        }
        else
        {
            if (event.target.value === "ממתינים לטיפול") {
                setSearchTerm(`${"חסרים"}`.trim());
                onChange(`${"חסרים"}`.trim());
            }
            else {
                setSearchTerm(`${"סטטוס=הוסר"}`.trim());
                onChange(`${"סטטוס=הוסר"}`.trim());
            }
        }
    };

    const handleInpChange = (keyword, value) => {
        const newSearchTerm = searchTerm.replace(keyword, value).trim();
        setSearchTerm(newSearchTerm);
        onChange(newSearchTerm);
    };

    const handleRemoveKeyword = (keyword) => {
        const newSearchTerm = searchTerm.replace(keyword, "").trim();
        setSearchTerm(newSearchTerm);
        onChange(newSearchTerm);
    };

    return (
        <div className="search-bar-container">
            <div className="keyword-select-container">
                {!isHidden && 
                <button onClick={handleSearch} className="green-button">
                    הוסף
                </button>
                // <button className="search-button" onClick={handleSearch} color='green'>
                //     הוסף
                // </button>
                }
                {!isHidden &&
                <input
                    className='hidden_input'
                    style = {{textAlign: "right"}}
                    type={style_inp()}
                    placeholder="ערך סינון"
                    value={value}
                    onChange={(event) => setValue(event.target.value)}
                />}
                {/* <label htmlFor="keyword-select">Select a Keyword:</label> */}
                <select
                    // multiple={true}
                    id="keyword-select"
                    value={selectedKeyword}
                    onChange={handleSelectChange}
                >
                    <option>בחר מילת סינון</option>
                    {keywords.map((keyword) => (
                        <option key={keyword} value={keyword}>
                            {keyword}
                        </option>
                    ))}
                </select>
            </div>
            <div className="search-bar-input-container">
                {searchTerm.split(" ").map((term, index) => (
                    <div key={index} className="pill-container">
                        <input className='pill' 
                        disabled={true}
                        style={{ width: `${(term === "חסרים" ? "ממתינים לטיפול" : term).length+2}ch`}}
                        type="text" value={term === "חסרים" ? "ממתינים לטיפול" : term} 
                            onChange={(event) => handleInpChange(term, event.target.value)}/>
                        {
                        // keywords.includes(term.toLowerCase()) && 
                        (
                            <button
                                className="remove-button"
                                onClick={() => handleRemoveKeyword(term)}
                            >
                                X
                            </button>
                        )}
                    </div>
                ))}

            </div>
        </div>
    );

    return (
        <div className="search-bar-container" style={{ display: "grid", gridTemplateColumns: "0fr 0fr 0fr" }}>
            <div className="keyword-select-container">
                <select
                    className='selection-select'
                    id="keyword-select"
                    value={selectedKeyword}
                    onChange={handleSelectChange}
                >
                    <option value="">-- Select a Keyword --</option>
                    {keywords.map((keyword) => (
                        <option key={keyword} value={keyword}>
                            {keyword}
                        </option>
                    ))}
                </select>
            </div>
            <div
                className={className}
                style={searchFieldStyle}
            >
                <input
                    className="react-search-field-input"
                    style={searchFieldInputStyle}
                    onChange={(event) => setSearchTerm(event.target.value)}
                    onKeyPress={onEnterHandler}
                    onBlur={onBlurHandler}
                    placeholder={placeholder}
                    type="text"
                    value={searchTerm}
                    disabled={disabled}
                />
                <button
                    className="react-search-field-button"
                    type="button"
                    aria-label="search button"
                    style={searchFieldButtonStyle(disabled)}
                    onClick={onSearchClickHandler}
                    disabled={disabled}
                >
                    <SearchIcon />
                </button>
            </div>
                {/* <input className='react-search-field'
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(event) => setSearchTerm(event.target.value)}
                /> */}
            <Button onClick={handleSearch}>
                Search
            </Button>
        </div>
    );
    return (
        <div>
            <FormControl sx={{ m: 1, width: 300 }}>
                <InputLabel id="demo-multiple-checkbox-label">Tag</InputLabel>
                <input
                    className="react-search-field-input"
                    style={searchFieldInputStyle}
                    onChange={onChangeHandler}
                    onKeyPress={onEnterHandler}
                    onBlur={onBlurHandler}
                    placeholder={placeholder}
                    type="text"
                    value={value}
                    disabled={disabled}
                />
                <Select
                    labelId="demo-multiple-checkbox-label"
                    id="demo-multiple-checkbox"
                    multiple
                    value={personName}
                    onChange={handleChange}
                    input={<OutlinedInput label="Tag" />}
                    renderValue={(selected) => selected.join(', ')}
                    MenuProps={MenuProps}
                >
                    {names.map((name) => (
                        <MenuItem key={name} value={name}>
                            <Checkbox checked={personName.indexOf(name) > -1} />
                            <ListItemText primary={name} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
    return (
        <>
            {/* <TextField
                id="outlined-select-currency"
                select
                label="Select"
                defaultValue="EUR"
                helperText="Please select your currency"
            >
                {currencies.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                        {option.label}
                    </MenuItem>
                ))}
            </TextField> */}
        <div
            className={className}
            style={searchFieldStyle}
        >
            <input
                className="react-search-field-input"
                style={searchFieldInputStyle}
                onChange={onChangeHandler}
                onKeyPress={onEnterHandler}
                onBlur={onBlurHandler}
                placeholder={placeholder}
                type="text"
                value={value}
                disabled={disabled}
            />
            <button
                className="react-search-field-button"
                type="button"
                aria-label="search button"
                style={searchFieldButtonStyle(disabled)}
                onClick={onSearchClickHandler}
                disabled={disabled}
            >
                <SearchIcon />
            </button>
            </div></>
    );
};

SearchField.propTypes = {
    classNames: PropTypes.string,
    searchText: PropTypes.string,
    placeholder: PropTypes.string,
    disabled: PropTypes.bool,
    onChange: PropTypes.func,
    onEnter: PropTypes.func,
    onSearchClick: PropTypes.func,
    onBlur: PropTypes.func,
};

SearchField.defaultProps = {
    classNames: '',
    searchText: '',
    placeholder: 'Search',
    disabled: false,
    onChange: null,
    onEnter: null,
    onSearchClick: null,
    onBlur: null,
};

export default SearchField;