import { request } from "./apiClient";

const authAPI = {
  register: (userData) => request("post", "/auth/register", userData),
  signIn: (credentials) => request("post", "/auth/signin", credentials),
  signOut: () => request("post", "/auth/signout"),
};

export default authAPI;
