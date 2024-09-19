import sys
import fitz  # PyMuPDF
import argparse
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_toc_with_pages(pdf_document):
    toc = pdf_document.get_toc(simple=False)
    result = []
    for item in toc:
        if len(item) >= 3:
            level, title, page = item[0], item[1], item[2]
            result.append((level, title, page))
    return result

def split_pdf_by_toc(input_path, output_prefix):
    try:
        pdf_document = fitz.open(input_path)
        toc_with_pages = extract_toc_with_pages(pdf_document)

        if not toc_with_pages:
            logger.warning("No usable table of contents found. Cannot split the PDF.")
            return

        sections = []
        current_section = None
        for i, (level, title, page) in enumerate(toc_with_pages):
            if level == 1:
                if current_section:
                    sections.append(current_section)
                current_section = {'title': title, 'start': page, 'end': -1}
            elif page != -1 and current_section and current_section['start'] == -1:
                current_section['start'] = page

        if current_section:
            sections.append(current_section)

        # Set end pages
        for i in range(len(sections) - 1):
            sections[i]['end'] = sections[i+1]['start'] if sections[i+1]['start'] != -1 else pdf_document.page_count
        if sections:
            sections[-1]['end'] = pdf_document.page_count

        # Create PDFs for each main section
        for i, section in enumerate(sections):
            if section['start'] == -1:
                logger.warning(f"Skipping section '{section['title']}' due to invalid start page")
                continue

            start_page = max(0, section['start'] - 1)  # Ensure we don't have negative page numbers
            end_page = min(section['end'], pdf_document.page_count)

            new_pdf = fitz.open()
            new_pdf.insert_pdf(pdf_document, from_page=start_page, to_page=end_page-1)

            safe_title = "".join(c if c.isalnum() else "_" for c in section['title'])
            output_filename = f"{output_prefix}_{i+1:02d}_{safe_title}.pdf"
            new_pdf.save(output_filename)
            new_pdf.close()

            logger.info(f"Created: {output_filename} (Pages {start_page+1}-{end_page})")

    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        if 'pdf_document' in locals():
            pdf_document.close()

def main():
    parser = argparse.ArgumentParser(description="Split PDF based on table of contents")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_prefix", help="Prefix for output PDF files")

    args = parser.parse_args()
    logger.info(f"Starting PDF splitting process for {args.input_pdf}")
    split_pdf_by_toc(args.input_pdf, args.output_prefix)
    logger.info("PDF splitting process completed")

if __name__ == "__main__":
    main()