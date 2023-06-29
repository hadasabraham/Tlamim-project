import React from "react";
import styled from "styled-components";
import { Select, MenuItem } from "@mui/material";

const StyledContainer = styled.div`
  display: flex;
  flex-direction: row-reverse;
  align: center;
  /* Padding seems to fuck up the motion. WHY? */
  padding: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
  background-color: transparent;
  border-radius: 10px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
`;

const StyledListItem = styled.div`
  padding: 16px;
  position: ${(props) => (props.isCollapsed ? "absolute" : "static")};
  top: 0;
  left: 0;
  right: 0;
`;

const StyledSelect = styled(Select)(({ theme }) => ({
    minWidth: "200px",
}));

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
        {!isCollapsed && <StyledListItem isCollapsed={isCollapsed}>{children}</StyledListItem>}
    </div>
);

const List = ({ answers, isCollapsed, setCollapsed, children }) => {
    const [selectedQuestion, setSelectedQuestion] = React.useState("בחר שאלה");

    const handleQuestionChange = (event) => {
        const selectedValue = event.target.value;
        setSelectedQuestion(selectedValue);
        const selectedQuestionIndex = answers.findIndex((answer) => answer.question === selectedValue);
        const updatedCollapsed = isCollapsed.map((item, index) => index === selectedQuestionIndex ? !item : true);
        setCollapsed(updatedCollapsed);
    };

    return (
        <div>
            <StyledContainer>
                <StyledSelect
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={selectedQuestion}
                    onChange={handleQuestionChange}
                >
                    <MenuItem value="בחר שאלה">בחר שאלה</MenuItem>
                    {answers.map((answer, ind) => (
                        <MenuItem key={ind + 1} value={answer.question}>
                            {answer.question}
                        </MenuItem>
                    ))}
                </StyledSelect>
                {children}
            </StyledContainer>
        </div>
    );
};

const Answers = ({ answers }) => {
    const [isCollapsed, setCollapsed] = React.useState(Array(answers.length).fill(true));

    return (
        <List answers={answers} isCollapsed={isCollapsed} setCollapsed={setCollapsed}>
            {answers.map((answer, i) => (
                <ListItem key={i} isCollapsed={isCollapsed[i]}>
                    {answer.answer}
                </ListItem>
            ))}
        </List>
    );
};

export default Answers;
