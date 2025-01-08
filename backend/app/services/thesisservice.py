from peewee import IntegrityError

from ..models.data import Thesis
from ..utils.db import model_to_dict

class ThesisService:
    def __init__(self, logger):
        """
        Initialize the ThesisService with a logger instance.
        """
        self.logger = logger

    def get_user_theses(self, user_id):
        """
        Fetch all theses created by the specified user.
        """
        try:
            theses = Thesis.select().where(Thesis.user == user_id).dicts()
            return list(theses)  # Convert QuerySet to a list of dictionaries
        except Exception as e:
            self.logger.error(f"Failed to fetch theses for user {user_id}: {e}")
            return []

    def get_thesis_by_id(self, thesis_id, user_id=None):
        """
        Fetch a single thesis by ID, optionally restricting to a specific user.
        """
        try:
            query = Thesis.select().where(Thesis.id == thesis_id)
            if user_id:
                query = query.where(Thesis.user == user_id)
            thesis = query.get_or_none()
            return model_to_dict(thesis) if thesis else None
        except Exception as e:
            self.logger.error(f"Failed to fetch thesis {thesis_id}: {e}")
            return None

    def create_thesis(self, user_id, thesis_data):
        """
        Create a new thesis for the specified user.
        """
        try:
            thesis = Thesis.create(user=user_id, **thesis_data)
            self.logger.info(f"Thesis created successfully: {thesis.id}")
            return model_to_dict(thesis)  # Return the thesis as a dictionary
        except IntegrityError as e:
            self.logger.error(f"IntegrityError creating thesis: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to create thesis: {e}")
            return None

    def update_thesis(self, thesis_id, user_id, updated_data):
        """
        Update an existing thesis for the specified user.
        """
        try:
            query = Thesis.update(**updated_data).where(
                (Thesis.id == thesis_id) & (Thesis.user == user_id)
            )
            updated_rows = query.execute()
            if updated_rows > 0:
                self.logger.info(f"Thesis {thesis_id} updated successfully.")
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                return thesis  # Return the updated thesis as a dictionary
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
                (Thesis.id == thesis_id) & (Thesis.user == user_id)
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
