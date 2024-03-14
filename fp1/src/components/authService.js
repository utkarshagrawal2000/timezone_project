// authService.js

import axios from 'axios';

const API_URL = 'http://65.2.177.148/';

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');

  try {
    const response = await axios.post(`${API_URL}api/token/refresh/`, {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('accessToken', access);

    return access;
  } catch (error) {
    console.error('Token refresh failed:', error);
    throw error;
  }
};

const logout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  // Additional cleanup if needed
};

export { refreshToken, logout };
