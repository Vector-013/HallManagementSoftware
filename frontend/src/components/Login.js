       
import Form from 'react-bootstrap/Form';
import React from 'react';
import { useState} from 'react';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function Login() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    function submitLogin(e) {
        e.preventDefault();
        client.post(
        "/api/login",
        {
            username: username,
            password: password
        }
        )
    }
    return (
    <div className="center">
            <Form onSubmit={e => submitLogin(e)}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="username" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                Login
                </Button>
            </Form>
            </div>
            
        )

  }

export default Login;