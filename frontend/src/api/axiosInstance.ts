// import axios from 'axios';

// const API_URL = 'http://localhost:8000/'; // Backend URL

// const axiosInstance = axios.create({
//   baseURL: API_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// // Add interceptor to attach JWT token to every request if logged in
// axiosInstance.interceptors.request.use((config) => {
//   const token = localStorage.getItem('access_token');
//   if (token) {
//     config.headers['Authorization'] = `Bearer ${token}`;
//   }
//   return config;
// });



// export default axiosInstance;


import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/',  // your Django backend API URL
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

  const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL,
  });

// Add JWT token to headers on each request
axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default axiosInstance;
