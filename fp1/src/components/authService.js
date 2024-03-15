// authService.js

import axios from 'axios';
import { jwtDecode } from 'jwt-decode';


const API_URL = 'http://65.2.177.148/';

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');

  try {
    const response = await axios.post(`${API_URL}token/refresh/`, {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('accessToken', access);

    // Update the expiration time
    const expTime = jwtDecode(access).exp * 1000;
    localStorage.setItem('expirationTime', expTime.toString());

    return access;
  } catch (error) {
    console.error('Token refresh failed:', error);
    throw error;
  }
};

const logout = (navigate) => {
  console.log('logdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('expirationTime');
  localStorage.removeItem('privilege');
  navigate('/');
  // Additional cleanup if needed
};

export { refreshToken, logout };
