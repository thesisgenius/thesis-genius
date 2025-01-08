from backend import Theses
from datetime import datetime, timezone

class ThesisService:
    def get_user_theses(self, user_id):
        """
        Fetch all theses for a specific user.
        """
        theses = Theses.select().where(Theses.user == user_id)
        return [
            {
                "id": thesis.id,
                "title": thesis.title,
                "abstract": thesis.abstract,
                "status": thesis.status,
                "submission_date": thesis.submission_date,
                "created_at": thesis.created_at,
                "updated_at": thesis.updated_at,
            }
            for thesis in theses
        ]

    def get_thesis_by_id(self, thesis_id, user_id):
        """
        Fetch a single thesis by ID for the authenticated user.
        """
        thesis = Theses.get_or_none(Theses.id == thesis_id, Theses.user == user_id)
        return thesis

    def create_thesis(self, user_id, thesis_data):
        """
        Create a new thesis.
        """
        thesis = Theses.create(
            user=user_id,
            title=thesis_data["title"],
            abstract=thesis_data["abstract"],
            status=thesis_data["status"],
            submission_date=thesis_data.get("submission_date", None),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return {
            "id": thesis.id,
            "title": thesis.title,
            "abstract": thesis.abstract,
            "status": thesis.status,
        }

    def update_thesis(self, thesis_id, user_id, thesis_data):
        """
        Update an existing thesis for the authenticated user.
        """
        thesis = Theses.get_or_none(Theses.id == thesis_id, Theses.user == user_id)
        if not thesis:
            return None
        query = Theses.update(
            **thesis_data, updated_at=datetime.now(timezone.utc)
        ).where(Theses.id == thesis_id, Theses.user == user_id)
        updated_rows = query.execute()
        if updated_rows:
            return self.get_thesis_by_id(thesis_id, user_id)
        return None

    def delete_thesis(self, thesis_id, user_id):
        """
        Delete a thesis for the authenticated user.
        """
        query = Theses.delete().where(Theses.id == thesis_id, Theses.user == user_id)
        return query.execute() > 0  # Returns True if rows were deleted
