import json
import re
import tiktoken

MAX_TOKENS = 8100


def split_longer_articles(law_article):
    # Define the pattern for finding points
    pattern = re.compile(r'\d+\)\s')
    # Split the law article using the pattern
    points = re.split(pattern, law_article)
    points = [p.strip() for p in points]
    title = points.pop(0)
    return title, points


def count_tokens(string, encoding_name='cl100k_base') -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def remove_footer_lines_pzp_law(text):
    pattern = r'®\s+ApexNet\. Wiedza, która chroni\n'
    regex = re.compile(pattern)
    # Remove the matched lines
    result = regex.sub('', text)
    return result


def law_extractor(input_string):
    def extract_title(idx):
        idx += 2
        stop_idx = -1
        for i in range(idx, len(input_string)):

            if input_string[i] == '\n':
                stop_idx = i
                break
        return input_string[idx:stop_idx].strip()

    chapter_pattern = re.compile(r'Rozdział\s+(\d+)')
    article_pattern = re.compile(r"(Art\.\s+\d+\. .*?)(?=Art\.\s+\d+\. |$)", re.DOTALL)

    matches = [match for match in re.finditer(article_pattern, input_string)]
    chapter_titles = []

    # Find all chapter titles and their indices
    for chapter_match in chapter_pattern.finditer(input_string):
        chapter_start = chapter_match.start()
        chapter_end = input_string.find('\n', chapter_start)

        title = extract_title(chapter_end)
        print(f'title: {title}')
        chapter_titles.append((chapter_start, title))
    chapter_titles = sorted(chapter_titles)
    print(chapter_titles)
    articles = []
    # Your loop to iterate over matches
    for i, match in enumerate(matches, start=1):
        # Find the index of the previous chapter
        print(f'match start: {match.start()}')

        title = chapter_titles[0]
        j = 0
        for entry in chapter_titles:
            if entry[0] > match.start():
                break

            title = chapter_titles[j]
            j += 1
        article = match.group().strip()
        txt = remove_footer_lines_pzp_law(article)
        tokens = count_tokens(txt)
        if tokens > MAX_TOKENS:
            article_start, parts = split_longer_articles(txt)
            print(f'splitting art {i} in {len(parts)} parts')

            for part in parts:
                entry = {
                    'txt': f'{article_start} {part}',
                    "metadata": {
                        "chapter": "0",
                        "paragraph": i,
                        "title": title[1],
                        "date": "11.09.2019",
                        "type": "main_law"
                    }
                }
                articles.append(entry)
        else:
            entry = {
                'txt': txt,
                "metadata": {
                    "chapter": "0",
                    "paragraph": i,
                    "title": title[1],
                    "date": "11.09.2019",
                    "type": "main_law"
                }
            }
            articles.append(entry)
    return articles


def process_and_save_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    articles = law_extractor(text)
    print(f'{len(articles)} extracted.')
    with open(output_path, 'w+', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False)
    print(f'saved to file: {output_path}')


if __name__ == '__main__':
    process_and_save_file('../data/txt/pzp.txt',
        '../data/json/pzp_uncut_no_ascii.json')