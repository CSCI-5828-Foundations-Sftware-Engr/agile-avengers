import axios from "axios";
import { BACKEND_BASE_URL,BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

const axiosInstance = axios.create({
  baseURL: BACKEND_BASE_URL,
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
    return axiosInstance.get(`${BACKEND_API_URL}/payment/get_sender_list`);
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
    return axiosInstance.post(`${BACKEND_API_URL}/request_payment', payload`);
  }
};

export default requestService;
