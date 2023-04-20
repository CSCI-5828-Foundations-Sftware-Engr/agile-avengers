import axios from "axios";
import { BACKEND_API_URL } from "../../constants/backend";

import config from "../header/headerConfig";

const pendingRequestsService = {
  pendingRequests() {
    const url = `${BACKEND_API_URL}/payment/pending_requests/${localStorage.getItem('user_id')}`;
    return axios.get(url, config);
  },
  cancelPendingRequest(transaction_id) {
    const url = `${BACKEND_API_URL}/payment/cancel_pending_request?transaction_id=${transaction_id}`;
    return axios.post(url, config);
  }
};

export default pendingRequestsService;
