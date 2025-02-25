import { request } from "./apiClient";

const statusAPI = {
  aliveCheck: () => request("get", "/status/alive"),
  healthCheck: () => request("get", "/status/health"),
  readinessCheck: () => request("get", "/status/ready"),
};

export default statusAPI;
