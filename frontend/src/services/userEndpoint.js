import { request } from "./apiClient";

const userAPI = {
  getUserProfile: () => request("get", "/user/profile"),
  updateUserProfile: (profileData) =>
    request("put", "/user/profile", profileData),
  uploadProfilePicture: (formData) =>
    request("post", "/user/profile-picture", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  activateUser: (userId) => request("put", `/user/activate/${userId}`),
  deactivateUser: () => request("put", "/user/deactivate"),
  deleteUser: (userId) => request("delete", `/user/${userId}`),
};

export default userAPI;
