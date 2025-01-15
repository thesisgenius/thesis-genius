from peewee import IntegrityError, PeeweeException
from playhouse.shortcuts import model_to_dict

from ..models.data import Thesis, User


class ThesisService:
    def __init__(self, logger):
        """
        Initialize the ThesisService with a logger instance.
        """
        self.logger = logger

    def get_user_theses(self, user_id, status=None, order_by=None):
        """
        Fetch all theses created by the specified user with optional filters and sorting.
        """
        try:
            query = Thesis.select().where(Thesis.student_id == user_id)
            if status:
                query = query.where(Thesis.status == status)
            if order_by:
                query = query.order_by(order_by)
            theses = list(query.dicts())
            return theses
        except PeeweeException as db_error:
            self.logger.error(
                f"Database error fetching theses for user {user_id}: {db_error}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching theses for user {user_id}: {e}"
            )
            raise

    def get_user_theses_paginated(self, user_id, page=1, per_page=10):
        """
        Fetch theses created by the specified user with pagination.
        """
        try:
            query = Thesis.select().where(Thesis.student_id == user_id)
            total = query.count()  # Total number of records
            theses = query.paginate(page, per_page)
            return [model_to_dict(thesis) for thesis in theses], total
        except PeeweeException as db_error:
            self.logger.error(
                f"Database error fetching theses for user {user_id}: {db_error}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching theses for user {user_id}: {e}"
            )
            raise

    def get_thesis_by_id(self, thesis_id, user_id=None):
        """
        Fetch a single thesis by ID, optionally restricting to a specific user.
        """
        try:
            query = Thesis.select().where(Thesis.id == thesis_id)
            if user_id:
                query = query.where(Thesis.student_id == user_id)
            thesis = query.get_or_none()
            return model_to_dict(thesis) if thesis else None
        except Exception as e:
            self.logger.error(f"Failed to fetch thesis {thesis_id}: {e}")
            return None

    def create_thesis(self, thesis_data):
        """
        Create a new thesis for the specified student.
        """
        try:
            title = thesis_data.get("title")
            abstract = thesis_data.get("abstract")
            status = thesis_data.get("status")
            student_id = thesis_data.get("student_id")

            # Validate required fields
            if not title or not abstract or not status or not student_id:
                raise ValueError(
                    "Title, abstract, status, and student ID are required."
                )

            # Ensure the student exists
            student = User.get_or_none(User.id == student_id)
            if not student:
                raise ValueError(f"User with ID {student_id} does not exist.")

            # Create the thesis
            thesis = Thesis.create(
                title=title,
                abstract=abstract,
                status=status,
                student_id=student_id,  # Use student_id directly
            )
            self.logger.info(f"Thesis created successfully: {thesis.id}")
            return thesis
        except IntegrityError as e:
            self.logger.error(f"IntegrityError creating thesis: {e}")
            raise
        except ValueError as e:
            self.logger.warning(f"Validation error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error creating thesis: {e}")
            raise

    def update_thesis(self, thesis_id, user_id, updated_data):
        """
        Update an existing thesis for the specified user.
        """
        try:
            query = Thesis.update(**updated_data).where(
                (Thesis.id == thesis_id) & (Thesis.student_id == user_id)
            )
            updated_rows = query.execute()
            if updated_rows > 0:
                self.logger.info(f"Thesis {thesis_id} updated successfully.")
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                return thesis
            else:
                self.logger.warning(f"No rows updated for thesis {thesis_id}.")
                return None
        except IntegrityError as e:
            self.logger.error(f"IntegrityError updating thesis {thesis_id}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to update thesis {thesis_id}: {e}")
            return None

    def delete_thesis(self, thesis_id, user_id):
        """
        Delete a thesis for the specified user.
        """
        try:
            thesis = Thesis.get_or_none(
                (Thesis.id == thesis_id) & (Thesis.student_id == user_id)
            )
            if not thesis:
                self.logger.warning(
                    f"Thesis {thesis_id} not found or not owned by user {user_id}."
                )
                return False

            thesis.delete_instance()
            self.logger.info(f"Thesis {thesis_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete thesis {thesis_id}: {e}")
            return False
