// apiRequest.js

import axios from 'axios';
import { refreshToken, logout } from './authService';

const API_URL = 'http://65.2.177.148/';

let isRefreshing = false;
let refreshQueue = [];

const apiRequest = async (method, url, data = null, headers = {}, navigate) => {
  const visibility = localStorage.getItem('visibility');
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
    logout(navigate);
    }

    const expirationTime = parseInt(localStorage.getItem('expirationTime'), 10);
    console.log('Expiry time of access token:', expirationTime);
    const now = Date.now();
    console.log('Current time:', now);
    const expiresIn = expirationTime - now;
    console.log('Expires in:', expiresIn);
    if (accessToken && expirationTime &&visibility==='visible'&& expiresIn > 0 && expiresIn < 300000) { // If expiration time is less than 5 minutes
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const newAccessToken = await refreshToken();
          localStorage.setItem('accessToken', newAccessToken);
          // Retry the queued requests with the new access token
          while (refreshQueue.length > 0) {
            const { resolve, reject, config } = refreshQueue.shift();
            config.headers.Authorization = `Bearer ${newAccessToken}`;
            try {
              const response = await axios(config);
              resolve(response.data);
            } catch (error) {
              reject(error);
            }
          }
        } catch (refreshError) {
          logout(navigate);
          throw refreshError;
        } finally {
          isRefreshing = false;
        }
      } 
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
    if (visibility==='visible'&&error.response && error.response.status === 401 && error.response.data.code === 'token_not_valid') {
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const newAccessToken = await refreshToken();
          localStorage.setItem('accessToken', newAccessToken);
          // Retry the queued requests with the new access token
          while (refreshQueue.length > 0) {
            const { resolve, reject, config } = refreshQueue.shift();
            config.headers.Authorization = `Bearer ${newAccessToken}`;
            try {
              const response = await axios(config);
              resolve(response.data);
            } catch (error) {
              reject(error);
            }
          }
        } catch (refreshError) {
          logout(navigate);
          throw refreshError;
        } finally {
          isRefreshing = false;
        }
      } else {
        // Queue the failed request for retry after token refresh
        const retryRequest = new Promise((resolve, reject) => {
          refreshQueue.push({ resolve, reject, config: error.config });
        });
        return retryRequest;
      }
    } else {
      logout(navigate);
    }
  }
};

export default apiRequest;
