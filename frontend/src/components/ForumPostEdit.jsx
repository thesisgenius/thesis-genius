import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import forumAPI from "../services/forumEndpoint.js"; // Import the forum API

const ForumPostEdit = () => {
  const { postId } = useParams(); // Get the post id from the URL
  const [postData, setPostData] = useState({ title: "", content: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  // Fetch the selected post details using forumAPI
  const fetchPostDetails = async () => {
    try {
      const post = await forumAPI.getPostById(postId); // Get post details
      setPostData({
        title: post.post.title,
        content: post.post.content,
        id: post.post.id,
      });
    } catch (err) {
      console.error("Failed to fetch post details:", err);
      setError("Failed to load post details.");
    } finally {
      setLoading(false);
    }
  };

  // Handle field input
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPostData((prev) => ({ ...prev, [name]: value })); // Dynamically update post title or content
  };

  // Submit the updated post data using forumAPI
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      await forumAPI.updatePost(postData.id, postData); // Update the post
      navigate(`/forum/posts/${postData.id}`); // Redirect to the updated post's page
    } catch (err) {
      console.error("Failed to update post:", err);
      setError("Failed to update the post. Please try again.");
    }
  };

  // Delete post using forumAPI
  const deletePost = async () => {
    try {
      await forumAPI.deletePost(postId); // Delete the post
      navigate("/forum"); // Navigate back to the forum dashboard
    } catch (error) {
      console.error("Failed to delete post:", error);
    }
  };

  useEffect(() => {
    fetchPostDetails();
  }, [postId]);

  if (loading) return <p>Loading post details...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="forum-container">
      <h1>Forum</h1>
      {error && <p className="error-message">{error}</p>}
      <div className="create-post">
        <h2>Edit Post</h2>
        <form onSubmit={handleFormSubmit}>
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={postData.title}
            onChange={handleInputChange}
            required
          />
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            name="content"
            rows="10"
            value={postData.content}
            onChange={handleInputChange}
            required
          ></textarea>
          <div style={{ marginTop: "20px" }}>
            <button type="submit" style={styles.button}>
              Save Changes
            </button>
            <button
              type="button"
              style={{
                ...styles.button,
                backgroundColor: "#ff0000",
                marginLeft: "10px",
              }}
              onClick={() => navigate(`/forum/posts/${postId}`)}
            >
              Cancel
            </button>
            <button
              type="button"
              style={{
                ...styles.button,
                backgroundColor: "#ff0000",
                marginLeft: "10px",
              }}
              onClick={deletePost}
            >
              Delete Post
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForumPostEdit;

// Inline styles for simplicity
const styles = {
  button: {
    marginLeft: "10px",
    padding: "5px 10px",
    backgroundColor: "#007acc",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
};
