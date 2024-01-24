def extract_paragraphs():
    import re

    pattern = r'§ \d+\. '

    text = "This is a sample text. § 1. This is the first paragraph. § 2. This is the second paragraph."

    matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]

    print("Positions of findings:")
    for i, (start, end) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        substring = text[start:next_start]
        print(f"Start: {start}, End: {end}, Match: {text[start:end]}, Extracted: {substring}")


if __name__ == '__main__':
    extract_paragraphs()