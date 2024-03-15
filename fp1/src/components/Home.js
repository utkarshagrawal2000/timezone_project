// Home.js

import React, { useState, useEffect } from 'react';
import apiRequest from './apiRequest';
import TimezoneSelect from 'react-timezone-select';
import { refreshToken } from './authService';
function Home() {
  const [bookings, setBookings] = useState([]);
  const [formData, setFormData] = useState({
    room: '',
    start_time: '',
    end_time: ''
  });
  const [selectedTimezone, setSelectedTimezone] = useState('UTC');
  const [lastTabSwitchTime, setLastTabSwitchTime] = useState(0);

  useEffect(() => {
    fetchBookings();
    const tabSwitchListener = () => {
      setLastTabSwitchTime(Date.now());
    };
    document.addEventListener('visibilitychange', tabSwitchListener);
    return () => {
      document.removeEventListener('visibilitychange', tabSwitchListener);
    };
  }, [selectedTimezone]);

  useEffect(() => {
    const refreshInterval = setInterval(() => {
      const accessToken = localStorage.getItem('accessToken');
      const expirationTime = localStorage.getItem('expirationTime');
      if (accessToken && expirationTime) {
        const expiresIn = parseInt(expirationTime) - Date.now();
        if (expiresIn < 300000) { // If expiration time is less than 5 minutes
          refreshToken();
        }
      }
    }, 300000); // Check every 5 minutes
    return () => clearInterval(refreshInterval);
  }, []);

  const fetchBookings = async () => {
    try {
      const headers = {
        'user-timezone': selectedTimezone
      };
      const response = await apiRequest('GET', 'get_bookings/', null, headers);
      setBookings(response);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleTimezoneChange = (timezone) => {
    setSelectedTimezone(timezone.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const headers = {
        'user-timezone': selectedTimezone
      };
      await apiRequest('POST', 'create_booking/', formData, headers);
      fetchBookings();
      setFormData({
        room: '',
        start_time: '',
        end_time: ''
      });
    } catch (error) {
      console.error('Error submitting booking:', error);
    }
  };

  return (
    <div>
      <h1>Hotel Bookings</h1>
      <label htmlFor="timezone">Select Timezone:</label>
      <TimezoneSelect
        id="timezone"
        value={selectedTimezone}
        onChange={handleTimezoneChange}
      />
      <form onSubmit={handleSubmit}>
        <label htmlFor="room">Room:</label>
        <input type="text" id="room" name="room" value={formData.room} onChange={handleChange} required />
        <label htmlFor="start_time">Start Time:</label>
        <input type="datetime-local" id="start_time" name="start_time" value={formData.start_time} onChange={handleChange} required />
        <label htmlFor="end_time">End Time:</label>
        <input type="datetime-local" id="end_time" name="end_time" value={formData.end_time} onChange={handleChange} required />
        <button type="submit">Book Room</button>
      </form>
      <h2>Current Bookings</h2>
      <ul>
        {bookings.map(booking => (
          <li key={booking.id}>
            Room: {booking.room}, 
            Start Time: {booking.start_time}, 
            End Time: {booking.end_time},
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;
