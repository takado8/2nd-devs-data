from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, page_numbers, output_dir):
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        total_pages = len(pdf_reader.pages)  # Update to use len(pdf_reader.pages)

        # Validate page numbers
        page_numbers = sorted(set(page_numbers))  # Remove duplicates and ensure order
        page_numbers.append(total_pages)  # Add the end page

        if page_numbers[-1] > total_pages:
            raise ValueError("Invalid page number in the list.")

        output_pdfs = []

        for i in range(len(page_numbers) - 1):
            start_page = page_numbers[i]
            end_page = page_numbers[i + 1] - 1
            output_pdf_path = f"{output_dir}/output_part_{i + 1}.pdf"

            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer = PdfWriter()

                for page_num in range(start_page, end_page + 1):
                    pdf_writer.add_page(pdf_reader.pages[page_num])  # Update to use `pages` attribute

                pdf_writer.write(output_file)
                output_pdfs.append(output_pdf_path)

    return output_pdfs


if __name__ == '__main__':
    pdf_path = '../data/Segregator_11-scalone.pdf'
    page_numbers = [48, 92, 757, 1064]
    resulting_pdfs = split_pdf(pdf_path, output_dir='../data', page_numbers=page_numbers)
    print("Split PDFs:", resulting_pdfs)
