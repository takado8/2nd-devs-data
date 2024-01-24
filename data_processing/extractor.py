import re


def find_dates(text):
    chapter_pattern = re.compile(r'Rozdział\s+(1)')
    date_pattern = re.compile(r'z\sdnia\s(\d{2}\s\w+\s\d{4})\sr\.')
    # Find all occurrences of dates before chapters
    matches = list(re.finditer(date_pattern, text))
    chapter_matches = list(re.finditer(chapter_pattern, text))
    dates_dict = {}
    i=0
    for chapter_match in chapter_matches:
        i+=1
        # Find the closest date before the chapter occurrence
        closest_date = None
        for date_match in reversed(matches):
            if date_match.end() < chapter_match.start():
                closest_date = date_match.group(1)
                break

        # Find the index of the closest date and get the one before it
        if closest_date:
            closest_index = matches.index(date_match)
            if closest_index > 0:
                one_before_date = matches[closest_index - 1].group(1)
                # print(f"Chapter {chapter_match.group(1)} - Found date: {one_before_date}")
                dates_dict[i] = one_before_date
            else:
                print(f"\nChapter {chapter_match.group(1)} - No date found before.\n")
        else:
            print(f"\nChapter {chapter_match.group(1)} - No date found.\n")
    return dates_dict


def remove_footers(input_string):
    compiled_pattern = re.compile(r'.*–(\d+)–.*\n')

    removed_lines_count = 0

    def remove_lines(match):
        nonlocal removed_lines_count
        removed_lines_count += 1
        return ''

    # Remove lines matching the pattern and count them
    result_string = re.sub(compiled_pattern, remove_lines, input_string)

    return result_string, removed_lines_count


def extract_paragraphs(text):
    paragraph_pattern = r'§ \d+\. '
    matches = [(match.start(), match.end()) for match in re.finditer(paragraph_pattern, text)]

    # print("Positions of findings:")
    paragraphs = []
    for i, (start, end) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        substring = text[start:next_start]
        paragraphs.append(substring)
        # print(f"Start: {start}, End: {end}, Match: {text[start:end]}, Extracted: {substring}")
    return paragraphs


def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    dates_dict = find_dates(text)
    print(dates_dict)
    return
    text, lines_removed_nb = remove_footers(text)
    print(f"Lines removed: {lines_removed_nb}")
    chapter_pattern = re.compile(r'Rozdział\s+(\d+)')
    # Find all chapters
    chapters = [m for m in chapter_pattern.finditer(text)]
    paragraph_nb = 0
    records = []
    for i, chapter in enumerate(chapters):
        chapter_nb = chapter.group(1)
        # Determine the text scope for the current chapter
        start = chapter.end()
        end = chapters[i + 1].start() if i + 1 < len(chapters) else len(text)
        chapter_text = text[start:end]

        # Title is first line of each chapter
        title = chapter_text.strip().splitlines()[0]
        print(f'Chapter {chapter_nb} title: {title}')
        # print(f'TXT: {chapter_text}')
        paragraphs = extract_paragraphs(chapter_text)

        for paragraph in paragraphs:
            paragraph_nb += 1
            print(f'Paragraph {paragraph_nb}: {paragraph}')
            record = {
                "txt": paragraph,
                "chapter": chapter_nb,
                "paragraph": paragraph_nb,
                "title": title
            }
            records.append(record)

    return records


if __name__ == '__main__':
    file_path = "../data/txt/dzienniki.txt"  # Replace with the actual path to your text file
    process_text(file_path)
