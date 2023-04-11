import axios from "axios";

import config from "../header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";

const sendService = {
  getAllPaymentMethods() {
    const url = `${instanceUrl}/api/v1/get_all_payment_methods`;
    return axios.get(url, config);
  },
  getPayeeList() {
    const url = `${instanceUrl}/api/v1/get_payee_list`;
    return axios.get(url, config);
  },
  makePayment(payload) {
    const url = `${instanceUrl}/api/v1/make_payment`;
    return axios.post(url, payload, config);
  }
};

export default sendService;
