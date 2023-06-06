import React, { useState } from 'react';
import Button from '@mui/joy/Button';
import {Menu, MenuItem } from '@material-ui/core';

const PopupMenu = ( title, options, handle ) => {
    // const classes = useStyles();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    const handleSelect = (options) =>
    {
        handle(options);
        handleClose();
    };


    return (
        <div>
            <Button onClick={handleClick}>
                {title}
            </Button>
            <Menu
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                {options.map((option) => (
                    <MenuItem key={option} onClick={() => handleSelect(option)}>
                        {option}
                    </MenuItem>
                ))}
            </Menu>
        </div>
    );
};

export default PopupMenu;
