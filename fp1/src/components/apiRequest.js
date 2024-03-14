// apiRequest.js

import axios from 'axios';
import { refreshToken, logout } from './authService';

const API_URL = 'http://65.2.177.148/';

const apiRequest = async (method, url, data = null, headers = {}) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found');
    }

    const response = await axios({
      method,
      url: API_URL + url,
      data,
      headers: {
        ...headers,
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401 && error.response.data.code === 'token_not_valid') {
      try {
        // Attempt token refresh
        const newAccessToken = await refreshToken();
        // Retry the original request with the new access token
        const response = await axios({
          method,
          url: API_URL + url,
          data,
          headers: {
            ...headers,
            Authorization: `Bearer ${newAccessToken}`,
          },
        });
        return response.data;
      } catch (refreshError) {
        // Refresh failed, logout user or handle the error accordingly
        console.error('Token refresh failed:', refreshError);
        logout(); // Logout user
        throw refreshError;
      }
    } else {
      // Handle other types of errors (e.g., network errors)
      throw error;
    }
  }
};

export default apiRequest;
