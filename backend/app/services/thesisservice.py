from peewee import IntegrityError, PeeweeException
from playhouse.shortcuts import model_to_dict

from ..models.data import (Appendix, Figure, Footnote, Reference, TableEntry,
                           Thesis, User)


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
            return thesis
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
            content = thesis_data.get("content")
            status = thesis_data.get("status")
            student_id = thesis_data.get("student_id")

            # Validate required fields
            if not title or not status or not student_id:
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
                content=content,
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
            # Fetch existing data
            thesis = Thesis.get_or_none(
                (Thesis.id == thesis_id) & (Thesis.student_id == user_id)
            )
            if not thesis:
                self.logger.warning(
                    f"Thesis {thesis_id} not found or not owned by user {user_id}."
                )
                return None

            # Check for changes
            existing_data = {
                "title": thesis.title,
                "abstract": thesis.abstract,
                "status": thesis.status,
            }
            if updated_data == existing_data:
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                self.logger.info(f"No changes detected for thesis {thesis_id}.")
                return thesis

            # Perform the update
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

    # --- References ---
    def add_reference(self, thesis_id, reference_data):
        """
        Adds a reference to the specified thesis.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            reference = Reference.create(thesis=thesis, **reference_data)
            self.logger.info(f"Reference added to thesis {thesis_id}: {reference_data}")
            return reference
        except Exception as e:
            self.logger.error(f"Error adding reference to thesis {thesis_id}: {e}")
            raise

    def get_references(self, thesis_id):
        """
        Retrieves all references for the specified thesis.
        """
        try:
            references = Reference.select().where(Reference.thesis_id == thesis_id)
            return [model_to_dict(ref) for ref in references]
        except Exception as e:
            self.logger.error(f"Error fetching references for thesis {thesis_id}: {e}")
            raise

    def update_reference(self, reference_id, updated_data):
        """
        Updates a specific reference.
        """
        try:
            reference = Reference.get_or_none(Reference.id == reference_id)
            if not reference:
                raise ValueError(f"Reference with ID {reference_id} not found.")

            query = Reference.update(**updated_data).where(Reference.id == reference_id)
            query.execute()

            updated_reference = Reference.get(Reference.id == reference_id)
            self.logger.info(f"Reference {reference_id} updated successfully.")
            return updated_reference
        except Exception as e:
            self.logger.error(f"Error updating reference {reference_id}: {e}")
            raise

    def delete_reference(self, reference_id):
        """
        Deletes a specific reference.
        """
        try:
            reference = Reference.get_or_none(Reference.id == reference_id)
            if not reference:
                raise ValueError(f"Reference with ID {reference_id} not found.")

            reference.delete_instance()
            self.logger.info(f"Reference {reference_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting reference {reference_id}: {e}")
            raise

    # --- Footnotes ---
    def add_footnote(self, thesis_id, footnote_data):
        """
        Adds a footnote to the specified thesis.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            footnote = Footnote.create(thesis=thesis, **footnote_data)
            self.logger.info(f"Footnote added to thesis {thesis_id}: {footnote_data}")
            return footnote
        except Exception as e:
            self.logger.error(f"Error adding footnote to thesis {thesis_id}: {e}")
            raise

    def get_footnotes(self, thesis_id):
        """
        Retrieves all footnotes for the specified thesis.
        """
        try:
            footnotes = Footnote.select().where(Footnote.thesis_id == thesis_id)
            return [model_to_dict(fn) for fn in footnotes]
        except Exception as e:
            self.logger.error(f"Error fetching footnotes for thesis {thesis_id}: {e}")
            raise

    def update_footnote(self, footnote_id, updated_data):
        """
        Updates a specific footnote.
        """
        try:
            footnote = Footnote.get_or_none(Footnote.id == footnote_id)
            if not footnote:
                raise ValueError(f"Footnote with ID {footnote_id} not found.")

            query = Footnote.update(**updated_data).where(Footnote.id == footnote_id)
            query.execute()

            updated_footnote = Footnote.get(Footnote.id == footnote_id)
            self.logger.info(f"Footnote {footnote_id} updated successfully.")
            return updated_footnote
        except Exception as e:
            self.logger.error(f"Error updating footnote {footnote_id}: {e}")
            raise

    def delete_footnote(self, footnote_id):
        """
        Deletes a specific footnote.
        """
        try:
            footnote = Footnote.get_or_none(Footnote.id == footnote_id)
            if not footnote:
                raise ValueError(f"Footnote with ID {footnote_id} not found.")

            footnote.delete_instance()
            self.logger.info(f"Footnote {footnote_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting footnote {footnote_id}: {e}")
            raise

    # --- Tables ---
    def add_table(self, thesis_id, table_data):
        """
        Adds a table to the specified thesis.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            table = TableEntry.create(thesis=thesis, **table_data)
            self.logger.info(f"Table added to thesis {thesis_id}: {table_data}")
            return table
        except Exception as e:
            self.logger.error(f"Error adding table to thesis {thesis_id}: {e}")
            raise

    def get_tables(self, thesis_id):
        """
        Retrieves all tables for the specified thesis.
        """
        try:
            tables = TableEntry.select().where(TableEntry.thesis_id == thesis_id)
            return [model_to_dict(tbl) for tbl in tables]
        except Exception as e:
            self.logger.error(f"Error fetching tables for thesis {thesis_id}: {e}")
            raise

    def update_table(self, table_id, updated_data):
        """
        Updates a specific table.
        """
        try:
            table = TableEntry.get_or_none(TableEntry.id == table_id)
            if not table:
                raise ValueError(f"Table with ID {table_id} not found.")

            query = TableEntry.update(**updated_data).where(TableEntry.id == table_id)
            query.execute()

            updated_table = TableEntry.get(TableEntry.id == table_id)
            self.logger.info(f"Table {table_id} updated successfully.")
            return updated_table
        except Exception as e:
            self.logger.error(f"Error updating table {table_id}: {e}")
            raise

    def delete_table(self, table_id):
        """
        Deletes a specific table.
        """
        try:
            table = TableEntry.get_or_none(TableEntry.id == table_id)
            if not table:
                raise ValueError(f"Table with ID {table_id} not found.")

            table.delete_instance()
            self.logger.info(f"Table {table_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting table {table_id}: {e}")
            raise

    # --- Figures ---
    def add_figure(self, thesis_id, figure_data):
        """
        Adds a figure to the specified thesis.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            figure = Figure.create(thesis=thesis, **figure_data)
            self.logger.info(f"Figure added to thesis {thesis_id}: {figure_data}")
            return figure
        except Exception as e:
            self.logger.error(f"Error adding figure to thesis {thesis_id}: {e}")
            raise

    def get_figures(self, thesis_id):
        """
        Retrieves all figures for the specified thesis.
        """
        try:
            figures = Figure.select().where(Figure.thesis_id == thesis_id)
            return [model_to_dict(fig) for fig in figures]
        except Exception as e:
            self.logger.error(f"Error fetching figures for thesis {thesis_id}: {e}")
            raise

    def update_figure(self, figure_id, updated_data):
        """
        Updates a specific figure.
        """
        try:
            figure = Figure.get_or_none(Figure.id == figure_id)
            if not figure:
                raise ValueError(f"Figure with ID {figure_id} not found.")

            query = Figure.update(**updated_data).where(Figure.id == figure_id)
            query.execute()

            updated_figure = Figure.get(Figure.id == figure_id)
            self.logger.info(f"Figure {figure_id} updated successfully.")
            return updated_figure
        except Exception as e:
            self.logger.error(f"Error updating figure {figure_id}: {e}")
            raise

    def delete_figure(self, figure_id):
        """
        Deletes a specific figure.
        """
        try:
            figure = Figure.get_or_none(Figure.id == figure_id)
            if not figure:
                raise ValueError(f"Figure with ID {figure_id} not found.")

            figure.delete_instance()
            self.logger.info(f"Figure {figure_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting figure {figure_id}: {e}")
            raise

    # --- Appendices ---
    def add_appendix(self, thesis_id, appendix_data):
        """
        Adds an appendix to the specified thesis.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            appendix = Appendix.create(thesis=thesis, **appendix_data)
            self.logger.info(f"Appendix added to thesis {thesis_id}: {appendix_data}")
            return appendix
        except Exception as e:
            self.logger.error(f"Error adding appendix to thesis {thesis_id}: {e}")
            raise

    def get_appendices(self, thesis_id):
        """
        Retrieves all appendices for the specified thesis.
        """
        try:
            appendices = Appendix.select().where(Appendix.thesis_id == thesis_id)
            return [model_to_dict(app) for app in appendices]
        except Exception as e:
            self.logger.error(f"Error fetching appendices for thesis {thesis_id}: {e}")
            raise

    def update_appendix(self, appendix_id, updated_data):
        """
        Updates a specific appendix.
        """
        try:
            appendix = Appendix.get_or_none(Appendix.id == appendix_id)
            if not appendix:
                raise ValueError(f"Appendix with ID {appendix_id} not found.")

            query = Appendix.update(**updated_data).where(Appendix.id == appendix_id)
            query.execute()

            updated_appendix = Appendix.get(Appendix.id == appendix_id)
            self.logger.info(f"Appendix {appendix_id} updated successfully.")
            return updated_appendix
        except Exception as e:
            self.logger.error(f"Error updating appendix {appendix_id}: {e}")
            raise

    def delete_appendix(self, appendix_id):
        """
        Deletes a specific appendix.
        """
        try:
            appendix = Appendix.get_or_none(Appendix.id == appendix_id)
            if not appendix:
                raise ValueError(f"Appendix with ID {appendix_id} not found.")

            appendix.delete_instance()
            self.logger.info(f"Appendix {appendix_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting appendix {appendix_id}: {e}")
            raise
