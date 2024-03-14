// Home.js

import React, { useState, useEffect } from 'react';
import apiRequest from './apiRequest'; // Import the apiRequest function
import TimezoneSelect from 'react-timezone-select';

function Home () {
  const [bookings, setBookings] = useState([]);
  const [formData, setFormData] = useState({
    room: '',
    start_time: '',
    end_time: ''
  });
  const [selectedTimezone, setSelectedTimezone] = useState('UTC');

  useEffect(() => {
    fetchBookings();
  }, [selectedTimezone]); // Reload bookings when timezone changes

  const fetchBookings = async () => {
    try {
      const headers = {
        'user-timezone': selectedTimezone // Set timezone in the request header
      };
      const response = await apiRequest('GET', 'get_bookings/', null, headers); // Use apiRequest instead of axios.get
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
        'user-timezone': selectedTimezone // Set timezone in the request header
      };
      await apiRequest('POST', 'create_booking/', formData, headers); // Use apiRequest instead of axios.post
      fetchBookings(); // Refresh bookings after successful submission
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
