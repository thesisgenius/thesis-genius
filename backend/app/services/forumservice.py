from peewee import IntegrityError, PeeweeException
from ..models.data import Post, PostComment, User
from ..utils.db import model_to_dict


class ForumService:
    def __init__(self, logger):
        """
        Initialize the ForumService with a logger instance.
        """
        self.logger = logger

    def get_all_posts(self, page=1, per_page=10, order_by=None):
        """
        Fetch all forum posts with pagination and optional sorting.
        """
        try:
            query = Post.select().dicts()
            if order_by:
                query = query.order_by(order_by)

            total = query.count()
            posts = query.paginate(page, per_page)
            return {
                "posts": list(posts),
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        except PeeweeException as db_error:
            self.logger.error(f"Database error fetching posts: {db_error}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching posts: {e}")
            raise

    def get_post_by_id(self, post_id):
        """
        Fetch a single post by ID.
        """
        try:
            # Explicitly select fields to avoid aliasing issues
            post = Post.select(
                Post.id,
                Post.title,
                Post.description,
                Post.content,
                Post.user,
                Post.created_at,
                Post.updated_at
            ).where(Post.id == post_id).dicts().get()

            return post
        except Post.DoesNotExist:
            self.logger.warning(f"Post with ID {post_id} not found.")
            return None
        except PeeweeException as db_error:
            self.logger.error(f"Database error fetching post {post_id}: {db_error}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching post {post_id}: {e}")
            raise

    def get_post_comments(self, post_id, page=1, per_page=10, order_by=None):
        """
        Fetch all comments for a specific post with pagination and optional sorting.
        """
        try:
            # Explicitly select fields to avoid aliasing
            # ERROR in forumservice: Database error fetching comments for
            # post 1: (1054, "Unknown column 't2.id' in 'field list'")
            query = PostComment.select(
                PostComment.id,
                PostComment.content,
                PostComment.created_at,
                PostComment.updated_at,
                PostComment.user,
                PostComment.post
            ).where(PostComment.post == post_id).dicts()

            if order_by:
                query = query.order_by(order_by)

            total = query.count()
            comments = query.paginate(page, per_page)
            return {
                "comments": list(comments),
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        except PeeweeException as db_error:
            self.logger.error(
                f"Database error fetching comments for post {post_id}: {db_error}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching comments for post {post_id}: {e}"
            )
            raise

    def create_post(self, user_id, post_data):
        """
        Create a new forum post.
        """
        try:
            post = Post.create(user=user_id, **post_data)
            self.logger.info(f"Post created successfully: {post.id}")
            return model_to_dict(post)
        except IntegrityError as e:
            self.logger.error(f"IntegrityError creating post: {e}")
            return None
        except PeeweeException as db_error:
            self.logger.error(f"Database error creating post: {db_error}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error creating post: {e}")
            raise

    def add_comment_to_post(self, user_id, post_id, comment_data):
        """
        Add a comment to a forum post.
        """
        try:
            comment = PostComment.create(
                user=user_id, post=post_id, content=comment_data["content"]
            )
            self.logger.info(f"Comment added successfully: {comment.id}")
            return model_to_dict(comment)
        except IntegrityError as e:
            self.logger.error(f"IntegrityError adding comment: {e}")
            return None
        except PeeweeException as db_error:
            self.logger.error(
                f"Database error adding comment to post {post_id}: {db_error}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error adding comment to post {post_id}: {e}"
            )
            raise

    def delete_post(self, post_id, user_id):
        """
        Delete a forum post.
        """
        try:
            post = Post.get_or_none((Post.id == post_id) & (Post.user == user_id))
            if not post:
                self.logger.warning(
                    f"Post {post_id} not found or not owned by user {user_id}"
                )
                return False

            post.delete_instance()
            self.logger.info(f"Post deleted successfully: {post_id}")
            return True
        except PeeweeException as db_error:
            self.logger.error(f"Database error deleting post {post_id}: {db_error}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error deleting post {post_id}: {e}")
            raise
