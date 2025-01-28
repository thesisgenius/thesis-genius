import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import forumAPI from "../services/forumEndpoint"; // Use the refactored API service
import "../styles/Forum.css";

const initialNewPostState = { title: "", content: "" };

const ForumDashboard = () => {
    const [posts, setPosts] = useState([]);
    const [newPost, setNewPost] = useState(initialNewPostState);
    const [loading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate(); // Navigation helper

    // Fetch all forum posts
    const fetchPosts = async () => {
        try {
            const postResponse = await forumAPI.getPosts(); // Fetch posts using forumAPI
            const apiPosts = Array.isArray(postResponse.results)
                ? postResponse.results.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                : [];
            setPosts(apiPosts); // Correctly set the state with the posts array
        } catch (error) {
            setPosts([]); // Fallback to an empty array on error
            setErrorMessage("Failed to load posts. Please try again later.");
            console.error("Fetch posts error:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    // Handle input changes for creating a new post
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewPost((prevNewPost) => ({
            ...prevNewPost,
            [name]: value,
        }));
    };

    const refreshPosts = async (newPostData) => {
        try {
            // Fetch the latest posts from the API
            const postResponse = await forumAPI.getPosts();
            const refreshedPosts = Array.isArray(postResponse.results)
                ? postResponse.results.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                : [];

            // Attempt to find the newly created post by matching on its content or title
            if (newPostData && (!newPostData.id || newPostData.id.startsWith("temp"))) {
                const matchingPost = refreshedPosts.find(
                    (post) =>
                        post.title === newPostData.title &&
                        post.content === newPostData.content &&
                        new Date(post.created_at).toISOString() === newPostData.created_at
                );

                if (matchingPost) {
                    console.log("Resolved missing post ID:", matchingPost.id);
                    newPostData.id = matchingPost.id; // Hardset the ID from the refreshed data
                }
            }

            // Update the state with the refreshed posts list
            setPosts(refreshedPosts);
        } catch (error) {
            console.error("Error refreshing posts:", error);
            setErrorMessage("Failed to refresh posts. Please try again later.");
        }
    };

    // Handle form submission to create a new post
    const handleCreatePost = async (event) => {
        event.preventDefault();
        try {
            const postResponse = await forumAPI.createPost(newPost); // API call
            console.log("Post Response:", postResponse); // Debugging the response structure

            let newPostData;

            // Check if the new post response is a string (assume it's an ID fallback)
            if (typeof postResponse.post === "string") {
                newPostData = {
                    id: undefined, // We will resolve this after refreshing
                    title: newPost.title,
                    content: newPost.content,
                    created_at: new Date().toISOString(), // Use current date as a fallback
                };
            } else if (typeof postResponse.post === "object" && postResponse.post !== null) {
                newPostData = postResponse.post; // Properly formatted post from API
            } else {
                throw new TypeError("Invalid response data: postResponse.post is not valid");
            }

            // Add the new post temporarily without an ID if it's undefined
            setPosts((prevPosts) => [newPostData, ...prevPosts]);

            // If the `id` is missing, refresh and fix it
            if (!newPostData.id) {
                console.warn("Post ID is missing, refreshing posts list...");
                await refreshPosts(newPostData); // Pass the new post to resolve its ID
            }

            setNewPost(initialNewPostState); // Reset the form
        } catch (error) {
            setErrorMessage("Failed to create a new post. Please try again.");
            console.error("Create post error:", error);
        }
    };

    // Render posts listing
    const renderPosts = () => {
        if (!Array.isArray(posts) || posts.length === 0) {
            return <p>No posts available.</p>;
        }

        return posts.map((post) => (
            <div
                key={post.id} // Use `id` or fallback to a random unique key
                className="post-summary"
                onClick={() => navigate(`/forum/posts/${post.id}`)}
            >
                <h3>{post.title}</h3>
                <p>{post.content}</p>
                <small>Posted on: {new Date(post.created_at).toLocaleString()}</small>
            </div>
        ));
    };

    if (loading) {
        return <p>Loading posts...</p>;
    }

    return (
        <div className="forum-container">
            <h1>Forum</h1>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <div className="create-post">
                <h2>Create a New Post</h2>
                <form onSubmit={handleCreatePost}>
                    <label htmlFor="title">Title</label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        value={newPost.title}
                        onChange={handleInputChange}
                        placeholder="Enter post title"
                        required
                    />
                    <label htmlFor="content">Content</label>
                    <textarea
                        id="content"
                        name="content"
                        value={newPost.content}
                        onChange={handleInputChange}
                        placeholder="Enter post content"
                        required
                    ></textarea>
                    <button type="submit">Submit</button>
                </form>
            </div>
            <div className="posts">
                <h2>All Posts</h2>
                {renderPosts()}
            </div>
        </div>
    );
};

export default ForumDashboard;