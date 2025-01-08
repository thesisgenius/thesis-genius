from peewee import IntegrityError

from ..models.data import Post, PostComment
from ..utils.db import model_to_dict


class ForumService:
    def __init__(self, logger):
        """
        Initialize the ForumService with a logger instance.
        """
        self.logger = logger

    def get_all_posts(self):
        """
        Fetch all forum posts.
        """
        try:
            posts = Post.select().dicts()
            return list(posts)  # Convert QuerySet to a list of dictionaries
        except Exception as e:
            self.logger.error(f"Failed to fetch posts: {e}")
            return []

    def get_post_by_id(self, post_id):
        """
        Fetch a single post by ID.
        """
        try:
            post = Post.get_or_none(Post.id == post_id)
            return (
                model_to_dict(post) if post else None
            )  # Return the post as a dictionary
        except Exception as e:
            self.logger.error(f"Failed to fetch post {post_id}: {e}")
            return None

    def get_post_comments(self, post_id):
        """
        Fetch all comments for a specific post.
        """
        try:
            comments = (
                PostComment.select(PostComment, Post)
                .where(PostComment.post == post_id)
                .dicts()
            )
            return list(comments)
        except Exception as e:
            self.logger.error(f"Failed to fetch comments for post {post_id}: {e}")
            return []

    def create_post(self, user_id, post_data):
        """
        Create a new forum post.
        """
        try:
            post = Post.create(user=user_id, **post_data)
            self.logger.info(f"Post created successfully: {post.id}")
            return model_to_dict(post)  # Return the post as a dictionary
        except IntegrityError as e:
            self.logger.error(f"IntegrityError creating post: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to create post: {e}")
            return None

    def add_comment_to_post(self, user_id, post_id, comment_data):
        """
        Add a comment to a forum post.
        """
        try:
            comment = PostComment.create(
                user=user_id, post=post_id, content=comment_data["content"]
            )
            self.logger.info(f"Comment added successfully: {comment.id}")
            return model_to_dict(comment)  # Return the comment as a dictionary
        except IntegrityError as e:
            self.logger.error(f"IntegrityError adding comment: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to add comment to post {post_id}: {e}")
            return None

    def delete_post(self, post_id, user_id):
        """
        Delete a forum post.
        """
        try:
            post = Post.get_or_none(Post.id == post_id, Post.user == user_id)
            if not post:
                self.logger.warning(f"Post not found or not owned by user {user_id}")
                return False

            post.delete_instance()
            self.logger.info(f"Post deleted successfully: {post_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete post {post_id}: {e}")
            return False
