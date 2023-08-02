import { useState } from 'react';
// @mui
import { alpha } from '@mui/material/styles';
import { Button, Box, Divider, Typography, Stack, MenuItem, Avatar, IconButton, Popover, List } from '@mui/material';
// mocks_
import account from '../../../_mock/account';
import navConfig from '../nav/config';
import NavSection from '../../../components/nav-section/NavSection';
// ----------------------------------------------------------------------

const MENU_OPTIONS = [
  {
    label: 'Home',
    icon: 'eva:home-fill',
  },
  {
    label: 'Profile',
    icon: 'eva:person-fill',
  },
  {
    label: 'Settings',
    icon: 'eva:settings-2-fill',
  },
];

// const navConfig = [
//   {
//     title: 'מועמדים',
//     path: '/dashboard/user',
//     icon: icon('ic_user'),
//   },
//   {
//     title: 'עריכת שלבים',
//     path: '/stages',
//     icon: icon('ic_stages'),
//   },
// ];

// ----------------------------------------------------------------------

export default function AccountPopover() {
  const [open, setOpen] = useState(null);

  const handleOpen = (event) => {
    setOpen(event.currentTarget);
  };

  const handleClose = () => {
    setOpen(null);
  };

  return (
    <>
      <IconButton
        onClick={handleOpen}
        sx={{
          p: 0,
          ...(open && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              // borderRadius: '50%',
              position: 'absolute',
              // bgcolor: (theme) => alpha(theme.palette.grey[900], 0.8),
            },
          }),
        }}
      >
        <Avatar src={account.photoURL} alt="photoURL" />
      </IconButton>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 0,
            mt: 1.5,
            ml: 0.75,
            width: 180,
            '& .MuiMenuItem-root': {
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <NavSection data={navConfig}/>
      </Popover>
    </>
  );
}
