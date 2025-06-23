import axios from 'axios';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

instance.interceptors.request.use(function (config) {
  // Add any request interceptors here if needed
  return config;
}, undefined)

instance.interceptors.response.use(
  function (value) {
    // Handle successful responses
    return value;
  },
  function (error) {
    // Handle errors

    return Promise.reject(error);
  });

  export default instance;