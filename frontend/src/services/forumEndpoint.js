import { request } from "./apiClient";

const forumAPI = {
  getPosts: () => request("get", "/forum/posts"),
  getPostById: (postId) => request("get", `/forum/posts/${postId}`),
  createPost: (postData) => request("post", "/forum/posts/new", postData),
  updatePost: (postId, postData) =>
    request("put", `/forum/posts/${postId}`, postData),
  deletePost: (postId) => request("delete", `/forum/posts/${postId}`),

  addComment: (postId, commentData) =>
    request("post", `/forum/posts/${postId}/comments`, commentData),
  deleteComment: (postId, commentId) =>
    request("delete", `/forum/posts/${postId}/comments/${commentId}`),
  deleteAllComments: (postId) =>
    request("delete", `/forum/posts/${postId}/comments`),
  getComment: (postId, commentId) =>
    request("get", `/forum/posts/${postId}/comments/${commentId}`),
  updateComment: (postId, commentId, commentData) =>
    request("put", `/forum/posts/${postId}/comments/${commentId}`, commentData),
};

export default forumAPI;
