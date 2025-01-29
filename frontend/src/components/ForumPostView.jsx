import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { useParams, useNavigate } from "react-router-dom";
import forumAPI from "../services/forumEndpoint.js"; // Import the forum API

const ForumPostView = () => {
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [commentContent, setCommentContent] = useState("");
    const { postId } = useParams();
    const { user } = useAuth();
    const navigate = useNavigate();

    // Fetch a single post's details using forumAPI
    const fetchPostDetails = async () => {
        try {
            const postDetails = await forumAPI.getPostById(postId);
            setPost({
                post: postDetails.post,
                comments: postDetails.comments,
                user: postDetails.user,
            });
        } catch (error) {
            console.error("Failed to load post details:", error);
        } finally {
            setLoading(false);
        }
    };

    // Add a new comment using forumAPI
    const addComment = async () => {
        try {
            if (!commentContent) return;
            const newComment = await forumAPI.addComment(postId, {
                content: commentContent,
            });
            setPost((prev) => ({
                ...prev,
                comments: {
                    ...prev.comments,
                    results: [
                        ...(prev.comments?.results || []),
                        newComment,
                    ],
                },
            }));
            setCommentContent("");
        } catch (error) {
            console.error("Failed to add comment:", error);
        }
    };

    // Delete a comment by ID using forumAPI
    const deleteComment = async (commentId) => {
        try {
            const isDeleted = await forumAPI.deleteComment(postId, commentId);
            if (isDeleted) {
                setPost((prev) => ({
                    ...prev,
                    comments: {
                        ...prev.comments,
                        results: prev.comments.results.filter(
                            (comment) => comment.id !== commentId
                        ),
                    },
                }));
                console.log("Comment deleted successfully");
            }
        } catch (error) {
            console.error("Failed to delete comment:", error);
        }
    };

    useEffect(() => {
        fetchPostDetails();
    }, [postId]);

    if (loading) return <p>Loading post...</p>;
    if (!post || !post.user) {
        console.warn("Post or post.user is missing, ownership cannot be determined.");
    } // Fallback for invalid post

    const isOwner = user && post.user.id && user.user.id === post.user.id;
    return (
        <div className="post-view">
            <h2>Title: {post.post.title}</h2>
            <section style={{ width: "100%", height: "100px" }}>
                {post.post.content}
                <small>
                    Posted by User {post.user.first_name} {post.user.last_name}  on{" "}
                    {new Date(post.post.created_at).toLocaleString()}
                </small>
            </section>

            {isOwner && (
                <div>
                    <button
                        style={styles.button}
                        onClick={() =>
                            navigate(`/forum/posts/${post.post.id}/edit`)
                        }
                    >
                        Edit Post
                    </button>
                </div>
            )}

            <section className="comments">
                <h3>Comments</h3>
                {post.comments?.results?.length > 0 ? (
                    post.comments.results.map((comment) => (
                        <div
                            key={comment.id || Math.random()}
                            className="comment"
                        >
                            <p>{comment.content}</p>
                            <small>Comment by User {comment.username || 'Unknown User'}</small>
                            {comment.user && user && user.user.id === comment.user && (
                                <button
                                    style={{
                                        ...styles.button,
                                        marginLeft: "10px",
                                        backgroundColor: "#ff0000",
                                    }}
                                    onClick={() => deleteComment(comment.id)}
                                >
                                    Delete Comment
                                </button>
                            )}
                        </div>
                    ))
                ) : (
                    <p>No comments yet.</p>
                )}
                {user && (
                    <div className="add-comment">
                        <textarea
                            placeholder="Add a comment"
                            value={commentContent}
                            onChange={(e) =>
                                setCommentContent(e.target.value)
                            }
                        ></textarea>
                        <div>
                            <button style={styles.button} onClick={addComment}>
                                Submit
                            </button>
                            <button
                                style={{ ...styles.button, marginLeft: "10px" }}
                                onClick={() => navigate("/forum")} // Navigate back to ForumDashboard
                            >
                                Return to Forum Dashboard
                            </button>
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
};

export default ForumPostView;

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