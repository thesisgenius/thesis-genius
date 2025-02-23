from datetime import datetime, timezone

from peewee import IntegrityError, PeeweeException
from playhouse.shortcuts import model_to_dict

from ..models.data import (Abstract, Appendix, BodyPage, Figure, Footnote,
                           Reference, TableEntry, TableOfContents, Thesis,
                           User)


class ThesisService:
    """
    Handles operations related to theses, such as CRUD actions, references, and footnotes. The class is designed to provide
    methods for creating, retrieving, updating, and deleting theses and associated data (references and footnotes). It uses
    a logger to capture errors, warnings, and informational messages during operations. This service also supports pagination
    and detailed filtering for fetching theses.

    :ivar logger: Logger instance for logging various events and errors during operations.
    :type logger: Logger
    """

    def __init__(self, logger):
        """
        Represents a class for handling logging functionality. This class is used
        to manage and set up a logger instance for logging purposes across the
        application.

        Attributes
        ----------
        logger : Logger
            The logger instance provided during initialization to handle logging
            operations.

        :param logger: The logger instance used to configure logging functionality
        :type logger: Logger
        """
        self.logger = logger

    def get_user_theses(self, user_id, status=None, order_by=None):
        """
        Fetches a list of theses for a specific user, with optional status
        filtering and sorting. This function queries the database for theses
        associated with a given user, and applies optional filters and sorting
        parameters. It handles database exceptions and any other unexpected
        errors by logging them and re-raising.

        :param user_id: The unique identifier of the user whose theses are to
            be retrieved.
        :type user_id: int
        :param status: (Optional) The status to filter the theses by.
            Theses will only be retrieved if they match the specified status,
            if provided.
        :type status: str, optional
        :param order_by: (Optional) The field by which the theses should be
            ordered. If provided, the list of theses will be sorted based on
            this field.
        :type order_by: str, optional
        :return: A list of dictionaries, where each dictionary represents a
            thesis belonging to the specified user and matches the applied
            filters, if any.
        :rtype: list[dict]
        :raises PeeweeException: Raised if there is an error in database
            querying, such as connection issues or malformed queries.
        :raises Exception: Raised for any unexpected errors that may occur
            during the execution of the function.
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
        Fetches a paginated list of theses for a specific user based on the user ID. This method uses
        the Peewee ORM to query the database for theses associated with the given user ID and provides
        pagination functionality by limiting the results to the specified page and number of items
        per page. Errors encountered during querying or unexpected issues are logged and raised.

        :param user_id: The ID of the user for whom the theses are being fetched.
        :type user_id: int
        :param page: The page number for paginated results. Defaults to 1.
        :type page: int
        :param per_page: The number of items per page in the paginated results. Defaults to 10.
        :type per_page: int
        :return: A tuple containing a list of serialized theses and the total number of theses found.
        :rtype: tuple[list[dict], int]
        :raises PeeweeException: Raised when a database error occurs.
        :raises Exception: Raised when any unexpected error occurs.
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
        Fetches a thesis record by its unique identifier and optionally filters by
        the user ID linked to the record. This method queries the database to retrieve
        a specific thesis object. In case of any errors during query execution,
        it logs the details and returns None.

        :param thesis_id: Unique identifier for the thesis.
        :type thesis_id: int
        :param user_id: (Optional) The ID of the user associated with the thesis.
        :type user_id: int, optional
        :return: The thesis object if retrieved successfully; otherwise, None.
        :rtype: Thesis or None
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
        except Thesis.DoesNotExist as thesis_not_found:
            self.logger.error(
                f"Thesis with ID {thesis_id} does not exist. {thesis_not_found}"
                f"Thesis with ID {thesis_id} was not found in the database. {thesis_not_found}"
            )
            return None

    def get_cover_page(self, thesis_id, user_id=None):
        """
        Retrieves the cover page details for a given thesis.

        :param thesis_id: The ID of the thesis whose cover page needs to be retrieved.
        :type thesis_id: int
        :param user_id: (Optional) The ID of the user requesting the cover page.
        :type user_id: int
        :return: A dictionary containing the cover page details.
        :rtype: dict
        """
        try:
            query = Thesis.select().where(Thesis.id == thesis_id)
            if user_id:
                query = query.where(Thesis.student_id == user_id)

            thesis = query.get_or_none()
            if not thesis:
                return None

            return {
                "title": thesis.title,
                "author": thesis.author,
                "affiliation": thesis.affiliation,
                "course": thesis.course,
                "instructor": thesis.instructor,
                "due_date": (
                    thesis.due_date.strftime("%Y-%m-%d") if thesis.due_date else None
                ),
            }

        except Exception as e:
            self.logger.error(f"Failed to fetch cover page for thesis {thesis_id}: {e}")
            return None

    def update_cover_page(self, thesis_id, user_id, cover_data):
        """
        Updates the cover page details for a given thesis.

        :param thesis_id: The ID of the thesis whose cover page is being updated.
        :type thesis_id: int
        :param user_id: The ID of the user attempting to update the cover page.
        :type user_id: int
        :param cover_data: A dictionary containing the updated cover page details.
        :type cover_data: dict
        :return: The updated cover page data or None if an error occurs.
        :rtype: dict or None
        """
        try:
            query = Thesis.select().where(
                Thesis.id == thesis_id, Thesis.student_id == user_id
            )
            thesis = query.get_or_none()
            if not thesis:
                return None

            # Update fields only if they are provided in the request
            update_data = {
                key: value for key, value in cover_data.items() if value is not None
            }
            if "due_date" in update_data and update_data["due_date"]:
                update_data["due_date"] = datetime.strptime(
                    update_data["due_date"], "%Y-%m-%d"
                )

            if update_data:
                Thesis.update(**update_data).where(Thesis.id == thesis_id).execute()

            # Return the updated cover page details
            return {
                "title": thesis.title,
                "author": update_data.get("author", thesis.author),
                "affiliation": update_data.get("affiliation", thesis.affiliation),
                "course": update_data.get("course", thesis.course),
                "instructor": update_data.get("instructor", thesis.instructor),
                "due_date": (
                    update_data.get("due_date", thesis.due_date).strftime("%Y-%m-%d")
                    if thesis.due_date
                    else None
                ),
            }

        except Exception as e:
            self.logger.error(
                f"Failed to update cover page for thesis {thesis_id}: {e}"
            )
            return None

    def add_table_of_contents_entry(self, thesis_id, section_title, page_number, order):
        """
        Adds an entry to the table of contents for a thesis.

        :param thesis_id: The ID of the thesis the entry belongs to.
        :type thesis_id: int
        :param section_title: The title of the section in the TOC.
        :type section_title: str
        :param page_number: The page number associated with the section.
        :type page_number: int
        :param order: The order of the section in the TOC.
        :type order: int
        :return: The newly created TOC entry.
        :rtype: TableOfContents
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")
            toc_entry = TableOfContents.create(
                thesis=thesis,
                section_title=section_title,
                page_number=page_number,
                order=order,
            )
            self.logger.info(f"TOC entry added to thesis {thesis_id}.")
            return toc_entry
        except Exception as e:
            self.logger.error(f"Error adding TOC entry to thesis {thesis_id}: {e}")
            raise

    def update_table_of_contents(self, thesis_id, toc_entries):
        """
        Allows users to manually update the TOC.
        """
        try:
            # Clear existing TOC entries
            TableOfContents.delete().where(
                TableOfContents.thesis_id == thesis_id
            ).execute()

            # Insert new TOC entries
            for entry in toc_entries:
                TableOfContents.create(thesis_id=thesis_id, **entry)

            return self.get_table_of_contents(thesis_id)  # Return updated TOC
        except Exception as e:
            self.logger.error(f"Error updating TOC for thesis {thesis_id}: {e}")
            raise

    def get_table_of_contents(self, thesis_id):
        """
        Fetches or generates a table of contents (TOC) for the given thesis. If a pre-existing TOC
        is stored in the database, it retrieves and returns it. Otherwise, the method dynamically
        creates a TOC based on the structure of the thesis document, including body pages and a
        reference section. The dynamically generated TOC is stored in the database for future use.

        :param thesis_id: Identifier of the thesis for which to fetch or generate the table of
            contents.
        :type thesis_id: int
        :return: A list of table of contents entries, with each entry containing information
            about a section such as title, page number, and order.
        :rtype: list[dict]
        :raises Exception: If there is an issue with fetching or generating the table of contents.
        """
        try:
            # Fetch stored TOC entries
            toc_entries = (
                TableOfContents.select()
                .where(TableOfContents.thesis_id == thesis_id)
                .order_by(TableOfContents.order)
            )
            result = [model_to_dict(entry) for entry in toc_entries]

            # If no entries exist, generate TOC dynamically
            if not result:
                self.logger.info(
                    f"No TOC found for thesis {thesis_id}, generating dynamically."
                )

                # Generate TOC based on document structure
                sections = [
                    {"section_title": "Cover Page", "page_number": 1, "order": 1},
                    {"section_title": "Abstract", "page_number": 2, "order": 2},
                ]

                # Fetch body pages and generate section entries
                body_pages = (
                    BodyPage.select()
                    .where(BodyPage.thesis_id == thesis_id)
                    .order_by(BodyPage.page_number)
                )
                for i, page in enumerate(body_pages, start=3):
                    sections.append(
                        {
                            "section_title": f"Page {page.page_number}",
                            "page_number": i,
                            "order": i,
                        }
                    )

                # Add references at the end
                sections.append(
                    {
                        "section_title": "References",
                        "page_number": len(sections) + 1,
                        "order": len(sections) + 1,
                    }
                )

                # Store in database
                for entry in sections:
                    TableOfContents.create(thesis_id=thesis_id, **entry)

                result = sections  # Return generated TOC

            return result
        except Exception as e:
            self.logger.error(f"Error fetching TOC for thesis {thesis_id}: {e}")
            raise

    def delete_table_of_contents_entry(self, entry_id):
        """
        Deletes a specific table of contents entry by its ID.

        :param entry_id: The ID of the TOC entry to delete.
        :type entry_id: int
        :return: True if deletion is successful.
        :rtype: bool
        """
        try:
            entry = TableOfContents.get_or_none(TableOfContents.id == entry_id)
            if not entry:
                self.logger.warning(f"TOC entry {entry_id} not found.")
                return False
            entry.delete_instance()
            self.logger.info(f"TOC entry {entry_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting TOC entry {entry_id}: {e}")
            raise

    def add_abstract(self, thesis_id, abstract_data):
        """
        Adds or updates the abstract for a specified thesis.

        :param thesis_id: The ID of the thesis to which the abstract belongs.
        :type thesis_id: int
        :param abstract_data: The abstract text to be added or updated.
        :type abstract_data: str
        :return: The created or updated Abstract instance.
        :rtype: Abstract
        :raises ValueError: If the specified thesis does not exist.
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            abstract, created = Abstract.get_or_create(thesis=thesis)
            abstract.text = abstract_data
            abstract.save()
            self.logger.info(
                f"Abstract {'created' if created else 'updated'} for thesis {thesis_id}."
            )
            return abstract
        except Exception as e:
            self.logger.error(
                f"Error adding or updating abstract for thesis {thesis_id}: {e}"
            )
            raise

    def get_abstract(self, thesis_id):
        """
        Fetches the abstract for a specified thesis.

        :param thesis_id: The ID of the thesis whose abstract is to be fetched.
        :type thesis_id: int
        :return: The abstract text.
        :rtype: str
        :raises ValueError: If the thesis does not have an abstract.
        """
        try:
            abstract = Abstract.get_or_none(Abstract.thesis_id == thesis_id)
            if not abstract:
                raise ValueError(f"No abstract found for thesis ID {thesis_id}.")
            return abstract.text
        except Exception as e:
            self.logger.error(f"Error fetching abstract for thesis {thesis_id}: {e}")
            raise

    def delete_abstract(self, thesis_id):
        """
        Deletes the abstract for a specified thesis.
        :param thesis_id: The ID of the thesis whose abstract is to be deleted.
        :type thesis_id: int
        :return: True if the deletion is successful.
        :rtype: bool
        """
        try:
            abstract = Abstract.get_or_none(Abstract.thesis_id == thesis_id)
            if not abstract:
                self.logger.warning(f"Abstract for thesis {thesis_id} not found.")
                return False
            abstract.delete_instance()
            self.logger.info(f"Abstract for thesis {thesis_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting abstract for thesis {thesis_id}: {e}")
            raise

    def add_body_page(self, thesis_id, page_number, body_text):
        """
        Adds a body page to the specified thesis.

        :param thesis_id: The ID of the thesis to which the body page belongs.
        :type thesis_id: int
        :param page_number: The page number for the body content.
        :type page_number: int
        :param body_text: The text content for this page.
        :type body_text: str
        :return: The created or updated BodyPage instance.
        :rtype: BodyPage
        """
        try:
            thesis = Thesis.get_or_none(Thesis.id == thesis_id)
            if not thesis:
                raise ValueError(f"Thesis with ID {thesis_id} not found.")

            body_page, created = BodyPage.get_or_create(
                thesis=thesis, page_number=page_number
            )
            body_page.body = body_text
            body_page.save()
            self.logger.info(
                f"Body page {page_number} for thesis {thesis_id} {'created' if created else 'updated'}."
            )
            return body_page
        except Exception as e:
            self.logger.error(
                f"Error adding or updating body page for thesis {thesis_id}: {e}"
            )
            raise

    def get_body_pages(self, thesis_id):
        """
        Fetches all body pages for a specified thesis.

        :param thesis_id: The ID of the thesis whose body pages are to be fetched.
        :type thesis_id: int
        :return: A list of dictionaries with page information.
        :rtype: list[dict]
        """
        try:
            pages = BodyPage.select().where(BodyPage.thesis_id == thesis_id)
            result = [model_to_dict(page) for page in pages]

            if not result:
                self.logger.warning(
                    f"No body pages found for thesis {thesis_id}, returning default blank page."
                )
                return [
                    {
                        "page_number": 1,
                        "body": "(This page is intentionally left blank.)",
                    }
                ]  # Default blank page

            return result
        except Exception as e:
            self.logger.error(f"Error fetching body pages for thesis {thesis_id}: {e}")
            raise

    def delete_body_page(self, thesis_id, page_id):
        """
        Deletes a body page from a thesis, ensuring it belongs to the correct thesis.
        """
        try:
            body_page = BodyPage.get_or_none(
                (BodyPage.id == page_id) & (BodyPage.thesis_id == thesis_id)
            )
            if not body_page:
                self.logger.warning(
                    f"Body page {page_id} not found for thesis {thesis_id}."
                )
                return False

            body_page.delete_instance()
            self.logger.info(
                f"Body page {page_id} deleted successfully from thesis {thesis_id}."
            )
            return True
        except Exception as e:
            self.logger.error(f"Error deleting body page {page_id}: {e}")
            raise

    def create_thesis(self, thesis_data):
        """
        Creates a new thesis entry in the database after performing validation on
        the input data. This function ensures the required fields are provided
        and that the related student exists before creating the thesis.

        :param thesis_data: A dictionary containing data for the thesis. Required
            keys include "title", "status", and "student_id". Optional keys include
            "abstract" and "content".
        :type thesis_data: dict
        :return: The newly created Thesis object.
        :rtype: Thesis
        :raises ValueError: If the required fields are missing or the student does
            not exist.
        :raises IntegrityError: If there is a database integrity issue during
            thesis creation.
        :raises Exception: For any general exceptions that occur while creating the
            thesis.
        """
        try:
            title = thesis_data.get("title")
            course = thesis_data.get("course")
            instructor = thesis_data.get("instructor")
            status = thesis_data.get("status")
            student_id = thesis_data.get("student_id")

            abstract = None
            if "abstract" in thesis_data:
                abstract = thesis_data.get("abstract")

            initial_body_pages = None
            if "body_pages" in thesis_data:
                initial_body_pages = thesis_data.get(
                    "body_pages", []
                )  # List of {'page_number': int, 'body': str}

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
                course=course,
                instructor=instructor,
                status=status,
                student=student_id,
            )

            # Conditionally create abstract
            if abstract:
                self.add_abstract(thesis.id, abstract)

            # Conditionally create body pages
            if initial_body_pages:
                for page in initial_body_pages:
                    self.add_body_page(
                        thesis.id, page.get("page_number"), page.get("body")
                    )
            else:
                # Add a default blank body page
                self.add_body_page(
                    thesis.id, 1, "(This page is intentionally left blank.)"
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
        Updates the thesis associated with a specific user by its ID. This method retrieves
        an existing thesis record, checks for modifications to the data provided, and
        updates the record within the database if changes are detected. In cases where
        no changes are identified or the thesis isn't found, appropriate logging is performed.

        :param thesis_id: The unique identifier of the thesis to be updated.
        :param user_id: The unique identifier of the user owning the thesis.
        :param updated_data: The dictionary containing new data to update the thesis record.
            It is expected to include keys such as 'title', 'abstract', and 'status'.
        :return: Returns the updated thesis record if the update operation is successful,
            or None if no changes are made, the thesis is not found or the user doesn't
            own it, or an error occurs during the operation.
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
            existing_data = model_to_dict(thesis)

            if updated_data == existing_data:
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                self.logger.info(f"No changes detected for thesis {thesis_id}.")
                return thesis

            # Perform the update
            updated_data["updated_at"] = datetime.now(timezone.utc)
            query = Thesis.update(**updated_data).where(
                (Thesis.id == thesis_id) & (Thesis.student_id == user_id)
            )
            updated_rows = query.execute()

            if "abstract" in updated_data:
                self.add_abstract(thesis.id, updated_data.get("abstract"))

            if "body_pages" in updated_data:
                for page in updated_data["body_pages"]:
                    self.add_body_page(
                        thesis.id, page.get("page_number"), page.get("body")
                    )

            if updated_rows > 0:
                self.logger.info(f"Thesis {thesis_id} updated successfully.")
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                return thesis
            else:
                self.logger.warning(f"No rows updated for thesis {thesis_id}.")
                thesis = self.get_thesis_by_id(thesis_id, user_id)
                return thesis
        except IntegrityError as e:
            self.logger.error(f"IntegrityError updating thesis {thesis_id}: {e}")
            return None
        except Exception as e:
            self.logger.error(
                f"Failed to update thesis {thesis_id}: {e}. Thesis: {type(thesis)}"
            )
            return None

    def update_body_page(self, thesis_id, page_id, page_number, body_text):
        """
        Updates a body page's content in an existing thesis.
        """
        try:
            body_page = BodyPage.get_or_none(
                (BodyPage.id == page_id) & (BodyPage.thesis_id == thesis_id)
            )
            if not body_page:
                raise ValueError(
                    f"Body page {page_id} for thesis {thesis_id} not found."
                )

            body_page.page_number = page_number
            body_page.body = body_text
            body_page.save()

            self.logger.info(f"Body page {page_id} updated successfully.")
            return body_page
        except Exception as e:
            self.logger.error(f"Error updating body page {page_id}: {e}")
            raise

    def delete_thesis(self, thesis_id, user_id):
        """
        Deletes a thesis record if it exists and is owned by the specified user. This method
        checks for the combination of thesis ID and user ID to ensure that the action is
        authorized. If the record exists, it is deleted from the database; otherwise, a
        warning is logged.

        :param thesis_id: The unique identifier of the thesis to be deleted.
        :type thesis_id: int
        :param user_id: The unique identifier of the user who owns the thesis.
        :type user_id: int
        :return: True if the thesis was successfully deleted, False otherwise.
        :rtype: bool
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
        Adds a reference to a specified thesis in the database. This method fetches the
        thesis identified by the given `thesis_id` and adds a new reference using the
        `reference_data`. If the thesis is not found or an error occurs during the
        process, appropriate handling is performed.

        :param thesis_id: Unique identifier of the thesis to which the reference will
            be added.
        :type thesis_id: int
        :param reference_data: Data of the reference to be added. Must include valid
            information required for reference creation.
        :type reference_data: dict
        :return: The newly created reference object associated with the specified thesis.
        :rtype: Reference
        :raises ValueError: If the thesis associated with the given `thesis_id` is not
            found.
        :raises Exception: For any other errors encountered during the process.
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
        Fetches references for a given thesis from the database.

        This method retrieves all references associated with the specified thesis ID
        from the database using an ORM query. The references are then converted to a
        dictionary representation for further use or processing. If an error occurs
        during the operation, it is logged, and the exception is re-raised for proper
        handling.

        :param thesis_id: The unique identifier of the thesis for which references
            need to be fetched.
        :type thesis_id: Any compatible type that matches `thesis_id` requirement in the
            database ORM query
        :return: A list of dictionaries, each representing a reference associated
            with the given thesis.
        :rtype: List[Dict[str, Any]]

        :raises Exception: When there is a failure in fetching references
            from the database.
        """
        try:
            references = Reference.select().where(Reference.thesis_id == thesis_id)
            return [model_to_dict(ref) for ref in references]
        except Exception as e:
            self.logger.error(f"Error fetching references for thesis {thesis_id}: {e}")
            raise

    def update_reference(self, reference_id, updated_data):
        """
        Updates an existing reference in the database with the given updated data. The method
        fetches the reference by its unique identifier, applies the provided data updates,
        and saves the changes. If the reference cannot be found, an exception is raised.
        Provides logs about the success or failure of the operation.

        :param reference_id: The unique identifier of the reference to be updated.
        :type reference_id: int
        :param updated_data: A dictionary containing the fields and values to update
            on the reference.
        :type updated_data: dict
        :return: The updated reference object.
        :rtype: Reference
        :raises ValueError: If no reference with the given ID is found.
        :raises Exception: For any other errors encountered during the update process.
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
        Deletes a reference in the database with the given reference ID. If the
        reference ID does not exist, a ValueError is raised. Logs the outcome of
        the deletion process and returns the result. If an error occurs during
        the process, the exception is logged and re-raised.

        :param reference_id: The ID of the reference to delete.
        :type reference_id: int
        :return: True if the deletion is successful.
        :rtype: bool
        :raises ValueError: If the reference ID does not exist.
        :raises Exception: If an error occurs during the deletion process.
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
        Adds a footnote to a specific thesis using the provided thesis ID and footnote data.

        This method attempts to find a thesis with the given ID. If the thesis is found, it creates
        a new footnote associated with the thesis using the provided footnote data. If the thesis
        is not found, an error is logged, and an exception is raised. The method also logs
        successful addition of the footnote.

        :param thesis_id: The ID of the thesis to which the footnote should be added.
        :type thesis_id: int
        :param footnote_data: A dictionary containing data for the footnote to be created. It
            must match the expected structure and fields required for creating a Footnote object.
        :type footnote_data: dict
        :return: The newly created Footnote object.
        :rtype: Footnote
        :raises ValueError: Raised when the thesis with the given ID is not found.
        :raises Exception: Any other exception that occurs during the operations will be
            logged and re-raised for further handling.
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
        Fetches all footnotes associated with a given thesis.

        This method retrieves footnotes from the database corresponding to a specific
        thesis ID. Each footnote record is converted to a dictionary using the
        `model_to_dict` utility before being added to the result list. If an error
        occurs during the retrieval process, an exception is logged, and the same
        exception is raised.

        :param thesis_id: ID of the thesis for which footnotes need to be retrieved.
        :type thesis_id: int
        :return: A list of dictionaries, each representing a footnote record.
        :rtype: list[dict]
        :raises Exception: If there is an error while fetching footnotes from
            the database.
        """
        try:
            footnotes = Footnote.select().where(Footnote.thesis_id == thesis_id)
            return [model_to_dict(fn) for fn in footnotes]
        except Exception as e:
            self.logger.error(f"Error fetching footnotes for thesis {thesis_id}: {e}")
            raise

    def update_footnote(self, footnote_id, updated_data):
        """
        Updates an existing footnote in the database with the provided updated data. If
        the specified footnote does not exist, a ValueError is raised. Logs the process
        and outcome, and reraises any encountered exceptions.

        :param footnote_id: The identifier of the footnote to be updated.
        :type footnote_id: int

        :param updated_data: A dictionary containing key-value pairs of the new data
            to update the footnote with.
        :type updated_data: dict

        :return: The updated footnote instance retrieved after the update.
        :rtype: Footnote
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
        Deletes a footnote by its ID. The method fetches the corresponding footnote
        from the database using the provided ID. If the footnote is found, it is
        deleted, and a success log is recorded. Otherwise, an exception will be
        raised. Logs errors in case of failure during the deletion.

        :param footnote_id: The ID of the footnote to be deleted.
        :type footnote_id: int
        :return: A boolean indicating whether the deletion was successful.
        :rtype: bool
        :raises ValueError: If the footnote with the specified ID is not found.
        :raises Exception: If any other failure occurs during the deletion process.
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
        Adds a new table entry to an existing thesis. The method retrieves the thesis
        object based on the provided `thesis_id`, then creates a new table entry
        associated with that thesis using the provided `table_data`. This operation
        is logged, and any errors encountered during the process are also logged
        before re-raising the exception.

        :param thesis_id: ID of the thesis the table should be added to.
        :type thesis_id: int
        :param table_data: Data of the table to be added, passed as key-value pairs.
        :type table_data: dict
        :return: The created table entry object.
        :rtype: TableEntry
        :raises ValueError: If the thesis with the provided ID cannot be found.
        :raises Exception: For other errors encountered during the operation.
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
        Fetches the tables associated with a given thesis ID from the database and
        returns them in dictionary form. This method queries the `TableEntry` model
        for all entries matching the provided thesis ID. If an error occurs during
        the query, it logs the error and raises the exception.

        :param thesis_id: The unique identifier of the thesis for which tables need
            to be fetched.
        :type thesis_id: int
        :return: A list of dictionaries where each dictionary represents a table
            associated with the given thesis ID.
        :rtype: list[dict]
        :raises Exception: If an error occurs while fetching the tables from the
            database.
        """
        try:
            tables = TableEntry.select().where(TableEntry.thesis_id == thesis_id)
            return [model_to_dict(tbl) for tbl in tables]
        except Exception as e:
            self.logger.error(f"Error fetching tables for thesis {thesis_id}: {e}")
            raise

    def update_table(self, table_id, updated_data):
        """
        Updates a table entry in the database with the provided data. If the table entry
        with the specified ID does not exist, an exception will be raised. The updated
        entry is then retrieved and returned.

        :param table_id: The unique identifier of the table entry to be updated.
        :type table_id: int
        :param updated_data: Dictionary containing the data to update in the table entry.
        :type updated_data: dict
        :return: The updated table entry.
        :rtype: TableEntry
        :raises ValueError: If no table entry is found with the provided ID.
        :raises Exception: If any other error occurs during the update operation.
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
        Deletes a table entry from the database identified by its table ID.

        Attempts to locate and delete a table entry in the database based on the
        provided table ID. If the table is not found, an error is logged and
        raised. If the deletion is successful, an appropriate log message is
        produced. Any unexpected exceptions encountered during this operation
        are logged and re-raised for handling elsewhere.

        :param table_id: Unique identifier of the table to be deleted.
        :type table_id: int
        :return: True if the table is successfully deleted.
        :rtype: bool
        :raises ValueError: If the table with the given table ID is not found.
        :raises Exception: If any other error occurs during the deletion process.
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
        Adds a figure to the specified thesis by its ID. The figure data is provided
        as a dictionary containing necessary details for figure creation. It attempts
        to fetch a Thesis object by ID. If the thesis does not exist, an error is
        raised. A new Figure object is then created and associated with the thesis.
        Logs are written to record successful operations and errors during the process.

        :param thesis_id: The unique identifier of the thesis to which the figure will
                          be added.
        :type thesis_id: int
        :param figure_data: A dictionary containing data required to create a new figure.
        :type figure_data: dict
        :return: A newly created Figure object representing the added figure.
        :rtype: Figure
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
        Fetches all figures associated with a specific thesis.

        This method retrieves all figure records that are associated with
        the given thesis ID from the database. Each figure record is
        converted to a dictionary representation before being returned
        in a list. If any error occurs during this process, it logs
        the error and re-raises the exception.

        :param thesis_id: The unique identifier for the thesis whose figures
                          are to be retrieved. Must match a valid `thesis_id`
                          in the database.
        :type thesis_id: int
        :return: A list of dictionaries where each dictionary represents a
                 figure associated with the given thesis ID.
        :rtype: list[dict]
        :raises Exception: If there is an issue while fetching figures
                           or executing the database query.
        """
        try:
            figures = Figure.select().where(Figure.thesis_id == thesis_id)
            return [model_to_dict(fig) for fig in figures]
        except Exception as e:
            self.logger.error(f"Error fetching figures for thesis {thesis_id}: {e}")
            raise

    def update_figure(self, figure_id, updated_data):
        """
        Updates an existing figure in the database with new data. Retrieves the figure
        by its ID, applies the updates, executes the update query, and fetches the
        updated figure to return. If the figure is not found, raises an error.

        :param figure_id: The unique identifier of the figure to be updated.
        :type figure_id: int
        :param updated_data: A dictionary containing the fields and their new values
            to update the figure with.
        :type updated_data: dict
        :return: The updated figure instance after applying changes.
        :rtype: Figure
        :raises ValueError: If the figure with the given ID is not found.
        :raises Exception: If any error occurs during the update process.
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
        Deletes a figure from the database identified by its unique figure ID.

        This method checks for the existence of a figure with the provided ID
        and removes it if it exists. If no such figure exists, it raises an
        error. The deletion process is logged, including both successful and
        unsuccessful operations. If an unexpected exception is encountered,
        the error is logged, and the exception is propagated.

        :param figure_id: Unique identifier of the figure to be deleted.
        :type figure_id: int
        :return: True if the figure is successfully deleted.
        :rtype: bool
        :raises ValueError: If no figure exists with the specified ID.
        :raises Exception: If an unexpected error occurs during the deletion process.
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
        Adds an appendix to a given thesis by its ID. Ensures that the specified thesis
        exists before attempting to create the appendix. Logs both successful and
        unsuccessful attempts to add the appendix.

        :param thesis_id: The ID of the thesis to which the appendix is to be added.
        :type thesis_id: int
        :param appendix_data: A dictionary containing data for the appendix to be added.
        :type appendix_data: dict
        :return: The created Appendix instance.
        :rtype: Appendix
        :raises ValueError: If the specified thesis is not found.
        :raises Exception: If an error occurs during the process of adding the appendix.
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
        Fetches appendices associated with the provided thesis ID.

        This function retrieves all appendices related to a specific thesis ID from
        the database and returns them as a list of dictionaries. If any error occurs
        during the retrieval process, it will log the error and raise the exception.

        :param thesis_id: ID of the thesis for which appendices are to be fetched.
        :type thesis_id: int
        :return: A list of dictionaries, where each dictionary represents an appendix
            associated with the provided thesis ID.
        :rtype: list[dict]
        :raises Exception: If an error occurs during the database query or
            data processing.
        """
        try:
            appendices = Appendix.select().where(Appendix.thesis_id == thesis_id)
            return [model_to_dict(app) for app in appendices]
        except Exception as e:
            self.logger.error(f"Error fetching appendices for thesis {thesis_id}: {e}")
            raise

    def update_appendix(self, appendix_id, updated_data):
        """
        Updates an existing appendix record in the database using the provided data. If the appendix with
        the specified ID does not exist, an exception is raised. After a successful update, the updated
        appendix record is retrieved and returned.

        :param appendix_id: The unique identifier of the appendix to be updated.
        :type appendix_id: int
        :param updated_data: A dictionary containing the fields to update with their new values.
        :type updated_data: dict
        :return: The updated appendix record.
        :rtype: Appendix
        :raises ValueError: If no appendix with the given ID is found.
        :raises Exception: For other database or unexpected errors.
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
        Deletes an appendix with the given ID. If the appendix with the specified ID
        does not exist in the database, a ValueError is raised. This function logs
        the successful deletion of the appendix or any errors encountered during
        the operation.

        :param appendix_id: The unique identifier of the appendix to be deleted.
        :type appendix_id: int
        :return: Returns True if the appendix was successfully deleted.
        :rtype: bool
        :raises ValueError: If no appendix with the given ID is found.
        :raises Exception: If any other error occurs during the deletion process.
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
