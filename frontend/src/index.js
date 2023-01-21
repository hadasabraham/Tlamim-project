import React from "react";
import ReactDOM from "react-dom";
import { ChakraProvider } from "@chakra-ui/react";
import { BrowserRouter as Router, Route, Routes, useParams } from 'react-router-dom'

import Header from "./components/Header";
import CandidatesTable from "./components/CandidatesTable";  
import Candidate from "./components/candidates/candidates";

function App() {
  return (
    <CandidatesTable /> 
  )
}

function PageNotFound () {
  return (
    <ChakraProvider>
      {Header("Page Not Found")}
    </ChakraProvider>
  )
}

function Lcandidate(){
  const params = useParams();
  return (
      <Candidate email={params.email}/>
    );
}

const rootElement = document.getElementById("root")
ReactDOM.render(
  <Router>
    <div>
      <Routes>
        <Route path="/candidate/:email" element={<Lcandidate />} />
        <Route path="/" element={<App />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </div>
  </Router>
  , rootElement
)