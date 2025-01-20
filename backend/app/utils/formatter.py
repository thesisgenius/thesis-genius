import logging

from docx import Document

logger = logging.getLogger(__name__)


def format_to_apa(thesis_data, references):
    """
    Formats thesis data into APA-compliant Word format.
    :param thesis_data: Dictionary containing thesis metadata (title, author, abstract).
    :param references: List of dictionaries containing reference metadata.
    :return: Path to the formatted APA Word document.
    """
    # Validate thesis data
    try:
        validate_thesis_data(thesis_data)
    except ValueError as e:
        logger.error(f"Invalid thesis data: {e}")
        raise

    # Validate references
    try:
        validate_references(references)
    except ValueError as e:
        logger.error(f"Invalid reference data: {e}")
        raise

    try:
        # Create a new Word document
        doc = Document()

        # Add Title Page
        add_title_page(doc, thesis_data)

        # Add Abstract Section
        if thesis_data.get("abstract"):
            add_abstract_section(doc, thesis_data["abstract"])

        # Add Content Section
        if thesis_data.get("content"):
            add_content_section(doc, thesis_data["content"])

        # Add References Section
        if references:
            add_references_section(doc, references)

        # Save document to a temporary location
        temp_file = "/tmp/apa_formatted_thesis.docx"
        doc.save(temp_file)

        logger.info(f"APA-formatted document saved at {temp_file}")
        return temp_file

    except Exception as e:
        logger.error(f"An error occurred while formatting the APA document: {e}")
        raise RuntimeError("Failed to format the APA document.") from e


def validate_thesis_data(thesis_data):
    """
    Validates the thesis metadata.
    :param thesis_data: Dictionary containing thesis metadata.
    """
    required_fields = ["title", "student", "institution"]
    missing_fields = [field for field in required_fields if not thesis_data.get(field)]
    if missing_fields:
        raise ValueError(
            f"Missing required thesis data fields: {', '.join(missing_fields)}"
        )


def validate_references(references):
    """
    Validates the reference metadata.
    :param references: List of dictionaries containing reference metadata.
    """
    if not isinstance(references, list):
        raise ValueError("References should be a list of dictionaries.")
    for i, ref in enumerate(references):
        if not isinstance(ref, dict):
            raise ValueError(f"Reference at index {i} is not a dictionary.")
        required_fields = ["author", "title", "publication_year"]
        missing_fields = [field for field in required_fields if not ref.get(field)]
        if missing_fields:
            raise ValueError(
                f"Reference at index {i} is missing required fields: {', '.join(missing_fields)}"
            )


def add_title_page(doc, thesis_data):
    """
    Adds the title page to the document.
    :param doc: Word document object.
    :param thesis_data: Dictionary containing thesis metadata.
    """
    doc.add_paragraph(thesis_data["title"]).bold = True
    doc.add_paragraph(f"Author: {thesis_data['student']}")
    doc.add_paragraph(f"Institution: {thesis_data['institution']}")
    doc.add_paragraph("\n\n")  # Add spacing


def add_abstract_section(doc, abstract):
    """
    Adds the abstract section to the document.
    :param doc: Word document object.
    :param abstract: Abstract content of the thesis.
    """
    doc.add_heading("Abstract", level=1)
    doc.add_paragraph(abstract)
    doc.add_paragraph("\n\n")


def add_content_section(doc, content):
    """
    Adds the content section to the document.
    :param doc: Word document object.
    :param content: Main content of the thesis.
    """
    doc.add_heading("Content", level=1)
    doc.add_paragraph(content)


def add_references_section(doc, references):
    """
    Adds the references section to the document.
    :param doc: Word document object.
    :param references: List of dictionaries containing reference metadata.
    """
    doc.add_heading("References", level=1)
    for ref in references:
        citation = f"{ref['author']} ({ref['publication_year']}). {ref['title']}."
        if ref.get("journal"):
            citation += f" {ref['journal']}."
        if ref.get("doi"):
            citation += f" DOI: {ref['doi']}"
        doc.add_paragraph(citation)
