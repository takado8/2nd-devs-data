import json
import re

from data_processing.law_articles_extractor import count_tokens

MAX_TOKENS = 8100
empty = [0]
empty_lines_nb = ['39', '40', '43', '48', '49', '51', '77', '105', '149', '159', '221', '244', '248', '249', '250',
                  '268', '274', '289', '294', '295', '296', '297', '301', '303', '307', '309', '347', '364', '366',
                  '367', '370', '375', '393', '404', '407', '410', '416', '421', '424', '426', '429', '443', '444',
                  '448', '451', '453', '456', '458', '459', '460', '461', '463', '465', '515', '550', '592', '621']


def aaaaa():
    a = '''**1. Zamawiający wyznaczony dla organów administracji rządowej lub jednostek orga-
nizacyjnych podległych tym organom lub przez nie nadzorowanych.**
 Przepis art. **39** Pzp'''
    comment_first_line_pattern = r"^\**1\.\s+[\s*\w*\W*]*-$"
    comment_first_line_regex = re.compile(comment_first_line_pattern)
    for line in a.split('\n'):
        matches = re.findall(comment_first_line_pattern, line.strip())
        print(matches)


def extract_comment_from_article_v2(article, first_line_pattern=None):
    # assuming article ends with **
    comment = []
    result_article = []
    comment_start = False
    first_line = True
    comment_first_line_pattern = first_line_pattern if first_line_pattern \
        else r"^\**1\.\s+[\s*\w*\W*]*\.\*\*"
    comment_first_line_regex = re.compile(comment_first_line_pattern)
    for line in article:
        if first_line:
            result_article.append(line)
            first_line = False
            continue
        stripped = line.strip()
        match = re.search(comment_first_line_regex, stripped)

        if not comment_start and match:
            comment_start = True
            # result_article.append(line)
            # continue

        if comment_start:
            comment.append(line)
        else:
            result_article.append(line)
    if not comment:
        if first_line_pattern:
            empty[0] += 1
        else:
            comment_first_line_pattern_alt = r"^\**1\.\s+[\s*\w*\W*]*\*\*\."
            result_article, comment = extract_comment_from_article_v2(article,
                comment_first_line_pattern_alt)
    # assert len(result_article) > 0
    # assert len(comment) > 0
    return result_article, comment


def extract_article_number(string, expected):
    numbers = re.findall(r'\d+', string)
    number = numbers.pop(0)
    assert int(number) == expected, f'numbers: {numbers}, number: {number}, expected: {expected}'
    # assert len(numbers) == 1, numbers
    return number


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


def process_article(article):
    # article_with_comments = remove_header_type_2(article)
    article_with_comments = remove_empty_lines(article)
    art, comm = extract_comment_from_article_v2(article_with_comments)
    return art, comm


def extract_articles(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    articles = []
    comments = []
    article_pattern = r"^\s*\**Art\.\s\d+\s*"
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
                article, comment = process_article(current_article)
                articles.append(article)
                comments.append(comment)
            current_article = [line]
        elif articles_started:
            # match = re.search(page_header_regex, line)
            # if match:
            #     if header_started:
            #         # end of header
            #         header_started = False
            #         header_lines.append(line)
            #         if len(header_lines) <= 3:
            #             all_headers_lines.extend(header_lines)
            #         elif len(header_lines) > 3:  # not a header
            #             # remove lines with <```>
            #             header_lines.pop(0)
            #             header_lines.pop(-1)
            #             current_article.extend(header_lines)
            #         header_lines.clear()
            #         continue
            #     else:
            #         header_started = True

            if not header_started:
                current_article.append(line)
            else:
                header_lines.append(line)
    article, comment = process_article(current_article)
    articles.append(article)
    comments.append(comment)
    assert len(articles) == len(comments)
    # make sure nothing relevant was removed with empty lines
    assert ''.join(empty_lines).strip() == ''
    return zip(articles, comments)


def split_comment(comment):
    all_sections = []
    current_section = []
    section_start_pattern = r"^\*\*\d+\.[\d+\.]*\s+"
    section_start_regex = re.compile(section_start_pattern)

    for line in comment:
        stripped = line.strip()
        match = re.search(section_start_regex, stripped)
        if match:  # new section starts
            if current_section:
                all_sections.append(current_section)
                current_section = []

        current_section.append(line)
    all_sections.append(current_section)

    for section in all_sections:
        section_string = '\n'.join(section)
        tokens = count_tokens(section_string)
        assert tokens <= MAX_TOKENS, f'Too many tokens: {tokens}'
    return all_sections


def create_entry(comment_string, article_nb):
    return {
        'txt': comment_string,
        "metadata": {
            "chapter": "0",
            "paragraph": article_nb,
            "title": "0",
            "date": "10.02.2023",
            "type": "kdnpzp"
        }
    }


def save_datapoints(output_filename, datapoints):
    with open(output_filename, 'w+', encoding='utf-8') as f:
        json.dump(datapoints, f, ensure_ascii=False)
        # f.write(datapoints_string)
    print(f'{len(datapoints)} entries saved to file: {output_filename}')


def process_comments(filename, output_filename):
    articles_and_comments = extract_articles(filename)

    datapoints = []
    lacking = []
    saved_batches = 1
    for i, article in enumerate(articles_and_comments, start=1):
        # print(i)
        if len(datapoints) % 10 == 0 and datapoints:
            save_datapoints(f"{output_filename}_{saved_batches}.json", datapoints)
            saved_batches += 1
            datapoints.clear()
            return
        article_nb_line = article[0][0]
        article_nb = extract_article_number(article_nb_line.strip(), expected=i)
        comment = article[1]
        comment_string = '\n'.join(comment)
        if comment_string == '' and article_nb in empty_lines_nb:
            art, comment = extract_comment_from_article_v2(article[0],
                r"^\**1\.\s+[\s*\w*\W*]*-$")
        comment_string = '\n'.join(comment)
        if comment_string == '':
            lacking.append(article_nb)
        # print('counting tokens...')
        tokens = count_tokens(comment_string)
        # print(tokens)
        if tokens <= MAX_TOKENS:
            entry = create_entry(comment_string, article_nb)
            datapoints.append(entry)
            # print(f'too long: {article_nb}')
        else:
            all_sections = split_comment(comment)
            for section in all_sections:
                datapoints.append(create_entry('\n'.join(section), article_nb))

    save_datapoints(f"{output_filename}_{saved_batches}.json", datapoints)
    print(f'{saved_batches} batches saved.')
    print(lacking)
    # print(f'too long: {too_long}')


if __name__ == '__main__':
    filename = '../data/md/pzp_comments_v2.md'
    output_filename = '../data/json/pzp_comments_v2_test_10'

    process_comments(filename, output_filename)
    # print(f'empty: {empty}')
    #
    # for i, text in enumerate(extracted_articles[:20], start=1):
    #     print(f"Text {i}:", text)
    #     print("----------")
