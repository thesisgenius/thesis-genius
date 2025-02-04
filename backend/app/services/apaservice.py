import logging

from peewee import DoesNotExist

from ..models.data import Thesis  # Assuming Reference model exists
from ..utils.formatter import format_to_apa

logger = logging.getLogger(__name__)


def generate_apa_formatted_document(thesis_id):
    """
    Generates an APA-formatted document for a specified thesis based on its ID. The function retrieves
    the thesis and its associated references from the database, prepares the relevant data,
    and formats the thesis into an APA-compliant document. If any step fails due to missing or invalid
    data, corresponding exceptions are raised.

    :param thesis_id: The ID of the thesis for which the APA-formatted document is generated.
    :type thesis_id: int
    :return: The file path of the generated APA-formatted document.
    :rtype: str

    :raises ValueError: If the thesis or its references are missing or invalid.
    :raises RuntimeError: If any unexpected error occurs during document generation.
    """
    try:
        # Fetch thesis data from the database
        thesis = Thesis.get_or_none(Thesis.id == thesis_id)
        if not thesis:
            logger.error(f"Thesis with ID {thesis_id} not found.")
            raise ValueError(f"Thesis with ID {thesis_id} not found.")

        # Fetch references associated with the thesis
        try:
            references = [
                {
                    "author": ref.author,
                    "title": ref.title,
                    "journal": ref.journal,
                    "publication_year": ref.publication_year,
                    "publisher": ref.publisher,
                    "doi": ref.doi,
                }
                for ref in thesis.references
            ]
        except AttributeError as e:
            logger.error(f"Error fetching references for thesis {thesis_id}: {e}")
            raise ValueError("Invalid reference data associated with the thesis.")

        # Prepare thesis data
        try:
            thesis_data = {
                "title": thesis.title,
                "student": f"{thesis.student.first_name} {thesis.student.last_name}",
                "instructor": f"{thesis.instructor}",
                "course": f"{thesis.course}",
                "institution": f"{thesis.student.institution}",  # Customize this value
                "abstract": thesis.abstract,
                "content": thesis.content,
                "submission_date": thesis.updated_at.strftime("%B %d, %Y"),
            }
        except AttributeError as e:
            logger.error(f"Error preparing thesis data for ID {thesis_id}: {e}")
            raise ValueError(
                "Invalid thesis data. Please ensure all fields are populated."
            )

        # Format document
        try:
            apa_document_path = format_to_apa(thesis_data, references)
        except Exception as e:
            logger.error(f"Error generating APA document for thesis {thesis_id}: {e}")
            raise RuntimeError(f"Failed to generate APA document: {e}")

        logger.info(f"APA document generated successfully for thesis ID {thesis_id}.")
        return apa_document_path

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise
    except DoesNotExist as e:
        logger.error(f"Database entry does not exist: {e}")
        raise ValueError(f"Thesis with ID {thesis_id} does not exist.")
    except Exception as e:
        logger.error(f"Unexpected error for thesis ID {thesis_id}: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}")
