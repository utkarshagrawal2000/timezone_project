// apiRequest.js

import axios from 'axios';
import { refreshToken, logout } from './authService';

const API_URL = 'http://65.2.177.148/';

let isRefreshing = false;
let refreshQueue = [];
// let refreshInterval;

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
          logout();
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
      throw error;
    }
  }
};


// export const startTokenRefresh = () => {
//   if (!refreshInterval) {
//     refreshInterval = setInterval(() => {
//       const accessToken = localStorage.getItem('accessToken');
//       const expirationTime = parseInt(localStorage.getItem('expirationTime'), 10);
//       console.log('Expiry time of access token:', expirationTime);
//       const now = Date.now();
//       console.log('Current time:', now);
//       const expiresIn = expirationTime - now;
//       console.log('Expiry time of access token:', expiresIn);
//       if (accessToken && expirationTime && expiresIn > 0 && expiresIn < 300000) { // If expiration time is less than 5 minutes
//         refreshToken();
//       }
//     }, 60000); // Check every 5 minutes
//   }
// };

// export const stopTokenRefresh = () => {
//   clearInterval(refreshInterval);
//   refreshInterval = null; // Reset refreshInterval to null to indicate that the interval is stopped
// };

export default apiRequest;
