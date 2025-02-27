# formatter.py
import io

import pdfkit
from app.utils.apa import create_apa_docx


class APAFormatter:

    @staticmethod
    def to_html(data: dict) -> str:
        """
        Generates an APA 7–style HTML that, when printed,
        uses near-APA margins, fonts, line spacing, etc.
        """
        cover = data.get("cover", {})
        toc_list = data.get("table_of_contents", [])
        # etc.

        # Instead of relying on external .css,
        # we embed a minimal style block that sets TNR, 12pt, double spacing, 1" margins:
        # (You could also keep it external in apaStyle.css.)
        style_block = """
        <style>
        /* Basic APA 7 styling embedded */
        body {
          font-family: "Times New Roman", serif;
          font-size: 12pt;
          line-height: 2;
          margin: 1in; /* 1-inch margins all around */
        }
        .apa-page {
          position: relative;
          page-break-after: always;
          margin-bottom: 2em;
        }
        .apa-running-head {
          position: absolute;
          top: 0.5in;
          left: 1in;
          font-weight: bold;
          text-transform: uppercase;
          font-size: 12pt;
        }
        .apa-page-number {
          position: absolute;
          top: 0.5in;
          right: 1in;
          font-size: 12pt;
        }
        .apa-title {
          text-align: center;
          margin-top: 3in; /* push it down */
          font-weight: bold;
          font-size: 16pt;
        }
        .apa-heading-1 {
          text-align: center;
          font-size: 14pt;
          font-weight: bold;
          margin-top: 2em;
          margin-bottom: 0.5em;
        }
        .apa-heading-2 {
          text-align: left;
          font-size: 12pt;
          font-weight: bold;
          margin-top: 1.5em;
          margin-bottom: 0.5em;
        }
        .apa-paragraph {
          text-indent: 0.5in;
          text-align: justify;
          margin-bottom: 1em;
        }
        .apa-abstract {
          text-align: left;
          margin: 0.5in 1in;
          text-indent: 0.5in;
        }
        /* references with hanging indent */
        .apa-references {
          margin-left: 0.5in;
        }
        .apa-reference-entry {
          text-indent: -0.5in;
          margin-left: 0.5in;
          margin-bottom: 1em;
        }
        /* etc. for other specialized classes */
        </style>
        """

        html_parts = [f"<!DOCTYPE html><html><head>{style_block}</head><body>"]

        # 1) Cover Page
        # In APA 7 for student papers, running head is optional, but let's keep it for professional
        running_head_txt = f"Running head: {cover.get('title','').upper()}"
        html_parts.append(
            f"""
        <div class="apa-page" style="text-align:center;">
           <div class="apa-running-head">{running_head_txt}</div>
           <div class="apa-page-number">1</div>
           <h1 class="apa-title">{cover.get('title','')}</h1>
           <p>{cover.get('author','')}</p>
           <p>{cover.get('affiliation','')}</p>
           <p>{cover.get('course','')}</p>
           <p>{cover.get('instructor','')}</p>
           <p>{cover.get('due_date','')}</p>
        </div>
        """
        )

        # 2) Table of Contents (2nd page)
        page_counter = 2
        toc_html = []
        for entry in toc_list:
            toc_html.append(
                f"<p>{entry['section_title']} ....... {entry.get('page_number','')}</p>"
            )
        if toc_html:
            html_parts.append(
                f"""
            <div class="apa-page">
              <div class="apa-running-head">{running_head_txt}</div>
              <div class="apa-page-number">{page_counter}</div>
              <h2 class="apa-heading-1">Table of Contents</h2>
              {''.join(toc_html)}
            </div>
            """
            )
            page_counter += 1

        # 3) Abstract
        abs_data = data.get("abstract", {})
        if abs_data.get("text"):
            html_parts.append(
                f"""
            <div class="apa-page">
              <div class="apa-running-head">{running_head_txt}</div>
              <div class="apa-page-number">{page_counter}</div>
              <h2 class="apa-heading-1">Abstract</h2>
              <p class="apa-abstract">{abs_data['text']}</p>
            </div>
            """
            )
            page_counter += 1

        # 4) Body (Chapters)
        body = data.get("body", [])
        for bp in body:
            page_number = bp.get("page_number", "")
            content = bp.get("content", "")
            html_parts.append(
                f"""
            <div class="apa-page">
              <div class="apa-running-head">{running_head_txt}</div>
              <div class="apa-page-number">{page_counter}</div>
              <h3 class="apa-heading-2">Chapter {page_number}</h3>
              <div class="apa-paragraph">{content}</div>
            </div>
            """
            )
            page_counter += 1

        # 5) References
        refs = data.get("references", [])
        if refs:
            ref_entries = []
            for r in refs:
                author = r.get("author", "")
                year = r.get("year", "")
                title = r.get("title", "")
                # naive example
                ref_entries.append(
                    f"""
                  <div class="apa-reference-entry">
                    {author} ({year}). <i>{title}</i>.
                  </div>
                """
                )
            html_parts.append(
                f"""
            <div class="apa-page">
              <div class="apa-running-head">{running_head_txt}</div>
              <div class="apa-page-number">{page_counter}</div>
              <h2 class="apa-heading-1">References</h2>
              <div class="apa-references">
                {''.join(ref_entries)}
              </div>
            </div>
            """
            )
            page_counter += 1

        # ... plus signature, dedication, appendices, figures, tables, etc.

        html_parts.append("</body></html>")
        return "".join(html_parts)

    # end to_html

    @staticmethod
    def to_docx(data: dict) -> io.BytesIO:
        """
        Creates a Word doc with:
          - 1" margins
          - Times New Roman, 12pt
          - Double-spacing
          - Running head, page numbering
          - Title page, separate pages for each section
        """
        return create_apa_docx(data)

    @staticmethod
    def to_pdf(data: dict) -> io.BytesIO:
        """
        Convert the same aggregator data to PDF by using the HTML approach
        then passing it to pdfkit or weasyprint.
        """
        html_str = APAFormatter.to_html(data)
        pdf_bytes = pdfkit.from_string(html_str, False)
        return io.BytesIO(pdf_bytes)
