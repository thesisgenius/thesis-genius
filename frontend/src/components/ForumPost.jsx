import React, { useState, useEffect } from "react";
import forumAPI from "../services/forumEndpoint.js"; // Import the forum API
import { useNavigate, useParams } from "react-router-dom";

// Initial state for new post creation
const initialNewPostState = { title: "", content: "" };

const ForumPost = () => {
    const [newPost, setNewPost] = useState(initialNewPostState);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const { postId } = useParams(); // Used to check if we are editing an existing post
    const navigate = useNavigate();

    // Fetch details of post to edit
    const fetchPostDetails = async () => {
        if (!postId) return; // No need to fetch if creating a new post
        setLoading(true);

        try {
            // Use forumAPI to get post details
            const post = await forumAPI.getPostById(postId);
            setNewPost({
                title: post.title,
                content: post.content,
            });
        } catch (error) {
            setErrorMessage("Failed to load post details. Please try again.");
            console.error("Fetch post details error:", error);
        } finally {
            setLoading(false);
        }
    };

    // Handle input change for form fields
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewPost((prevNewPost) => ({
            ...prevNewPost,
            [name]: value,
        }));
    };

    // Handle form submission for creating or updating a post
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            if (postId) {
                // Update existing post using forumAPI
                await forumAPI.updatePost(postId, newPost);
            } else {
                // Create new post using forumAPI
                await forumAPI.createPost(newPost);
            }

            // Redirect to Forum page after success
            navigate("/forum");
        } catch (error) {
            setErrorMessage(
                postId
                    ? "Failed to update the post. Please try again."
                    : "Failed to create a new post. Please try again."
            );
            console.error("Submit post error:", error);
        } finally {
            setLoading(false);
        }
    };

    // Fetch post details for editing on mount
    useEffect(() => {
        fetchPostDetails();
    }, [postId]);

    return (
        <div className="forum-container">
            <div className="create-post">
                <h2>{postId ? "Edit Post" : "New Post"}</h2>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <form onSubmit={handleSubmit}>
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
                        <div>
                            <button style={styles.button} type="submit" disabled={loading}>
                                {postId ? "Update Post" : "Create Post"}
                            </button>
                            {/* Return to ForumDashboard Button */}
                            <button
                                style={styles.button}
                                type="button" // Prevent accidental form submission
                                onClick={() => navigate("/forum")}
                            >
                                Return to Forum Dashboard
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default ForumPost;

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