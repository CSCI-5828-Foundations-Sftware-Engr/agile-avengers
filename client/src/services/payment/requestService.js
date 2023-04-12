import axios from "axios";

import config from "../header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";

const requestService = {
  getUserPermissions() {
    const url = `/api/v1/permission`;
    return axios.get(url, config);
  },
  getSenderList() {
    const url = `${instanceUrl}/api/v1/get_sender_list`;
    return axios.get(url, config);
  },
  makePayment(payload) {
    const url = `${instanceUrl}/api/v1/request_payment`;
    return axios.post(url, payload, config);
  }
};

export default requestService;
