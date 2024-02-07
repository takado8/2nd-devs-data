from bs4 import BeautifulSoup

# Specify the path to your local HTML file
file_path = '../data/html/Komentarz-Prawo-zamowien-publicznych.html'


def process_html(filepath):
    # Read the HTML content from the local file
    with open(filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    def extract_text_with_bold(node):
        if isinstance(node, str):  # If it's a string, return the text
            return node
        else:
            result = ''
            for child in node.contents:
                # Recursively extract text and preserve bold formatting for certain tags
                if child.name in ['h1', 'h2', 'h3', 'b']:
                    result += f'**{extract_text_with_bold(child)}** '
                elif child.name == 'p':
                    if 's17' in child.get('class', []):
                        # Wrap text inside <p class="s17"> tags with double asterisks for bold formatting
                        result += f'**{extract_text_with_bold(child)}** '
                    else:
                        # Preserve the text inside other <p> tags without modifications
                        result += extract_text_with_bold(child)
                elif child.name == 'br':
                    result += '\n'  # Add newline for <br> tags
                else:
                    result += extract_text_with_bold(child)
            return result
    text_with_bold = extract_text_with_bold(soup)
    print(text_with_bold[2000000: 5000000])


if __name__ == '__main__':
    process_html(file_path)