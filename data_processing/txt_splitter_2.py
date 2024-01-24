import re
import json


def parse(input_file_path, output_file_path):
    # Define patterns for chapters, paragraphs, and points.
    chapter_pattern = re.compile(r'^\s*Rozdział\s+(\d+)\s+(.*?)\s*$\n', re.MULTILINE)
    paragraph_pattern = re.compile(r'^\s*(§\s+\d+\..*?)(?=^\s*§\s+\d+\.|\Z)', re.MULTILINE | re.DOTALL)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # Find all chapters with titles
    chapters = [(match.start(), match.group(1), match.group(2)) for match in chapter_pattern.finditer(input_text)]

    processed_data = []

    # Parse each chapter
    for i, (start, chapter_nb, title) in enumerate(chapters):
        # Determine the end of the current chapter based on the start of the next chapter
        end = chapters[i + 1][0] if i + 1 < len(chapters) else len(input_text)
        chapter_content = input_text[start:end]

        # Extract paragraphs from the current chapter
        paragraphs = paragraph_pattern.findall(chapter_content)
        for para in paragraphs:
            para_nb = ''
            point_nb = ''

            # Identify the paragraph number
            para_nb_match = re.match(r'§\s+(\d+)\.', para)  # Obtain paragraph number
            if para_nb_match:
                para_nb = para_nb_match.group(1)

            # Extract points within this paragraph
            point_pattern = re.compile(r'^(\d+)\.(.*?)(?=\n\d+\.|\n§|^\Z)', re.MULTILINE | re.DOTALL)
            points = point_pattern.findall(para)

            if points:  # Paragraph has points
                for pt_nb, pt_text in points:
                    processed_data.append({
                        'txt': pt_text.strip(),
                        'chapter': chapter_nb.strip(),
                        'paragraph': para_nb.strip(),
                        'point': pt_nb.strip(),
                        'title': title.strip()
                    })
            else:  # Paragraph without points; treat the whole paragraph text as point '1'
                processed_data.append({
                    'txt': para.strip(),
                    'chapter': chapter_nb.strip(),
                    'paragraph': para_nb.strip(),
                    'point': '1',
                    'title': title.strip()
                })

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parse(input_file_path='../data/txt/input.txt',
        output_file_path='../data/txt/output.json')
