import Form from 'react-bootstrap/Form';
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import { useNavigate } from "react-router-dom";


const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function HallClerkRegister() {

    let navigate = useNavigate()

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [mobile, setMobile] = useState('');
    const [address, setAddress] = useState('');

   
    function submitRegistration(e) {
    e.preventDefault();
    client.post(
      "/api/hall-clerk-register",
      {
        email: email,
        username: username,
        password: password,
        first_name: first_name,
        last_name:last_name,
        address:address,
        mobile:mobile
      }
    )
    navigate("/", {replace: true});
    }
  
  return (
       <div className="center">
          <Form onSubmit={e => submitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter username" value={username} onChange= {e=>setUsername(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
            </Form.Group>
             <Form.Group className="mb-3" controlId="formFirstName">
              <Form.Label>First Name</Form.Label>
              <Form.Control type="text" placeholder="Enter first name" value={first_name} onChange={e=>setFirstName(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formLastName">
              <Form.Label>Last Name</Form.Label>
              <Form.Control type="text" placeholder="Enter last name" value={last_name} onChange={e=>setLastName(e.target.value)} />
            </Form.Group>
             <Form.Group className="mb-3" controlId="formEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e=>setEmail(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formMobile">
              <Form.Label>Mobile No.</Form.Label>
              <Form.Control type="text" placeholder="Enter mobile no." value={mobile} onChange={e=>setMobile(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formAddress">
              <Form.Label>Address</Form.Label>
              <Form.Control type="text" placeholder="Enter address" value={address} onChange={e=>setAddress(e.target.value)} />
            </Form.Group>           
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>     
      )}

export default HallClerkRegister;