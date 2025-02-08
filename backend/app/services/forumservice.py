from datetime import datetime, timezone

from peewee import PeeweeException

from ..models.data import PostComment, Posts, User


class ForumService:
    MSG_ERROR_FETCH_POSTS = "Database error fetching posts: {error}"
    MSG_UNEXPECTED_FETCH_POSTS = "Unexpected error fetching posts: {error}"
    MSG_POST_NOT_FOUND = "Post with ID {post_id} not found."
    MSG_COMMENT_NOT_FOUND = "Comment {comment_id} not found for post {post_id}."
    MSG_SUCCESS_UPDATE = "Post {post_id} updated successfully."
    MSG_FAIL_UPDATE = "No rows updated for post {post_id}."
    MSG_DELETE_ERROR = "Error deleting {item} {item_id} for post {post_id}: {error}"

    def __init__(self, logger):
        """
        Initialize the ForumService with a logger instance.
        """
        self.logger = logger

    def _safe_execute(self, query, log_error_msg, on_error=None):
        """
        Try executing a database query and handle errors.
        :param query: Query to execute (function or callable).
        :param log_error_msg: Message to log if an error occurs.
        :param on_error: (Optional) Value to return on errors.
        """
        try:
            return query()
        except PeeweeException as db_error:
            self.logger.error(log_error_msg.format(error=db_error))
            if on_error is not None:
                return on_error
            raise
        except Exception as e:
            self.logger.error(log_error_msg.format(error=e))
            if on_error is not None:
                return on_error
            raise

    @staticmethod
    def _paginate_query(query, page=1, per_page=10):
        """
        Paginate the given Peewee query.
        :param query: Peewee query object to paginate.
        :param page: Page number.
        :param per_page: Items per page.
        :return: Dictionary with paginated results.
        """
        total = query.count()
        results = query.paginate(page, per_page)
        return {
            "results": list(results),
            "total": total,
            "page": page,
            "per_page": per_page,
        }

    def create_post(self, user_id, post_data):
        """
        Create a new forum post.
        :param user_id: ID of the user creating the post.
        :param post_data: Dictionary containing post details (title, content).
        :return: Dictionary with the created post details or None if creation fails.
        """

        def execute_create():
            post = Posts.create(
                user=user_id,
                title=post_data["title"],
                content=post_data["content"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            return post.id  # Return the ID of the newly created post

        post_id = self._safe_execute(
            execute_create,
            log_error_msg=f"Error creating post for user {user_id}: {{error}}",
            on_error=None,
        )

        if post_id:
            self.logger.info(f"Post {post_id} created successfully by user {user_id}.")
            return {"id": post_id, **post_data}

        self.logger.error(
            f"Post creation failed for user {user_id} with data {post_data}."
        )
        return None

    def get_all_posts(self, page=1, per_page=10, order_by=None):
        """
        Fetch all forum posts with pagination and optional sorting.
        """

        def fetch_query():
            query = Posts.select().dicts()
            if order_by:
                query = query.order_by(order_by)
            return self._paginate_query(query, page, per_page)

        return self._safe_execute(
            fetch_query,
            log_error_msg=self.MSG_ERROR_FETCH_POSTS,
            on_error={"results": [], "total": 0, "page": page, "per_page": per_page},
        )

    def get_post_by_id(self, post_id):
        """
        Fetch a single post by ID, including user data.
        """

        def fetch_post():
            try:
                # Fetch the post with joined user data as a dictionary
                post = (
                    Posts.select(
                        Posts.id,
                        Posts.title,
                        Posts.description,
                        Posts.content,
                        Posts.user.alias(
                            "post_user"
                        ),  # Alias to avoid potential conflicts
                        Posts.created_at,
                        Posts.updated_at,
                        User.id.alias("user_id"),  # User fields
                        User.username,
                        User.first_name,
                        User.last_name,
                    )
                    .join(User, on=(Posts.user == User.id))  # Join the User table
                    .where(Posts.id == post_id)
                    .dicts()  # Return results as dictionaries, not model instances
                    .get()  # Get only one result
                )
                # Return the fetched post
                return post

            except Posts.DoesNotExist:
                # Handle the case where the post does not exist
                self.logger.warning(f"Post with ID {post_id} not found in the database")
                return None

        return self._safe_execute(
            fetch_post,
            log_error_msg=f"Database error fetching post {post_id}: {{error}}",
            on_error=None,
        )

    def get_post_comments(self, post_id, page=1, per_page=10, order_by=None):
        """
        Fetch all comments for a specific post with pagination and optional sorting,
        including related user data for each comment.
        """

        def fetch_comments():
            query = (
                PostComment.select(
                    PostComment.id,
                    PostComment.content,
                    PostComment.created_at,
                    PostComment.updated_at,
                    PostComment.user,
                    PostComment.post,
                    User.id.alias("user_id"),  # Include user fields via join
                    User.username,
                    User.first_name,
                    User.last_name,
                )
                .join(
                    User, on=(PostComment.user == User.id)
                )  # Join User table using foreign key
                .where(PostComment.post == post_id)
                .dicts()
            )
            if order_by:
                query = query.order_by(order_by)
            return self._paginate_query(query, page, per_page)

        return self._safe_execute(
            fetch_comments,
            log_error_msg=f"Database error fetching comments for post {post_id}: {{error}}",
            on_error={"results": [], "total": 0, "page": page, "per_page": per_page},
        )

    def update_post(self, post_id, post_data, user_id):
        """
        Update a forum post.
        :param post_id: ID of the post to update.
        :param post_data: Dictionary containing post details to update (e.g., title, content).
        :param user_id: ID of the user updating the post.
        :return: Dictionary with updated post details or None if update fails.
        """

        def execute_update():
            # Update the post and set the updated_at field
            return (
                Posts.update(**post_data, updated_at=datetime.now(timezone.utc))
                .where((Posts.id == post_id) & (Posts.user == user_id))
                .execute()
            )

        updated_rows = self._safe_execute(
            execute_update,
            log_error_msg=f"Error updating post {post_id}: {{error}}",
            on_error=0,
        )

        if updated_rows > 0:
            self.logger.info(f"Post {post_id} updated successfully by user {user_id}.")
            # Combine the updated data along with the post_id to return detailed info
            return {"id": post_id, **post_data}
        elif updated_rows == 0:
            self.logger.warning(
                f"No post was updated. Post {post_id} may not exist or user {user_id} may not have permissions."
            )
            return None
        else:
            # Unexpected case, handled as an error
            self.logger.error(f"Unexpected error during post update for post {post_id}")
            return None

    def add_comment_to_post(self, user_id, post_id, comment_data):
        """
        Add a comment to a specific post.
        :param user_id: ID of the user adding the comment.
        :param post_id: ID of the post to which the comment is being added.
        :param comment_data: Dictionary containing comment details (content).
        :return: Dictionary with the created comment's details or None if creation fails.
        """

        def execute_add_comment():
            comment = PostComment.create(
                user=user_id,
                post=post_id,
                content=comment_data["content"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            return {"id": comment.id, "content": comment.content}

        return self._safe_execute(
            execute_add_comment,
            log_error_msg=f"Error adding comment to post {post_id} by user {user_id}: {{error}}",
            on_error=None,
        )

    def delete_post(self, post_id, user_id):
        """
        Delete a forum post with authorization.
        :param post_id: ID of the post to be deleted.
        :param user_id: ID of the user attempting to delete the post.
        :return: True if the post was deleted successfully, False otherwise.
        """

        def execute_delete():
            post = Posts.get_or_none(Posts.id == post_id)
            if not post:
                self.logger.warning(f"Post {post_id} not found.")
                return False

            # Check if the user is authorized to delete the post
            if post.user_id != user_id:
                self.logger.warning(
                    f"User {user_id} is unauthorized to delete post {post_id}."
                )
                return False

            # Perform the deletion
            self.delete_all_comments(post_id)
            post.delete_instance()
            self.logger.info(f"Post {post_id} deleted successfully by user {user_id}.")
            return True

        return self._safe_execute(
            execute_delete,
            log_error_msg=f"Error deleting post {post_id} by user {user_id}: {{error}}",
            on_error=False,
        )

    def delete_comment(self, post_id, comment_id, user_id):
        """
        Deletes a comment associated with a specific post, given its ID. The function ensures that only
        the authorized user can delete the comment. If the comment is not found or the user lacks
        authorization to delete it, the method logs appropriate warnings and does not perform the
        deletion. The function will handle execution safely and return a boolean indicating the success
        or failure of the operation.

        :param post_id: The unique identifier of the post associated with the comment.
        :param comment_id: The unique identifier of the comment to be deleted.
        :param user_id: The unique identifier of the user attempting to delete the comment.
        :return: A boolean indicating whether the deletion was successfully performed. Returns `True` if
                 the comment was deleted successfully, and `False` otherwise.
        """

        def fetch_and_delete():
            comment = PostComment.get_or_none(
                (PostComment.id == comment_id) & (PostComment.post == post_id)
            )
            # Check if the user is authorized to delete the comment
            if comment.user_id != user_id:
                self.logger.warning(
                    f"User {user_id} is unauthorized to delete comment {comment_id}."
                )
                return False

            if not comment:
                self.logger.warning(
                    self.MSG_COMMENT_NOT_FOUND.format(
                        comment_id=comment_id, post_id=post_id
                    )
                )
                return False
            comment.delete_instance()
            return True

        return self._safe_execute(
            fetch_and_delete,
            log_error_msg=self.MSG_DELETE_ERROR.format(
                item="comment", item_id=comment_id, post_id=post_id, error="{error}"
            ),
            on_error=False,
        )

    def get_comment_by_id(self, post_id, comment_id):
        """
        Fetches a specific comment associated with a given post.

        This method retrieves a specific comment from the database using the post ID and
        comment ID provided. It ensures that the comment with the exact ID matching both
        the post and comment parameters is fetched.

        Any database errors during the fetch operation are logged with a specific error
        message while allowing additional error handling mechanisms.

        :param post_id: The unique identifier of the post to which the comment belongs.
        :type post_id: int
        :param comment_id: The unique identifier of the comment to retrieve.
        :type comment_id: int
        :return: A dictionary containing the comment information, including ID, content,
            creation timestamp, last updated time, user, and associated post, or `None`
            if the operation fails.
        :rtype: dict or None
        """

        def fetch_comment():
            comment = (
                PostComment.select(
                    PostComment.id,
                    PostComment.content,
                    PostComment.created_at,
                    PostComment.updated_at,
                    PostComment.user,
                    PostComment.post,
                )
                .where((PostComment.id == comment_id) & (PostComment.post == post_id))
                .dicts()
                .get()
            )
            return comment

        return self._safe_execute(
            fetch_comment,
            log_error_msg=f"Database error fetching comment {comment_id} for post {post_id}: {{error}}",
            on_error=None,
        )

    def update_comment(self, post_id, comment_id, new_content):
        """
        Updates the content of a specific comment within a specified post. The method ensures
        that the update is safely executed, logs any errors that occur during execution, and
        returns whether the update was successful.

        :param post_id: The ID of the post containing the comment to be updated.
        :type post_id: int
        :param comment_id: The ID of the comment to update within the specified post.
        :type comment_id: int
        :param new_content: The new content to replace the existing comment content.
        :type new_content: str
        :return: A boolean indicating whether the update was successful.
        :rtype: bool
        """

        def execute_update():
            query = PostComment.update(content=new_content).where(
                (PostComment.id == comment_id) & (PostComment.post == post_id)
            )
            return query.execute()

        updated_rows = self._safe_execute(
            execute_update,
            log_error_msg=f"Error updating comment {comment_id} for post {post_id}: {{error}}",
            on_error=0,
        )

        if updated_rows > 0:
            self.logger.info(
                f"Comment {comment_id} for post {post_id} updated successfully."
            )
            return True

        self.logger.warning(
            f"No rows updated for comment {comment_id} on post {post_id}."
        )
        return False

    def delete_all_comments(self, post_id):
        """
        Deletes all comments associated with a specific post.

        This method attempts to delete all comments linked to a given post ID.
        If the deletion is successful, it logs an informational message and returns
        True. If no comments are found to delete, it logs a warning and returns False.

        :param post_id: Unique identifier of the post whose comments need to be deleted.
        :type post_id: int
        :return: True if comments were deleted successfully, False otherwise.
        :rtype: bool
        """

        def execute_deletion():
            query = PostComment.delete().where(PostComment.post == post_id)
            return query.execute()

        deleted_rows = self._safe_execute(
            execute_deletion,
            log_error_msg=f"Error deleting all comments for post {post_id}: {{error}}",
            on_error=0,
        )

        if deleted_rows > 0:
            self.logger.info(f"All comments for post {post_id} deleted successfully.")
            return True

        self.logger.warning(f"No comments found to delete for post {post_id}.")
        return False
