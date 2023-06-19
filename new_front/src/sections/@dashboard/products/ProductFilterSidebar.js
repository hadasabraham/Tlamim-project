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
export const FILTER_GENDER_OPTIONS = ["ללא", "ממתין לטופס", "להתקשר", "חסר התייחסות", "הוסר"];
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

export default function ShopFilterSidebar({ openFilter, onOpenFilter, onCloseFilter, maxStage}) {
  const { filterName, onFilterName} = useState("");
  const { stage, onStageChange} = useState("");
  const { status, onStatusChange} = useState("");

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
                value={filterName}
                onChange={onFilterName}
                placeholder="אימייל"
              />
            </div>
            <div>
              <StyledSearch
                inputProps={{ min: 0, style: { textAlign: 'right' } }}
                value={filterName}
                onChange={onFilterName}
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
                    onChange={onStageChange}
                  >
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
                value={filterName}
                onChange={onFilterName}
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
                      onChange={onStatusChange}
                    >
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
                value={filterName}
                onChange={onFilterName}
                placeholder="הערות"
              />
            </div>
          </Stack>
        </Scrollbar>

        <Box sx={{ p: 3 }}>
          <Button
            fullWidth
            size="large"
            type="submit"
            color="inherit"
            variant="outlined"
            startIcon={<Iconify icon="ic:round-clear-all" />}
          >
            Clear All
          </Button>
        </Box>
      </Drawer>
    </>
  );
}
