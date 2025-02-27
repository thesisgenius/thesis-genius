import React, { useEffect, useState } from "react";
import apiClient from "../services/apiClient";
import "../styles/Forum.css";

const Forum = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: "", content: "" });
  const [loading, setLoading] = useState(true);

  // Fetch all forum posts on component load
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await apiClient.get("/forum/posts");
        setPosts(response.data.posts);
      } catch (error) {
        console.error("Failed to fetch posts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  // Handle input changes for creating a new post
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewPost({ ...newPost, [name]: value });
  };

  // Handle submission of a new post
  const handleCreatePost = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post("/forum/posts", newPost);
      setPosts((prevPosts) => [response.data.post, ...prevPosts]); // Add the new post to the list
      setNewPost({ title: "", content: "" }); // Reset the form
    } catch (error) {
      console.error("Failed to create post:", error);
    }
  };

  if (loading) {
    return <p>Loading posts...</p>;
  }

  return (
    <div className="forum-container">
      <h1>Forum</h1>

      {/* New Post Form */}
      <div className="create-post">
        <h2>Create a New Post</h2>
        <form onSubmit={handleCreatePost}>
          <label>Title</label>
          <input
            type="text"
            name="title"
            value={newPost.title}
            onChange={handleInputChange}
            placeholder="Enter post title"
            required
          />
          <label>Content</label>
          <textarea
            name="content"
            value={newPost.content}
            onChange={handleInputChange}
            placeholder="Enter post content"
            required
          ></textarea>
          <button type="submit">Submit</button>
        </form>
      </div>

      {/* Forum Posts */}
      <div className="posts">
        <h2>All Posts</h2>
        {posts.length === 0 ? (
          <p>No posts available.</p>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="post">
              <h3>{post.title}</h3>
              <p>{post.content}</p>
              <small>
                Posted on: {new Date(post.created_at).toLocaleString()}
              </small>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Forum;
