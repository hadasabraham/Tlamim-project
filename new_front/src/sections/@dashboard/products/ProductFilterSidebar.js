import PropTypes from 'prop-types';
import { useState } from 'react';
import { styled, alpha } from '@mui/material/styles';

// @mui
import {
  Box,
  Radio,
  Stack,
  Button,
  Drawer,
  Rating,
  Divider,
  Checkbox,
  FormGroup,
  IconButton,
  Typography,
  RadioGroup,
  FormControlLabel,
  OutlinedInput,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

// import { Toolbar, Tooltip, IconButton, Typography, OutlinedInput, InputAdornment } from '@mui/material';

// components
import Iconify from '../../../components/iconify';
import Scrollbar from '../../../components/scrollbar';
import { ColorMultiPicker } from '../../../components/color-utils';

// ----------------------------------------------------------------------

export const SORT_BY_OPTIONS = [
  { value: 'featured', label: 'Featured' },
  { value: 'newest', label: 'Newest' },
  { value: 'priceDesc', label: 'Price: High-Low' },
  { value: 'priceAsc', label: 'Price: Low-High' },
];
export const FILTER_GENDER_OPTIONS = ["ממתין לטופס", "להתקשר", "חסר התייחסות", "הוסר"];
export const FILTER_CATEGORY_OPTIONS = ['All', 'Shose', 'Apparel', 'Accessories'];
export const FILTER_RATING_OPTIONS = ['up4Star', 'up3Star', 'up2Star', 'up1Star'];
export const FILTER_PRICE_OPTIONS = [
  { value: 'below', label: 'Below $25' },
  { value: 'between', label: 'Between $25 - $75' },
  { value: 'above', label: 'Above $75' },
];
export const FILTER_COLOR_OPTIONS = [
  '#00AB55',
  '#000000',
  '#FFFFFF',
  '#FFC0CB',
  '#FF4842',
  '#1890FF',
  '#94D82D',
  '#FFC107',
];

// ----------------------------------------------------------------------

const StyledSearch = styled(OutlinedInput)(({ theme }) => ({
  width: 230,
  textAlign: 'center',
  alignContent: 'center',
  alignItems: 'center',
  transition: theme.transitions.create(['box-shadow', 'width'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.shorter,
  }),
  '& fieldset': {
    borderWidth: `1px !important`,
    borderColor: `${alpha(theme.palette.grey[500], 0.32)} !important`,
  },
}));

const StyledSelect = styled(Select) (({ theme }) => ({
  textAlign: 'right',
  alignItems: 'right',
  alignContent: 'right',
  flexDirection: 'row-reverse',
  justifyContent: 'right',
  display: 'flex',
}))



ShopFilterSidebar.propTypes = {
  openFilter: PropTypes.bool,
  onOpenFilter: PropTypes.func,
  onCloseFilter: PropTypes.func,
  maxStage: PropTypes.number,
};

const arrayRange = (start, stop, step) =>
  Array.from(
    { length: (stop - start) / step + 1 },
    (value, index) => start + index * step
  );

export default function ShopFilterSidebar({ openFilter, onOpenFilter, onCloseFilter, maxStage, setFilters}) {
  const [ filterName, onFilterName] = useState("");
  const [ filterEmail, onFilterEmail ] = useState("");
  const [ filterPhone, onFilterPhone ] = useState("");
  const [ filterNotes, onFilterNotes ] = useState("");
  const [ stage, onStageChange ] = useState("");
  const [ status, onStatusChange ] = useState("");
  const filterSelect = () => {
    let filters = "";
    if (filterEmail !== "" && filterEmail !== undefined) {
      filters = `אימייל=${filterEmail}`
    }
    if (filterName !== "" && filterName !== undefined) {
      if (filters !== "") {
        filters = `${filters} `
      }
      filters = `${filters}שם=${filterName}`
    }
    if (filterPhone !== "" && filterPhone !== undefined) {
      if (filters !== "") {
        filters = `${filters} `
      }
      filters = `${filters}טלפון=${filterPhone}`
    }
    // if (filterNotes !== "") {
    //   if (filters !== "") {
    //     const filters = `${filters} `
    //   }
    //   const filters = `${filters}notes=${filterNotes}}`
    // }
    if (stage !== "" && stage !== undefined) {
      if (filters !== "") {
        filters = `${filters} `
      }
      filters = `${filters}שלב=${stage}`
    }
    if (status !== "" && status !== undefined && status !== "ללא") {
      if (filters !== "") {
        filters = `${filters} `
      }
      filters = `${filters}סטטוס=${status}`
    }
    onCloseFilter();
    setFilters(filters);
  }

  return (
    <>
      <Button disableRipple color="inherit" endIcon={<Iconify icon="ic:round-filter-list" />} onClick={onOpenFilter}>
        Filters&nbsp;
      </Button>

      <Drawer
        anchor="right"
        open={openFilter}
        onClose={onCloseFilter}
        PaperProps={{
          sx: { width: 280, border: 'none', overflow: 'hidden' },
        }}
      >
        <Stack direction="row" children={{style: {textAlign: 'right'}}} justifyContent="space-between" sx={{ px: 1, py: 2 }}>
          <IconButton onClick={onCloseFilter}>
            <Iconify icon="eva:close-fill" />
          </IconButton>
          <Typography variant="subtitle1" sx={{ ml: 1 }}>
            סינונים
          </Typography>
        </Stack>

        <Divider />

        <Scrollbar>
          <Stack spacing={3} sx={{ p: 3 }}>
            <div>
              <StyledSearch
                inputProps={{ min: 0, style: { textAlign: 'right' } }}
                value={filterEmail}
                onChange={(e)=>onFilterEmail(e.target.value)}
                placeholder="אימייל"
              />
            </div>
            <div>
              <StyledSearch
                inputProps={{ min: 0, style: { textAlign: 'right' } }}
                value={filterName}
                onChange={(e) => onFilterName(e.target.value)}
                placeholder="שם"
              />
            </div>
            <div>
              <Box sx={{ minWidth: 120}}>
                <FormControl fullWidth>
                  <InputLabel id="demo-simple-select-label">שלב</InputLabel>
                  <StyledSelect
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={stage}
                    label="שלב"
                    onChange={(e)=>onStageChange(e.target.value)}
                  >
                    <MenuItem value={""}>{"ללא"}</MenuItem>
                    {arrayRange(0, maxStage, 1).map((item) => (
                      <MenuItem value={item}>{item}</MenuItem>
                    ))}
                  </StyledSelect>
                </FormControl>
              </Box>
            </div>
            <div>
              <StyledSearch
                inputProps={{ min: 0, style: { textAlign: 'right' } }}
                value={filterPhone}
                onChange={(e) => onFilterPhone(e.target.value)}
                placeholder="טלפון"
              />
            </div>
            <div>
                <Box sx={{ minWidth: 120 }}>
                  <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">סטטוס</InputLabel>
                    <StyledSelect
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={status}
                      label="סטטוס"
                    onChange={(e) => onStatusChange(e.target.value)}
                    >
                    <MenuItem value={"ללא"}>{""}</MenuItem>
                      {FILTER_GENDER_OPTIONS.map((item) => (
                        <MenuItem value={item}>{item}</MenuItem>
                      ))}
                    </StyledSelect>
                  </FormControl>
                </Box>
            </div>
            <div>
              <StyledSearch
                inputProps={{ min: 0, style: { textAlign: 'right' } }}
                value={filterNotes}
                onChange={(e)=>onFilterNotes(e.target.value)}
                placeholder="הערות"
              />
            </div>
          </Stack>
        </Scrollbar>
        <Button 
        variant="contained" startIcon={<Iconify icon="ph:x-bold" />} 
          onClick={filterSelect}>
          חפש
        </Button>
        <Box sx={{ p: 3 }}>
          <Button
            fullWidth
            size="large"
            type="submit"
            color="inherit"
            variant="outlined"
            startIcon={<Iconify icon="ic:round-clear-all" />}
            onSelect={filterSelect}
          >
            חפש
          </Button>
        </Box>
        <Box sx={{ p: 3 }}>
          <Button
            fullWidth
            size="large"
            type="submit"
            color="inherit"
            variant="outlined"
            startIcon={<Iconify icon="ic:round-clear-all" />}
            onClick={(e) => {onFilterEmail(""); onFilterName(""); onFilterPhone(""); onFilterNotes(""); onStageChange(""); onStatusChange("");}}
          >
            מחק סינונים
          </Button>
        </Box>
      </Drawer>
    </>
  );
}
