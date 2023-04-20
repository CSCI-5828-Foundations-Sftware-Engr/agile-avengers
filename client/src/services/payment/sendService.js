import axios from "axios";
import { BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

const sendService = {
  getAllPaymentMethods() {
    const url = `${BACKEND_API_URL}/payment/get_all_payment_methods/${localStorage.getItem('user_id')}`;
    return axios.get(url, config);
  },
  getPayeeList() {
    const url = `${BACKEND_API_URL}/payment/get_payee_list/${localStorage.getItem('user_id')}`;
    return axios.get(url, config);
  },
  makePayment(payload) {
    const url = `${BACKEND_API_URL}/payment/send`;
    return axios.post(url, payload, config);
  },
  makeTransactionPayment(payload,transactionId) {
    const url = `${BACKEND_API_URL}/payment/send/${transactionId}`;
    return axios.post(url, payload, config);
  }
};

export default sendService;
