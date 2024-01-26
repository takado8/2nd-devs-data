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
    # input_string = """
    #         Line 1
    #         Line 2 -123-
    #         Line 3
    #         Line 4 -45-
    #         Line 5
    #         """
    # Compile the provided pattern
    # pattern_page_nb = r'.*-(\d+)-.*\n'
    pattern_laws = r'®\s+ApexNet\. Wiedza, która chroni'
    compiled_pattern = re.compile(pattern_laws)

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


def remove_white_lines(text):
    import re
    # Your long multiline string
    input_string = """
    here is together
    This is some text.


    With multiple lines.


    And some extra white spaces.




    At the end.
    """

    # Keep one line of whitespace between non-empty lines
    output_string = re.sub('\n{2,}', '\n\n', input_string)

    print(output_string)


def law_articles_extractor():
    import re

    # Your multiline input string
    multiline_string = """
    Art. 1. This is the content between the first match.

    Art. 2. This is the content between the second match.

    Art. 3. This is the content between the third match.
    """
    # Modified regex pattern for extracting content including the match
    pattern = re.compile(r"(Art\. \d+\. .*?)(?=Art\. \d+\. |$)", re.DOTALL)

    # Using re.findall to extract content including the match
    matches = re.findall(pattern, multiline_string)

    # Print the extracted content
    for i, match in enumerate(matches, start=1):
        print(f"Match {i}: {match.strip()}")


def law_extractor(input_string):
    input_string = """
        Rozdział 1
        Title of Chapter 1
        Art. 1. Lorem ipsum dolor sit amet.

        Rozdział 2
        Title of Chapter 2
        Art. 2. Consectetur adipiscing elit.
        Art. 3. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
    chapter_pattern = re.compile(r'Rozdział\s+(\d+)')
    pattern = re.compile(r"(Art\. \d+\. .*?)(?=Art\. \d+\. |$)", re.DOTALL)
    # Using re.finditer to get match objects
    # # Using re.finditer to get match objects
    matches = [match for match in re.finditer(pattern, input_string)]

    # List to store chapter titles along with their indices
    chapter_titles = []

    # Find all chapter titles and their indices
    for chapter_match in chapter_pattern.finditer(input_string):
        chapter_start = chapter_match.start()
        chapter_end = input_string.find('\n', chapter_start)
        title = input_string[chapter_start:chapter_end]
        print(f'title: {title}')
        chapter_titles.append((chapter_start, title))
    chapter_titles = sorted(chapter_titles)
    print(chapter_titles)

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
            # # Print the extracted content
            print(f"Match {i}: {match.group().strip()}")
            print(f"Chapter Title: {title}")


def remove_footer_lines_pzp_law(text):
    pattern = r'®\s+ApexNet\. Wiedza, która chroni\n'
    regex = re.compile(pattern)
    # Remove the matched lines
    result = regex.sub('', text)
    return result


def split_longer_articles(articles):
    import re

    # Your multiline law article string
    law_article = """Art. 11. 1. Przepisów ustawy nie stosuje się do zamówień lub konkursów, których
przedmiotem:
1)   są usługi arbitrażowe lub pojednawcze;
2)   są usługi prawne:
     a)      zastępstwa procesowego wykonywanego przez adwokata, radcę prawnego lub
             prawnika zagranicznego w rozumieniu ustawy z dnia 5 lipca 2002 r. o
             świadczeniu          przez      prawników     zagranicznych   pomocy   prawnej   w
             Rzeczypospolitej Polskiej (Dz. U. z 2020 r. poz. 823), w postępowaniu
             arbitrażowym lub pojednawczym, lub przed sądami, trybunałami lub innymi
             organami publicznymi państwa członkowskiego Unii Europejskiej, państw
             trzecich lub przed międzynarodowymi sądami, trybunałami, instancjami
             arbitrażowymi lub pojednawczymi,
     b)      doradztwa prawnego wykonywanego przez adwokata, radcę prawnego lub
             prawnika zagranicznego w rozumieniu ustawy z dnia 5 lipca 2002 r. o
             świadczeniu          przez      prawników     zagranicznych   pomocy   prawnej   w
             Rzeczypospolitej Polskiej, w zakresie przygotowania postępowań, o których
             mowa w lit. a, lub gdy zachodzi wysokie prawdopodobieństwo, że sprawa,
             której dotyczy to doradztwo, stanie się przedmiotem tych postępowań,
     c)      notarialnego poświadczania i uwierzytelniania dokumentów,
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     d)      do świadczenia których wykonawcy są wyznaczani przez sąd lub trybunał
             danego państwa członkowskiego Unii Europejskiej, lub wyznaczani z mocy
             prawa w celu wykonania konkretnych zadań pod nadzorem takich trybunałów
             lub sądów,
     e)      związane z wykonywaniem władzy publicznej;
