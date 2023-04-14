import axios from "axios";

import config from "../header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";

const paymentMethodService = {
  addNewCreditCard(payload) {
    const url = `${instanceUrl}/api/v1/add_new_credit_card`;
    return axios.post(url, payload, config);
  },
  addNewDebitCard(payload) {
    const url = `${instanceUrl}/api/v1/add_new_debit_card`;
    return axios.post(url, payload, config);
  }
};

export default paymentMethodService;
