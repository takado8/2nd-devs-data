import re


def extract_paragraphs():

    pattern = r'§ \d+\. '

    text = "This is a sample text. § 1. This is the first paragraph. § 2. This is the second paragraph."

    matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]

    print("Positions of findings:")
    for i, (start, end) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        substring = text[start:next_start]
        print(f"Start: {start}, End: {end}, Match: {text[start:end]}, Extracted: {substring}")


def remove_footer(input_string):
    input_string = """
            Line 1
            Line 2 -123-
            Line 3
            Line 4 -45-
            Line 5
            """
    # Compile the provided pattern
    compiled_pattern = re.compile(r'.*-(\d+)-.*\n')

    # Initialize a counter for removed lines
    removed_lines_count = 0

    # Function to count and remove lines
    def remove_lines(match):
        nonlocal removed_lines_count
        removed_lines_count += 1
        return ''

    # Remove lines matching the pattern and count them
    result_string = re.sub(compiled_pattern, remove_lines, input_string)

    return result_string, removed_lines_count


def find_date(text):
    # Your chapter pattern remains the same
    chapter_pattern = re.compile(r'Rozdział\s+(1)')

    # Updated date pattern to match the examples you provided
    date_pattern = re.compile(r'z\sdnia\s(\d{2}\s\w+\s\d{4})\sr\.')

    # Example usage
    text = """
    Some text here
    z dnia 22 lutego 2021 r.
    z dnia 11 września 2021 r.
    More text
    Rozdział 1
    Chapter content
    z dnia 03 marca 2021 r.
    z dnia 12 września 2021 r.
    More text
    Rozdział 1
    Chapter content
    """

    # Find all occurrences of dates before chapters
    matches = list(re.finditer(date_pattern, text))
    chapter_matches = list(re.finditer(chapter_pattern, text))

    for chapter_match in chapter_matches:
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
                print(f"Chapter {chapter_match.group(1)} - Found date: {one_before_date}")
            else:
                print(f"Chapter {chapter_match.group(1)} - No date found before.")
        else:
            print(f"Chapter {chapter_match.group(1)} - No date found.")


if __name__ == '__main__':
    find_date('')