3)   są usługi badawcze lub rozwojowe, chyba że są one objęte kodami CPV od
     73000000-2 do 73120000-9, 73300000-5, 73420000-2 i 73430000-5, określonymi
     we Wspólnym Słowniku Zamówień, oraz spełnione są łącznie następujące warunki:
     a)      korzyści z tych usług przypadają wyłącznie zamawiającemu na potrzeby jego
             własnej działalności,
     b)      całość wynagrodzenia za świadczoną usługę wypłaca zamawiający;
4)   jest nabycie audycji i materiałów do audycji lub ich opracowanie, produkcja lub
     koprodukcja, jeżeli są przeznaczone na potrzeby świadczenia audiowizualnych
     usług medialnych lub radiowych usług medialnych – udzielanych przez dostawców
     audiowizualnych lub radiowych usług medialnych;
5)   jest zakup czasu antenowego lub audycji od dostawców audiowizualnych lub
     radiowych usług medialnych;
6)   jest nabycie własności lub innych praw do istniejących budynków lub
     nieruchomości;
7)   są usługi finansowe związane z emisją, sprzedażą, kupnem lub zbyciem papierów
     wartościowych lub innych instrumentów finansowych, w rozumieniu ustawy z dnia
     29 lipca 2005 r. o obrocie instrumentami finansowymi (Dz. U. z 2022 r. poz. 1500
     i 1488), oraz operacje przeprowadzane z Europejskim Instrumentem Stabilności
     Finansowej i Europejskim Mechanizmem Stabilności;
8)   są pożyczki lub kredyty, bez względu na to, czy wiążą się one z emisją, sprzedażą,
     kupnem lub zbyciem papierów wartościowych lub innych instrumentów
     finansowych w rozumieniu ustawy z dnia 29 lipca 2005 r. o obrocie instrumentami
     finansowymi, z wyjątkiem kredytów zaciąganych przez jednostki samorządu
     terytorialnego w ramach limitów zobowiązań określonych w uchwale budżetowej;
9)   są usługi w dziedzinie obrony cywilnej, ochrony ludności i zapobiegania
     niebezpieczeństwom, świadczone przez organizacje lub stowarzyszenia o
     ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




     charakterze niekomercyjnym i objęte kodami CPV 75250000-3, 75251000-0,
     75251100-1, 75251110-4, 75251120-7, 75252000-7, 75222000-8, 98113100-9
     oraz 85143000-3, określonymi we Wspólnym Słowniku Zamówień, z wyjątkiem
     usług transportu sanitarnego pacjentów;
10) są usługi publiczne w zakresie transportu pasażerskiego koleją lub metrem;
11) są dostawy uprawnień do emisji do powietrza gazów cieplarnianych i innych
     substancji, jednostek poświadczonej redukcji emisji oraz jednostek redukcji emisji,
     w rozumieniu przepisów o handlu uprawnieniami do emisji do powietrza gazów
     cieplarnianych i innych substancji.
     2. Przepisów ustawy nie stosuje się do umów:
1)   z zakresu prawa pracy;
2)   koncesji na roboty budowlane oraz koncesji na usługi w rozumieniu ustawy z dnia
     21 października 2016 r. o umowie koncesji na roboty budowlane lub usługi (Dz.
     U. z 2021 r. poz. 541), chyba że ustawa stanowi inaczej;
