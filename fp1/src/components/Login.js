// Login.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {jwtDecode} from "jwt-decode";

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await fetch('http://localhost:8000/user/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Login successful, store token and expiration time in localStorage
                localStorage.setItem('accessToken', data.token.access);
                localStorage.setItem('refreshToken', data.token.refresh);
                localStorage.setItem('privilege', data.token.privilege);
                // Parse the expiration time to ensure it is a number
                const expirationTime = jwtDecode(data.token.access).exp * 1000;
                console.log(expirationTime);
                // const expirationTime = parseInt(data.token.access_exp); // Assuming access_exp is in seconds
                if (!isNaN(expirationTime)) {
                    localStorage.setItem('expirationTime', expirationTime.toString());
                } else {
                    console.error('Invalid expiration time received:', data.token.access_exp);
                }
                // Redirect to home page
                navigate('/home');
            } else {
                // Login failed, display error message
                setError(data.errors.non_field_errors[0]);
            }
        } catch (error) {
            console.error('Error logging in:', error);
            setError('An error occurred while logging in. Please try again later.');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <div>
                <label>Email:</label>
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div>
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button onClick={handleLogin}>Login</button>
            {error && <div style={{ color: 'red' }}>{error}</div>}
        </div>
    );
};

export default Login;
