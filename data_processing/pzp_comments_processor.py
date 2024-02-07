import json
import re

numbers_of = [0, 0]


def extract_comment_from_article(article):
    comment = []
    result_article = []
    comment_start = False
    first_line = True
    for line in article:
        if first_line:
            result_article.append(line)
            first_line = False
            continue
        stripped = line.strip()
        if not comment_start and stripped[-1] == '*' and stripped[-2] == '*':
            comment_start = True
            result_article.append(line)
            continue

        if comment_start:
            comment.append(line)
        else:
            result_article.append(line)
    # result_article_str = ''.join(result_article)
    # comment_str = ''.join(comment)
    # print(f'\n\nArticle: {result_article_str}\nComment: {comment_str}')
    # assert len(result_article) > 0
    # assert len(comment) > 0
    if len(comment) <= 0:
        numbers_of[0] += 1
    if len(article) <= 0:
        numbers_of[1] += 1
    return result_article, comment


def extract_article_number(string):
    numbers = re.findall(r'\d+', string)
    assert len(numbers) == 1
    return numbers.pop()


def remove_empty_lines(article):
    result = []
    empty_lines = []
    for line in article:
        if line.strip() != '':
            result.append(line)
        else:
            empty_lines.append(line)
    # make sure only empty lines were removed
    assert ''.join(empty_lines).strip() == ''
    return result


def remove_header_type_2(lines):
    result_lines = []
    removed_lines = []
    header_pattern = r"\*\*Art\.\s\d+\*\*"
    header_regex = re.compile(header_pattern)
    for line in lines:
        match = re.search(header_regex, line)
        if match:
            removed_lines.append(line)
        else:
            result_lines.append(line)
    return result_lines


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
                current_article = remove_header_type_2(current_article)
                current_article = remove_empty_lines(current_article)
                extract_comment_from_article(current_article)
                articles.append(current_article)
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

            if not header_started:
                current_article.append(line)
            else:
                header_lines.append(line)
    articles.append(current_article)
    extract_comment_from_article(current_article)

    # make sure nothing relevant was removed with empty lines
    assert ''.join(empty_lines).strip() == ''
    return articles


def process_comments(filename, output_filename):
    articles = extract_articles(filename)
    datapoints = []
    for i, article in enumerate(articles, start=1):
        article_nb_line = article[0]
        article_nb = extract_article_number(article_nb_line.strip())
        # print(f'{i}: {article_nb}')
        article_string = ''.join(article)
        entry = {
            'txt': article_string,
            "metadata": {
                "chapter": "0",
                "paragraph": article_nb,
                "title": "0",
                "date": "20.05.2021",
                "type": "kdnpzp"
            }
        }
        datapoints.append(entry)
        # print(f'{i}: {article_string}')
    # with open(output_filename, 'w+', encoding='utf-8') as f:
    #     # json.dump(datapoints, f)
    #     f.write(''.join([''.join(article) for article in articles]))
    # print(f'{len(datapoints)} entries saved to file: {output_filename}')


if __name__ == '__main__':
    filename = '../data/md/pzp_comments.md'
    output_filename = '../data/json/pzp_comments.txt'

    process_comments(filename, output_filename)
    print(numbers_of)
    #
    # for i, text in enumerate(extracted_articles[:20], start=1):
    #     print(f"Text {i}:", text)
    #     print("----------")