3)   o których mowa w art. 149 ust. 2 ustawy z dnia 20 lipca 2018 r. – Prawo o
     szkolnictwie wyższym i nauce (Dz. U. z 2022 r. poz. 574, z późn. zm.).
     3. Uchylony
     4. Przepisów ustawy nie stosuje się do zamówień dotyczących wytwarzania:
1)   blankietów dokumentów publicznych, o których mowa w art. 5 ust. 2 ustawy z dnia
     22 listopada 2018 r. o dokumentach publicznych (Dz. U. z 2022 r. poz. 1394 i 1415),
     oraz ich personalizacji lub indywidualizacji;
2)   znaków akcyzy;
3)   znaków legalizacyjnych, o których mowa w ustawie z dnia 20 czerwca 1997 r. –
     Prawo o ruchu drogowym (Dz. U. z 2022 r. poz. 988 i 1002);
4)   kart do głosowania i nakładek na karty do głosowania, o których mowa odpowiednio
     w art. 40 § 1 i art. 40a § 1 ustawy z dnia 5 stycznia 2011 r. – Kodeks wyborczy (Dz.
     U. z 2022 r. poz. 1277) oraz w art. 20 ustawy z dnia 14 marca 2003 r. o referendum
     ogólnokrajowym (Dz. U. z 2020 r. poz. 851);
5)   znaków holograficznych umieszczanych na zaświadczeniach o prawie do
     głosowania, o których mowa w art. 32 § 1 ustawy z dnia 5 stycznia 2011 r. – Kodeks
     wyborczy;
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




6)   układu mikroprocesorowego z oprogramowaniem służącym do zarządzania
     dokumentami publicznymi, systemów i baz informatycznych niezbędnych do
     zastosowania dokumentów publicznych, o których mowa w art. 5 ust. 2 ustawy z
     dnia 22 listopada 2018 r. o dokumentach publicznych, zawierających warstwę
     elektroniczną, zgodnie z ich przeznaczeniem.
     5. Przepisów ustawy nie stosuje się do zamówień o wartości mniejszej niż progi
unijne:
1)   których przedmiotem są dostawy lub usługi służące wyłącznie do celów prac
     badawczych, eksperymentalnych, naukowych lub rozwojowych, które nie służą
     prowadzeniu przez zamawiającego produkcji masowej służącej osiągnięciu
     rentowności rynkowej lub pokryciu kosztów badań lub rozwoju;
2)   których przedmiotem są dostawy lub usługi z zakresu działalności kulturalnej
     związanej z organizacją wystaw, koncertów, konkursów, festiwali, widowisk,
     spektakli teatralnych, przedsięwzięć z zakresu edukacji kulturalnej lub z
     gromadzeniem materiałów bibliotecznych przez biblioteki lub muzealiów, a także z
     zakresu działalności archiwalnej związanej            z gromadzeniem materiałów
     archiwalnych, jeżeli zamówienia te nie służą wyposażaniu zamawiającego w środki
     trwałe przeznaczone do bieżącej obsługi jego działalności;
3)   udzielanych przez inne niż określone w ust. 1 pkt 4 podmioty, których przedmiotem
     działalności jest produkcja i koprodukcja audycji i materiałów do audycji lub ich
     opracowanie, jeżeli zamówienia te są przeznaczone na potrzeby świadczenia
     audiowizualnych usług medialnych lub radiowych usług medialnych;
4)   których przedmiotem są dostawy lub usługi z zakresu działalności oświatowej
     związanej z gromadzeniem w bibliotekach szkolnych podręczników, materiałów
     edukacyjnych i materiałów ćwiczeniowych, o których mowa w ustawie z dnia 7
     września 1991 r. o systemie oświaty (Dz. U. z 2021 r. poz. 1915 oraz z 2022 r. poz.
     583 i 1116), jeżeli zamówienia te nie służą wyposażaniu zamawiającego w środki
     trwałe przeznaczone do bieżącej obsługi jego działalności;
