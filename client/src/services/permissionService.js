import axios from "axios";

import config from "./header/headerConfig";

const instanceUrl = "http://127.0.0.1:5000";

const PermissionService = {
  getUserPermissions() {
    const url = `/api/v1/permission`;
    return axios.get(url, config);
  }
};

export default PermissionService;
