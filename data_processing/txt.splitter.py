import re

def process_text(text):
    # Define patterns to match chapters, titles, paragraphs, and points
    chapter_pattern = re.compile(r'Rozdział\s+(\d+)')
    title_pattern = re.compile(r'\n([^\n§]+)\n§')
    paragraph_pattern = re.compile(r'§ (\d+(?:\.\d+)?)\.')
    point_pattern = re.compile(r'\n(\d+)\)\s+(.+?)(?=\n\d+\)|\n§|\Z)', re.DOTALL)

    # Find all chapters
    chapters = [m for m in chapter_pattern.finditer(text)]

    # Iterate over chapters to find titles, paragraphs, and points
    records = []
    for i, chapter in enumerate(chapters):
        chapter_nb = chapter.group(1)
        # Determine the text scope for the current chapter
        start = chapter.end()
        end = chapters[i + 1].start() if i + 1 < len(chapters) else len(text)
        chapter_text = text[start:end]

        # Find the title for the current chapter
        title_match = title_pattern.search(chapter_text)
        title = title_match.group(1).strip() if title_match else ""

        # Find all paragraphs in the chapter
        paragraphs = [m for m in paragraph_pattern.finditer(chapter_text)]

        # Iterate over paragraphs to find points
        for j, paragraph in enumerate(paragraphs):
            paragraph_nb = paragraph.group(1)
            # Determine the text scope for the current paragraph, including potential points
            start = paragraph.end()
            end = paragraphs[j + 1].start() if j + 1 < len(paragraphs) else len(chapter_text)
            paragraph_text = chapter_text[start:end]

            # Find and iterate over all points in the paragraph
            for point in point_pattern.finditer(paragraph_text):
                point_nb = point.group(1)
                point_text = point.group(2).strip().replace("\n", " ")  # Normalize text

                # Store extracted data in a structured record
                record = {
                    "txt": point_text,
                    "chapter": chapter_nb,
                    "paragraph": paragraph_nb,
                    "point": point_nb,
                    "title": title
                }
                records.append(record)

    return records

text_to_process = """Rozdział 1
Przepisy ogólne
§ 1. Rozporządzenie określa:
1) tryb przeprowadzania postępowania kwalifikacyjnego oraz uzupełniającego postępowania kwalifikacyjnego, a także
sposób ustalania jego wyniku, jak również sposób wniesienia odwołania od wyniku oraz tryb i sposób rozpatrzenia
odwołania;
2) dokumenty, które należy dołączyć do zgłoszenia kandydata na członka Izby, potwierdzające spełnianie warunków,
o których mowa w art. 474 ust. 2 pkt 1–6 i 8–10 ustawy z dnia 11 września 2019 r. – Prawo zamówień publicznych,
oraz zakres danych, które ma zawierać to zgłoszenie;
3) szczegółowy zakres zagadnień, w oparciu o które przeprowadzane jest postępowanie kwalifikacyjne oraz uzupełniające
postępowanie kwalifikacyjne;
4) sposób powoływania komisji kwalifikacyjnej, szczegółowe wymagania wobec członków komisji kwalifikacyjnej oraz
organizację jej pracy."""

if __name__ == '__main__':
    output = process_text(text_to_process)

    for record in output:
        print(record)