5)   których przedmiotem są usługi lub roboty budowlane realizujące przedsięwzięcia
     rewitalizacyjne zawarte w gminnym programie rewitalizacji oraz wykonywane na
     obszarze Specjalnej Strefy Rewitalizacji, o których mowa odpowiednio w
     rozdziałach 4 i 5 ustawy z dnia 9 października 2015 r. o rewitalizacji (Dz. U. z 2021
     r. poz. 485), jeżeli zamówienia te udzielane są:
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     a)      przez gminę lub gminne jednostki organizacyjne organizacjom pozarządowym
             lub spółdzielniom socjalnym, a przedmiot zamówienia należy do działalności
             statutowej wykonawcy lub
     b)      w celu aktywizacji osób mających miejsce zamieszkania na obszarze
             Specjalnej Strefy Rewitalizacji, o której mowa w rozdziale 5 ustawy z dnia 9
             października 2015 r. o rewitalizacji;
6)   których przedmiotem są usługi z zakresu leśnictwa, objęte kodami CPV 77200000-
     2, 77210000-5, 77211000-2, 77211100-3, 77211200-4, 77211300-5, 77211400-6,
     77211500-7, 77211600-8, 77220000-8, 77230000-1, 77231000-8, 77231200-0,
     77231600-4 oraz 77231700-5 określonymi we Wspólnym Słowniku Zamówień;
7)   udzielanych w ramach realizacji współpracy rozwojowej przez jednostki wojskowe,
     określone na podstawie art. 5 ustawy z dnia 17 grudnia 1998 r. o zasadach użycia
     lub pobytu Sił Zbrojnych Rzeczypospolitej Polskiej poza granicami państwa (Dz.
     U. z 2021 r. poz. 396 oraz z 2022 r. poz. 655);
8)   udzielanych przez Ministra Sprawiedliwości – Prokuratora Generalnego albo
     jednostki organizacyjne mu podległe lub przez niego nadzorowane przywięziennym
     zakładom pracy, prowadzonym jako przedsiębiorstwa państwowe albo instytucje
     gospodarki budżetowej, związanych z zatrudnianiem osób pozbawionych wolności,
     jeżeli zasadnicza część działalności przywięziennego zakładu pracy dotyczy
     wykonywania zadań powierzonych mu przez Ministra Sprawiedliwości –
     Prokuratora Generalnego lub jednostki organizacyjne mu podległe lub przez niego
     nadzorowane, realizowanych samodzielnie lub przy udziale podwykonawców, pod
     warunkiem że co najmniej część zamówienia jest realizowana przez osoby
     pozbawione wolności;
9)   udzielanych przez zarządzającego specjalną strefą ekonomiczną, o którym mowa w
     ustawie z dnia 20 października 1994 r. o specjalnych strefach ekonomicznych (Dz.
     U. z 2020 r. poz. 1670 oraz z 2021 r. poz. 2105), będącego podmiotem, o którym
     mowa w art. 4 pkt 3;
10) związanych z procesem wypłat środków gwarantowanych, o których mowa w art. 2
     pkt 65 ustawy z dnia 10 czerwca 2016 r. o Bankowym Funduszu Gwarancyjnym,
     systemie gwarantowania depozytów oraz przymusowej restrukturyzacji (Dz. U. z
     2022 r. poz. 793 i 872), w szczególności usług świadczonych przez podmiot, z
     którym zostanie zawarta umowa o dokonanie wypłat środków gwarantowanych;
     ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




