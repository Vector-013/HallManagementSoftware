import './App.css';
import React from 'react';
import axios from 'axios';
import StudentRegister from "./components/StudentRegister"
import HallClerkRegister from "./components/HallClerkRegister"
import StudentView from "./components/StudentViewr"
import Logout from "./components/Logout"
import { BrowserRouter , Routes, Route} from "react-router-dom";
import Login from "./components/Login"


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function App() {

  function submitLogout(e) {
    e.preventDefault();
    client.post(
      "/api/logout",
      {withCredentials: true}
    )
  }
  
  return (
    <div>
        <BrowserRouter>
         <Routes>
            <Route
                exact
                path="/"
                element={<Login />}
            />
             <Route
                exact
                path="/hall-clerk-register"
                element={<HallClerkRegister />}
            />
             <Route
                exact
                path="/logout"
                element={<Logout />}
            />
             <Route
                exact
                path="/student-view"
                element={<StudentView />}
            />
            <Route
                exact
                path="/student-register"
                element={<StudentRegister/>}
            />
          </Routes>
       </BrowserRouter>  
        </div>
      )
}

export default App;