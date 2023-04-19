import axios from "axios";

import config from "../header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";
const axiosInstance = axios.create({
  baseURL: instanceUrl,
});

const requestService = {
  getSenderList() {
    axiosInstance.interceptors.request.use(
      config => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );
    return axiosInstance.get('/api/v1/get_sender_list');
  },
  makePayment(payload) {
    axiosInstance.interceptors.request.use(
      config => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );
    return axiosInstance.post('/api/v1/request_payment', payload);
  }
};

export default requestService;
