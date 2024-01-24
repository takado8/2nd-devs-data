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


if __name__ == '__main__':
    text = """
        Line 1
        Line 2 -123-
        Line 3
        Line 4 -45-
        Line 5
        """
    result, deleted = remove_footer(text)
    print(result)
    print(deleted)