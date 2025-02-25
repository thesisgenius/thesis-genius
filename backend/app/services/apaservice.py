# apaservice.py
from peewee import DoesNotExist

from ..models.data import Abstract  # plus any model for citations, etc.
from ..models.data import (Appendix, BodyPage, CopyrightPage, DedicationPage,
                           Figure, Reference, SignaturePage, TableEntry,
                           TableOfContents, Thesis)


class APAService:
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

    def get_thesis_data(self, thesis_id):
        """
        Returns a single dict aggregator with all pieces of the Thesis needed
        for APA formatting. The frontend or the 'formatter.py' can convert this
        aggregator to HTML, DOCX, or PDF as needed.
        """
        try:
            query = Thesis.select().where(Thesis.id == thesis_id)
            thesis = query.get_or_none()
        except DoesNotExist:
            raise ValueError(f"Thesis {thesis_id} not found")

        # 1) Title/Cover data (assuming these fields on Thesis)
        cover_data = {
            "title": thesis.title,
            "author": thesis.author,
            "affiliation": thesis.affiliation,
            "course": thesis.course,
            "instructor": thesis.instructor,
            "due_date": thesis.due_date.strftime("%Y-%m-%d") if thesis.due_date else "",
        }

        # 2) Table of Contents
        toc_list = []
        toc_entries = (
            TableOfContents.select()
            .where(TableOfContents.thesis == thesis_id)
            .order_by(TableOfContents.order)
        )
        for entry in toc_entries:
            toc_list.append(
                {
                    "section_title": entry.section_title,
                    "page_number": entry.page_number,
                    "order": entry.order,
                }
            )

        # 3) Copyright
        try:
            cp = CopyrightPage.get(CopyrightPage.thesis == thesis_id)
            copyright_data = {
                "content": cp.content,
                "year": cp.created_at.year,
                "name": thesis.author,
            }
        except DoesNotExist:
            copyright_data = {}

        # 4) Signature
        try:
            sig = SignaturePage.get(SignaturePage.thesis == thesis_id)
            signature_data = {
                "content": sig.content,
                "name": (
                    sig.student.first_name + " " + sig.student.last_name
                    if sig.student
                    else thesis.author
                ),
                "affiliation": thesis.affiliation,
                "degree": thesis.degree,
                "instructor": thesis.instructor,
            }
        except DoesNotExist:
            signature_data = {}

        # 5) Abstract
        try:
            abs_obj = Abstract.get(Abstract.thesis == thesis_id)
            abstract_data = {"text": abs_obj.text}
        except DoesNotExist:
            abstract_data = {}

        # 6) Dedication
        try:
            ded = DedicationPage.get(DedicationPage.thesis == thesis_id)
            dedication_data = {"content": ded.content}
        except DoesNotExist:
            dedication_data = {}

        # 7) Body (Chapters)
        body_list = []
        body_pages = (
            BodyPage.select()
            .where(BodyPage.thesis == thesis_id)
            .order_by(BodyPage.page_number)
        )
        for bp in body_pages:
            body_list.append(
                {
                    "page_number": bp.page_number,
                    "content": bp.body,
                }
            )

        # 8) Appendices
        appendices_list = []
        apps = Appendix.select().where(Appendix.thesis == thesis_id)
        for app in apps:
            appendices_list.append({"title": app.title, "content": app.content})

        # 9) References
        references_list = []
        refs = Reference.select().where(Reference.thesis == thesis_id)
        for ref in refs:
            references_list.append(
                {
                    "author": ref.author,
                    "title": ref.title,
                    "journal": ref.journal,
                    "year": ref.publication_year,
                    "publisher": ref.publisher,
                    "doi": ref.doi,
                }
            )

        # 10) Figures
        figs = Figure.select().where(Figure.thesis == thesis_id)
        figures_list = []
        for f in figs:
            figures_list.append({"caption": f.caption, "file_path": f.file_path})

        # 11) Tables
        table_entries = TableEntry.select().where(TableEntry.thesis == thesis_id)
        tables_list = []
        for t in table_entries:
            tables_list.append({"caption": t.caption, "file_path": t.file_path})

        # 12) Additional citations if you have them
        # citations_list = ...

        # Combine
        aggregator = {
            "cover": cover_data,
            "table_of_contents": toc_list,
            "copyright": copyright_data,
            "signature": signature_data,
            "abstract": abstract_data,
            "dedication": dedication_data,
            "body": body_list,
            "appendices": appendices_list,
            "references": references_list,
            "figures": figures_list,
            "tables": tables_list,
            # "citations": citations_list
        }
        return aggregator
