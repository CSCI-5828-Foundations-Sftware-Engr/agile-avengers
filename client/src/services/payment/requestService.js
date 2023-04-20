import axios from "axios";
import { BACKEND_BASE_URL,BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

const axiosInstance = axios.create({
  baseURL: BACKEND_BASE_URL,
});

const requestService = {
  getSenderList() {
    const url = `${BACKEND_API_URL}/payment/get_payee_list/${localStorage.getItem('user_id')}`;
    return axios.get(url, config);
  },
  requestPayment(payload) {
    const url = `${BACKEND_API_URL}/payment/request`;
    return axios.post(url, payload, config);
  }
};

export default requestService;
