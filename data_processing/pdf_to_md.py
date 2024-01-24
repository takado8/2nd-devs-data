from pdfminer.high_level import extract_text
import os
import re

# Use regular expressions to identify list items.
list_item_re = re.compile(r'^(\d+\))\s*(.*)')


def preprocess_pdf_text(lines):
    """ Preprocess the PDF text by merging lines that belong to list items. """
    processed_lines = []
    for line in lines:
        match = list_item_re.match(line)
        if match:
            # Start a new list item
            item_number = match.group(1)
            content = match.group(2).strip()
            new_line = f"{item_number} {content}"
            processed_lines.append(new_line)
        elif processed_lines:
            # Continue adding to the last line if it's not a new list item
            processed_lines[-1] += (line.strip() + ' ')
        else:
            # Regular line that doesn't belong to a list
            processed_lines.append(line)
    return processed_lines


def convert_lines_to_markdown(processed_lines):
    """ Convert the preprocessed text lines to Markdown format. """
    # Placeholder for Markdown output
    markdown_lines = []
    for line in processed_lines:
        # Check for a list item
        match = list_item_re.match(line)
        if match:
            item_number = match.group(1)[:-1]  # Remove the closing parenthesis
            content = match.group(2).strip()
            # Format as an ordered list item
            markdown_lines.append(f"{item_number}. {content}\n")
        else:
            # Handle non-list lines (which may include empty lines)
            markdown_lines.append(line + '\n')
    return markdown_lines


def pdf_to_markdown(pdf_path):
    # Extract text from the PDF
    text = extract_text(pdf_path)
    lines = text.split('\n')

    # Preprocess lines to fix list items
    processed_lines = preprocess_pdf_text(lines)

    # Convert processed lines to Markdown
    markdown_lines = convert_lines_to_markdown(processed_lines)

    # Join the Markdown lines into a single string
    markdown_text = ''.join(markdown_lines)

    # Save to markdown file
    md_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.md'
    with open(md_filename, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_text)

    print(f"Markdown file saved as {md_filename}")


if __name__ == '__main__':
    # Usage
    pdf_path = '../data/pdf/dzienniki.pdf'  # Replace with your PDF file path
    pdf_to_markdown(pdf_path)