11) związanych z przymusową restrukturyzacją albo umorzeniem lub konwersją
    instrumentów kapitałowych lub zobowiązań kwalifikowalnych, o których mowa w
    art. 101 ust. 7 ustawy z dnia 10 czerwca 2016 r. o Bankowym Funduszu
    Gwarancyjnym,              systemie        gwarantowania   depozytów   oraz   przymusowej
    restrukturyzacji, lub związanych z podejmowaniem działań i wykonywaniem
    uprawnień na podstawie rozporządzenia Parlamentu Europejskiego i Rady (UE)
    2021/23 z dnia 16 grudnia 2020 r. w sprawie ram na potrzeby prowadzenia działań
    naprawczych oraz restrukturyzacji i uporządkowanej likwidacji w odniesieniu do
    kontrahentów centralnych oraz zmieniającego rozporządzenia (UE) nr 1095/2010,
    (UE) nr 648/2012, (UE) nr 600/2014, (UE) nr 806/2014 i (UE) 2015/2365 oraz
    dyrektywy 2002/47/WE, 2004/25/WE, 2007/36/WE, 2014/59/UE i (UE) 2017/1132
    (Dz. Urz. UE L 22 z 22.01.2021, str. 1), zwanego dalej „rozporządzeniem nr
    2021/23”, których przedmiotem jest:
    a)      przeprowadzenie oszacowania, o którym mowa w art. 137 ust. 1 oraz art. 241
            ust. 1 ustawy z dnia 10 czerwca 2016 r. o Bankowym Funduszu
            Gwarancyjnym, systemie gwarantowania depozytów oraz przymusowej
            restrukturyzacji,
    aa) przeprowadzenie wyceny, o której mowa w art. 24 ust. 1 rozporządzenia nr
            2021/23,
    b) świadczenie usług doradztwa, w tym doradztwa strategicznego, ekonomiczno-
    finansowego, podatkowego, prawnego i informatycznego,
    c) [uchylony]
12) [uchylony];
13) związanych z zastosowaniem rządowych instrumentów stabilizacji finansowej, o
    których mowa w ustawie z dnia 12 lutego 2010 r. o rekapitalizacji niektórych
    instytucji oraz o rządowych instrumentach stabilizacji finansowej (Dz. U. z 2022 r.
    poz. 396), w szczególności zamówień, których przedmiotem jest:
    a) dokonanie aktualizacji oszacowania, o którym mowa w art. 19f ust. 8 tej ustawy,
    b) świadczenie usług doradztwa, w tym doradztwa strategicznego, ekonomiczno-
    finansowego, podatkowego, prawnego i informatycznego,
    c) powierzenie podmiotowi trzeciemu zarządzania prawami, o których mowa w art.
    19b ust. 1 tej ustawy;
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




14) na usługi Banku Gospodarstwa Krajowego, w zakresie zlecenia przez:
     a) ministra właściwego do spraw finansów publicznych spraw i czynności
     związanych z udzieleniem wsparcia, o którym mowa w art. 3 ust. 1 ustawy z
     dnia 12 lutego 2009 r. o udzielaniu przez Skarb Państwa wsparcia instytucjom
     finansowym (Dz. U. z 2022 r. poz. 618), lub udzieleniem gwarancji spłaty kredytu
     refinansowego, o której mowa w art. 4 ust. 1 tej ustawy, w tym związanych z
     zabezpieczeniem lub obsługą udzielonego wsparcia lub udzielonej gwarancji,
     b) Narodowy Bank Polski spraw i czynności związanych z udzieleniem
     kredytów, o których mowa w art. 42 i art. 43 ustawy z dnia 29 sierpnia 1997 r. o
     Narodowym Banku Polskim (Dz. U. z 2022 r. poz. 492 i 655), w tym związanych z
     zabezpieczeniem lub obsługą tych kredytów.”.
     6. Do zasadniczej części działalności przywięziennego zakładu pracy, o której
mowa w ust. 5 pkt 8, wlicza się działalność związaną z realizacją zamówień w związku
ze społeczną i zawodową integracją osób, o których mowa w art. 94 ust. 1 pkt 5;"""

    # Define the pattern for finding points
    pattern = re.compile(r'\d+\)\s')

    # Split the law article using the pattern
    points = re.split(pattern, law_article)
    # i = 0
    title = points.pop(0)
    # for point in points:
    #     i += 1
    #     print(f'part {i}: {point.strip()}')
    return title, points


if __name__ == '__main__':
    split_longer_articles('')
