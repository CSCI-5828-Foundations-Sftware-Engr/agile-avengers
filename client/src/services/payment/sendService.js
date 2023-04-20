import axios from "axios";
import { BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

<<<<<<< Updated upstream
=======
const instanceUrl = "http://127.0.0.1/api";

>>>>>>> Stashed changes
const sendService = {
  getAllPaymentMethods() {
    const url = `${BACKEND_API_URL}/payment/get_all_payment_methods`;
    return axios.get(url, config);
  },
  getPayeeList() {
    const url = `${BACKEND_API_URL}/payment/get_payee_list`;
    return axios.get(url, config);
  },
  makePayment(payload) {
    const url = `${BACKEND_API_URL}/payment/send`;
    return axios.post(url, payload, config);
  }
};

export default sendService;
