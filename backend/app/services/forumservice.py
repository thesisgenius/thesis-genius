from backend import Post, PostComment
from datetime import datetime, timezone

class ForumService:
    def get_all_posts(self):
        """
        Fetch all forum posts.
        """
        posts = Post.select()
        return [
            {
                "id": post.id,
                "user_id": post.user.id,
                "user_name": post.user.name,
                "title": post.title,
                "description": post.description,
                "content": post.content,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
            for post in posts
        ]

    def get_post_by_id(self, post_id):
        """
        Fetch a single post by ID.
        """
        post = Post.get_or_none(Post.id == post_id)
        if not post:
            return None
        return {
            "id": post.id,
            "user_id": post.user.id,
            "user_name": post.user.name,
            "title": post.title,
            "description": post.description,
            "content": post.content,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }

    def create_post(self, user_id, post_data):
        """
        Create a new forum post.
        """
        post = Post.create(
            user=user_id,
            title=post_data["title"],
            description=post_data.get("description"),
            content=post_data["content"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
        }

    def add_comment_to_post(self, user_id, post_id, comment_data):
        """
        Add a comment to a forum post.
        """
        comment = PostComment.create(
            user=user_id,
            post=post_id,
            content=comment_data["content"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return {
            "id": comment.id,
            "post_id": comment.post.id,
            "user_id": comment.user.id,
            "content": comment.content,
        }

    def delete_post(self, post_id, user_id):
        """
        Delete a forum post for the authenticated user.
        """
        post = Post.get_or_none(Post.id == post_id, Post.user == user_id)
        if not post:
            return False
        return Post.delete().where(Post.id == post_id, Post.user == user_id).execute() > 0

    def get_post_comments(self, post_id):
        """
        Fetch all comments for a specific post.
        """
        comments = PostComment.select().where(PostComment.post == post_id)
        return [
            {
                "id": comment.id,
                "user_id": comment.user.id,
                "user_name": comment.user.name,
                "content": comment.content,
                "created_at": comment.created_at,
            }
            for comment in comments
        ]
