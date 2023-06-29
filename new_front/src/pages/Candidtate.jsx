import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // Removed "BrowserRouter as" from import
import {
    Card,
    Grid,
    Stack,
    Button,
    Container,
    Typography,
    AppBar, Toolbar,
} from '@mui/material';
import Textarea from '@mui/joy/Textarea';
import Iconify from '../components/iconify';

import Answers from '../layouts/dashboard/nav/answers';
import './Candidate.css';

function ProfilePage({ email }) {
    const [notesList, setNotesList] = useState([]);
    const [scoresList, setScoresList] = useState([]);
    const [flag, setFlag] = useState(false);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [candidatesInfo, setCandidate] = useState({ stages_info: [] });

    const fetchCandidate = async () => {
        const response = await fetch(`http://localhost:8001/candidate/${email}`);
        const data = await response.json();
        setCandidate(data);
    };

    const setNote = (index, value) => {
        if (candidatesInfo.grades.length > index) {
            onScoreNotesUpdate(index, value, candidatesInfo.grades[index].score);
        } else {
            onScoreNotesUpdate(index, value, 0);
        }
    };

    const setScore = (index, value) => {
        if (candidatesInfo.grades.length > index) {
            onScoreNotesUpdate(index, candidatesInfo.grades[index].notes, value);
        } else {
            onScoreNotesUpdate(index, "", value);
        }
    };

    const onScoreNotesUpdate = async (stageIndex, _notes, _score) => {
        const i = parseInt(stageIndex, 10);
        let score = _score;
        if (typeof score !== 'number') {
            score = parseInt(score, 10);
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                grade_parameter: {
                    email: email,
                    stage: i,
                    score: score,
                    notes: _notes,
                },
            }),
        };
        await fetch('http://localhost:8001/set/grade', requestOptions);
        fetchCandidate();
    };

    const onNextLevel = async (data) => {
        const passed = true;
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                decision_parameter: {
                    stage: data.current_stage,
                    email: data.email,
                    passed: passed,
                },
            }),
        };
        await fetch('http://localhost:8001/set/decision', requestOptions);
        fetchCandidate();
    };

    useEffect(() => {
        fetchCandidate();
    }, []);

    const removeCandidate = async (data) => {
        const confirmation = window.confirm('האם ברצונך להסיר מועמד זה?');
        if (!confirmation) {
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status_parameter: {
                    email: data.email,
                    status: 'הוסר',
                },
            }),
        };
        await fetch('http://localhost:8001/set/status', requestOptions);
    };

    const handleAnswerSelect = (answerIndex) => {
        setSelectedAnswer(answerIndex);
    };


    const PopupWindow = ({stage, answers, onClose }) => {
        return (
        <div className="popup-window">
        <AppBar position="fixed" color="default">
                <Stack direction="row" alignItems="center" justifyContent="space-between" ml={2} mr={2} mb={2} mt={2}>
                <Button variant="text" onClick={onClose}>
                    X
                </Button>
                <Typography variant="h6" align="center">
                    תשובות - שלב {stage}
                </Typography>
                </Stack>
        </AppBar>
        <Container sx={{ paddingTop: '60px' }}>
        <Card sx={{height: 'fixed', overflowY: 'scroll'}}>
          <Container>
                <Grid container spacing={2} sx={{ mt: 1, mb: 2 }}>
                {answers.map((answer, index) => (
                    <Grid item xs={12} key={index}>
                        <Card key={index}>
                            <Typography sx={{ p: 2, textAlign: 'right' }}>
                                <strong>{answer.question}</strong>
                                <p>{answer.answer}</p>
                            </Typography>
                        </Card>
                    </Grid>
                ))}
            </Grid>
          </Container>
        </Card>
        </Container>
      </div>
            // <div className="popup-window">
            //     <div className="popup-content">
            //         <button className="close-button" onClick={onClose}>
            //             Close
            //         </button>
            //         <h2>{stage} תשובות - שלב</h2>
            //         <ul>
            //             {answers.map((ans, index) => (
            //                 <li key={index}>
            //                     <strong>{ans.question}</strong>: {ans.answer}
            //                 </li>
            //             ))}
            //         </ul>
            //     </div>
            // </div>
        );
    };
    const [showPopup, setShowPopup] = useState(false);

    const togglePopup = () => {
        setShowPopup(!showPopup);
    };
    

    return (
        <section className="profile-section">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={3}>
                    <Button variant="contained" startIcon={<Iconify icon="ic:round-arrow-back-ios" />} onClick={() => window.location.href = 'http://localhost:3000/candidates/'}>
                        חזור
                    </Button>
                </Stack>
            <div className="dashboard">
                <Stack direction="row" spacing={2} mb={5}>
                    <Stack direction="column" spacing={1}>
                        <Grid item>
                            <Card>
                                <div className="dashboard-item" style={{ textAlign: 'center', alignContent: 'center' }}>
                                    <div className="dashboard-header">
                                        <h3>{candidatesInfo.name}</h3>
                                    </div>
                                    <div className="dashboard-body">
                                        <div className="profile-image">
                                            <img src="/assets/images/avatars/avatar_2.jpg" alt="Profile Avatar" />
                                        </div>
                                        <div className="profile-details">
                                            <h4 style={{ marginTop: '15px' }}>{candidatesInfo.email}</h4>
                                            <p>{candidatesInfo.phone}</p>
                                        </div>
                                    </div>
                                </div>
                            </Card>
                        </Grid>
                        <Grid item>
                            <Card>
                                <div className="dashboard-item">
                                    <div className="dashboard-body">
                                        <div className="contact-info" style={{ textAlign: 'center', alignContent: 'center', marginTop: '10px' }}>
                                            <div>
                                                <strong>שלב:</strong> {candidatesInfo.current_stage}
                                            </div>
                                            <div>
                                                <strong>ציון:</strong> {candidatesInfo.grade ? candidatesInfo.grade : 'אין'}
                                            </div>
                                            <div style={{ marginBottom: '10px' }}>
                                                <strong>סטטוס:</strong> {candidatesInfo.status}
                                            </div>
                                            <Button variant="contained" startIcon={<Iconify icon="ph:x-bold" />} onClick={removeCandidate}>
                                                הסר מועמד
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </Card>
                        </Grid>
                    </Stack>
                    <Stack direction="column" spacing={1}>
                        <Card>
                            {selectedAnswer !== null && (
                                <div className="dashboard-item" style={{ textAlign: 'right', alignContent: 'center' }}>
                                    <Stack direction="row" alignItems="center" justifyContent="space-between" mb={0} mt={0}>
                                        <Button variant="contained" startIcon={<Iconify icon="pepicons-pop:expand" />} onClick={togglePopup}>
                                        הרחב
                                        </Button>
                                        <h3>תשובות - שלב {selectedAnswer}</h3>
                                    </Stack>
                                    <div className="answer-details">
                                        <Answers answers={candidatesInfo.stages_info[selectedAnswer].answers} />
                                    </div>
                                </div>
                            )}
                            {selectedAnswer === null && (
                                <div className="dashboard-item" style={{ textAlign: 'center', alignContent: 'center' }}>
                                    <div className="dashboard-header" style={{ marginTop: '10px' }}>
                                        <h3>תשובות</h3>
                                    </div>
                                    <div className="answer-details" style={{ marginTop: '33px' }}>
                                        <p>בחר שלב לראות תשובות</p>
                                    </div>
                                </div>
                            )}
                        </Card>
                        <div className="dashboard-body-stages" style={{ textAlign: 'center', alignContent: 'center' }}>
                            <div className="card-window">
                                <div
                                    className="card-container"
                                    style={{
                                        display: 'flex',
                                        flexDirection: 'row-reverse',
                                    }}
                                >
                                    {candidatesInfo.stages_info.length > 0 ? (
                                        candidatesInfo.stages_info.map((stageInfo) => (
                                            <Card
                                                key={parseInt(stageInfo.stage, 10)}
                                                className={`answer-box ${selectedAnswer === parseInt(stageInfo.stage, 10) ? 'selected' : ''}`}
                                                onClick={() => handleAnswerSelect(parseInt(stageInfo.stage, 10))}
                                            >
                                                <div>
                                                    <h4>שלב {stageInfo.stage}</h4>
                                                    <select
                                                        style={{ textAlign: 'center', alignContent: 'center' }}
                                                        value={
                                                            candidatesInfo.grades.length > parseInt(stageInfo.stage, 10)
                                                                ? candidatesInfo.grades[parseInt(stageInfo.stage, 10)].score
                                                                : ''
                                                        }
                                                        onChange={(e) => setScore(parseInt(stageInfo.stage, 10), e.target.value)}
                                                    >
                                                        <option value="0">-</option>
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="4">4</option>
                                                        <option value="5">5</option>
                                                    </select>
                                                    <div>
                                                        <textarea
                                                            style={{ textAlign: 'right', alignContent: 'center' }}
                                                            className="textarea"
                                                            placeholder="הערות"
                                                            value={
                                                                candidatesInfo.grades.length > parseInt(stageInfo.stage, 10)
                                                                    ? candidatesInfo.grades[parseInt(stageInfo.stage, 10)].notes
                                                                    : ''
                                                            }
                                                            onChange={(e) => setNote(parseInt(stageInfo.stage, 10), e.target.value)}
                                                        />
                                                    </div>
                                                    <Stack direction="row-reverse" spacing={0}>
                                                        <button className="button secondary" onClick={() => onNextLevel(candidatesInfo)}>
                                                            העבר שלב
                                                        </button>
                                                    </Stack>
                                                </div>
                                            </Card>
                                        ))
                                    ) : (
                                        <>no data</>
                                    )}
                                </div>
                            </div>
                        </div>
                    </Stack>
                </Stack>
                    {showPopup && (
                        <div className="popup-container">
                            <PopupWindow
                                stage={selectedAnswer}
                                answers={candidatesInfo.stages_info[selectedAnswer].answers}
                                onClose={togglePopup}
                            />
                        </div>
                    )}
            </div>
            </Container>
        </section>
    );
};

export default ProfilePage;
