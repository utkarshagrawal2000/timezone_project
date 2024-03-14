import React, { useState } from 'react';
import {  useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await fetch('http://65.2.177.148/user/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Login successful, store token in localStorage
                localStorage.setItem('accessToken', data.token.access);
                localStorage.setItem('refresh', data.token.refresh);
                localStorage.setItem('privilege', data.token.privilege);
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
                <label>email:</label>
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
