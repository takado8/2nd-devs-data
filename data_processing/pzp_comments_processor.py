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
    headers_lines = []
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
                    header_started = False
                    headers_lines.append(line)
                    continue
                else:
                    header_started = True
            if not header_started:
                current_article.append(line)
            else:
                headers_lines.append(line)

    return headers_lines


if __name__ == '__main__':

    # Example usage:
    filename = '../data/md/pzp_comments.csv'
    extracted_articles = extract_articles(filename)

    for i, text in enumerate(extracted_articles[:150], start=1):
        print(f"Text {i}:", text)
        print("----------")