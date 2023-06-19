import React from "react";
import ReactDOM from "react-dom";
import styled from "styled-components";
import {
    Select,
    MenuItem,
} from "@mui/material";
// import Motion, { Move, Reveal } from "@element-motion/core";

const StyledContainer = styled.div`
  display: flex;
  flex-direction: row-reverse;
  align: center;
  /* Padding seems to fuck up the motion. WHY? */
  /* padding: 8px; */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
  background-color: transparent;
  border-radius: 10px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
`;

const StyledListItem = styled.div`
  padding: 16px;
  position: ${props => (props.isCollapsed ? "absolute" : "static")};
  top: 0;
  left: 0;
  right: 0;
`;

const StyledSelect = styled(Select)(({ theme }) => ({
    // textAlign: 'right',
    // alignItems: 'right',
    // alignContent: 'right',
    // flexDirection: 'row-reverse',
    // justifyContent: 'right',
    // display: 'flex',
    minWidth: '200px',
    // textDecorationColor: '#000',
}))

const StyledHeader = styled.div`
  flex-direction: column;
  display: flex;
  padding: 16px;
  position: relative;
  z-index: 222;
  background-color: #f5f5f5;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: 500;
  border-radius: 10px;
  min-width: 100px;

  > :first-child {
    margin-right: auto;
  }
`;

const StyledButton = styled.button`
  background-color: transparent;
  border: none;
`;

const ListItem = ({ isCollapsed, children }) => (
    <div>
        {!isCollapsed && <StyledListItem isCollapsed={isCollapsed}>
            {children}
        </StyledListItem>}
    </div >
);

const List = ({ answers, isCollapsed, setCollapsed, children }) => {
    const [ans, setAns] = React.useState("בחר שאלה")

    const ansChange = (tmp, e) => {
        setAns(e.props.children);
        setCollapsed(isCollapsed.map(
            (item, i) => i === e.props.value ? !item : true));
    }

    return(
    <div>
            <StyledContainer >
                <StyledHeader>
                    <StyledSelect
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={ans}
                    label="שאלות"
                    onChange={ansChange}>
                        {answers.map((answer, ind) => (
                            <MenuItem key={ind} value={ind}>{answer.question}</MenuItem>
                        ))}
                    </StyledSelect>
                    {/* {answers.map((answer, ind) =>
                        <StyledButton key={ind} onClick = {() => setCollapsed(isCollapsed.map(
                        (item, i) => i === ind ? !item : true))}>{answer.question}</StyledButton>
                    )} */}
                </StyledHeader>
                {children}
            </StyledContainer>
    </div>
);
}

// const listOfLen = (len, val) =>
// {
//     const list = [];
//     for (let i = 0; i < len; i+=1)
//     {
//         list.push(val);
//     }
//     return list;
// }


const Answers = ({answers}) => {

    const [isCollapsed, setCollapsed] = React.useState(Array(answers.length).fill(true));

    return (
        <List answers={answers} isCollapsed={isCollapsed} setCollapsed={setCollapsed}>
            {answers.map((answer, i) =>            
                <ListItem key={i} isCollapsed={isCollapsed[i]}>{answer.answer}</ListItem>
            )}
        </List>
    );
}
export default Answers

