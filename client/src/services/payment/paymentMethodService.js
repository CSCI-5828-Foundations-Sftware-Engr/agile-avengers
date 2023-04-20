import axios from "axios";
import { BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

const paymentMethodService = {
  addNewCreditCard(payload) {
    const url = `${BACKEND_API_URL}/creditcard/add`;
    return axios.post(url, payload, config);
  },
  addNewDebitCard(payload) {
    const url = `${BACKEND_API_URL}/debitcard/add`;
    return axios.post(url, payload, config);
  },
  addNewBankAccount(payload) {
    const url = `${BACKEND_API_URL}/bankaccount/add`;
    return axios.post(url, payload, config);
  }
};

export default paymentMethodService;
