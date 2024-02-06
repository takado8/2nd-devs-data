import json
import re


def extract_articles(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    articles = []
    article_pattern = r"\*\*Art\.\s\d+\.\s*"
    article_regex = re.compile(article_pattern)
    page_header_pattern = r"```"
    page_header_regex = re.compile(page_header_pattern)

    current_article = []
    articles_started = False
    header_started = False
    all_headers_lines = []
    header_lines = []
    empty_lines = []
    for line in lines:
        match = re.search(article_regex, line)
        if match:
            if not articles_started:
                articles_started = True
            # new article starts
            if current_article:
                articles.append(''.join(current_article))
            current_article = [line]
        elif articles_started:
            match = re.search(page_header_regex, line)
            if match:
                if header_started:
                    # end of header
                    header_started = False
                    header_lines.append(line)
                    if len(header_lines) <= 3:
                        all_headers_lines.extend(header_lines)
                    elif len(header_lines) > 3:  # not a header
                        # remove lines with <```>
                        header_lines.pop(0)
                        header_lines.pop(-1)
                        current_article.extend(header_lines)
                    header_lines.clear()
                    continue
                else:
                    header_started = True
                    # remove previous 2 empty lines
                    for _ in range(2):
                        if current_article[-1].strip() == '':
                            empty1 = current_article.pop(-1)
                            empty_lines.append(empty1)

            if not header_started:
                current_article.append(line)
            else:
                header_lines.append(line)

    # make sure nothing relevant was removed with empty lines
    assert ''.join(empty_lines).strip() == ''
    return articles


if __name__ == '__main__':

    # Example usage:
    filename = '../data/md/pzp_comments.csv'
    extracted_articles = extract_articles(filename)
    print(f'Extracted: {len(extracted_articles)}')
    # with open("aaaaaaaaaa.json", 'w+', encoding='utf-8')as f:
    #     json.dump(extracted_articles, f)
    for i, text in enumerate(extracted_articles[:15], start=1):
        print(f"Text {i}:", text)
        print("----------")
