import logging

from peewee import DoesNotExist

from ..models.data import Thesis  # Assuming Reference model exists
from ..utils.formatter import format_to_apa

logger = logging.getLogger(__name__)


def generate_apa_formatted_document(thesis_id):
    """
    Generates an APA-formatted document for the given thesis ID.
    :param thesis_id: ID of the thesis to format.
    :return: Path to the formatted APA Word document.
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
                "institution": "ThesisGenius University",  # Customize this value
                "abstract": thesis.abstract,
                "content": thesis.content,
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
