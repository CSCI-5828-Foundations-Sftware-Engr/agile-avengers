import axios from "axios";

import config from "../header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";

const requestService = {
  getUserPermissions() {
    const url = `/api/v1/permission`;
    return axios.get(url, config);
  }
};

export default requestService;
