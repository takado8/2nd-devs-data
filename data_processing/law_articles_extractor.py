import json
import re
import tiktoken

MAX_TOKENS = 1500


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
    with open(output_path, 'w+') as f:
        json.dump(articles, f)
    print(f'saved to file: {output_path}')


text = """®   ApexNet. Wiedza, która chroni | www.apexnet.pl




                                                      U S T AWA

                                             z dnia 11 września 2019 r.

                                        Prawo zamówień publicznych1)


                                                         DZIAŁ I

                                                   Przepisy ogólne

                                                        Rozdział 1

                                                 Przedmiot regulacji

                                                        Oddział 1

                                    Zakres spraw regulowanych ustawą

         Art. 1. Ustawa reguluje zamówienia publiczne, zwane dalej „zamówieniami”, oraz
konkursy, w tym określa:
1)       podmioty obowiązane do stosowania przepisów ustawy;
2)       zakres wyłączeń stosowania przepisów ustawy;
3)       zasady udzielania zamówień;
4)       etapy przygotowania i prowadzenia postępowania o udzielenie zamówienia;
5)       tryby udzielania zamówień oraz szczególne instrumenty i procedury w zakresie
         zamówień;

1)
     Niniejsza ustawa wdraża:

1) dyrektywę Parlamentu Europejskiego i Rady 2014/24/UE z dnia 26 lutego 2014 r. w sprawie zamówień
   publicznych, uchylającą dyrektywę 2004/18/WE (Dz. Urz. UE L 94 z 28.03.2014, str. 65, z późn. zm.);
2) dyrektywę Parlamentu Europejskiego i Rady 2014/25/UE z dnia 26 lutego 2014 r. w sprawie udzielania
   zamówień przez podmioty działające w sektorach gospodarki wodnej, energetyki, transportu i usług
   pocztowych, uchylającą dyrektywę 2004/17/WE (Dz. Urz. UE L 94 z 28.03.2014, str. 243, z późn. zm.);
3) dyrektywę Parlamentu Europejskiego i Rady 2009/81/WE z dnia 13 lipca 2009 r. w sprawie koordynacji
   procedur udzielania niektórych zamówień na roboty budowlane, dostawy i usługi przez instytucje lub
   podmioty zamawiające w dziedzinach obronności i bezpieczeństwa i zmieniającą dyrektywy
   2004/17/WE i 2004/18/WE (Dz. Urz. UE L 216 z 20.08.2009, str. 76, z późn. zm.);
4) dyrektywę Rady 89/665/EWG z dnia 21 grudnia 1989 r. w sprawie koordynacji przepisów ustawowych,
   wykonawczych i administracyjnych odnoszących się do stosowania procedur odwoławczych w zakresie
   udzielania zamówień publicznych na dostawy i roboty budowlane (Dz. Urz. WE L 395 z 30.12.1989,
   str. 33, z późn. zm.; Dz. Urz. UE Polskie wydanie specjalne, rozdz. 6, t. 1, str. 246);
5) dyrektywę Rady 92/13/EWG z dnia 25 lutego 1992 r. koordynującą przepisy ustawowe, wykonawcze i
   administracyjne odnoszące się do stosowania przepisów wspólnotowych w procedurach zamówień
   publicznych podmiotów działających w sektorach gospodarki wodnej, energetyki, transportu i
   telekomunikacji (Dz. Urz. WE L 76 z 23.03.1992, str. 14, z późn. zm.; Dz. Urz. UE Polskie wydanie
   specjalne, rozdz. 6, t. 1, str. 315).
        ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




6)     wymagania dotyczące umów w sprawie zamówienia publicznego oraz umów
       ramowych;
7)     organy właściwe w sprawach zamówień;
8)     środki ochrony prawnej;
9)     pozasądowe rozwiązywanie sporów dotyczących realizacji umów w sprawie
       zamówienia publicznego;
10) kontrolę udzielania zamówień oraz kary pieniężne.

       Art. 2. 1. Przepisy ustawy stosuje się do udzielania:
1)     zamówień klasycznych oraz organizowania konkursów, których wartość jest równa
       lub przekracza kwotę 130 000 złotych, przez zamawiających publicznych;
2)     zamówień sektorowych oraz organizowania konkursów, których wartość jest równa
       lub przekracza progi unijne, przez zamawiających sektorowych;
3)     zamówień w dziedzinach obronności i bezpieczeństwa, których wartość jest równa
       lub przekracza progi unijne, przez zamawiających publicznych oraz zamawiających
       sektorowych;
4)     zamówień klasycznych oraz organizowania konkursów, których wartość jest równa
       lub      przekracza         progi     unijne,         przez   zamawiających   subsydiowanych   w
       okolicznościach, o których mowa w art. 6.
       2. [Uchylony]

       Art. 3. 1. Przez progi unijne należy rozumieć kwoty wartości zamówień lub
konkursów określone w:
1)     art. 4 i art. 13 dyrektywy Parlamentu Europejskiego i Rady 2014/24/UE z dnia 26
       lutego 2014 r. w sprawie zamówień publicznych, uchylającej dyrektywę
       2004/18/WE (Dz. Urz. UE L 94 z 28.03.2014, str. 65, z późn. zm.2)), zwanej dalej
       „dyrektywą 2014/24/UE”,
2)     art. 15 dyrektywy Parlamentu Europejskiego i Rady 2014/25/UE z dnia 26 lutego
       2014 r. w sprawie udzielania zamówień przez podmioty działające w sektorach




2)
     Zmiany wymienionej dyrektywy zostały ogłoszone w Dz. Urz. UE L 307 z 25.11.2015, str. 5; Dz. Urz.
     UE L 24 z 30.01.2016, str. 14 oraz Dz. Urz. UE L 337 z 19.12.2017, str. 19.
      ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




      gospodarki wodnej, energetyki, transportu i usług pocztowych, uchylającej
      dyrektywę 2004/17/WE (Dz. Urz. UE L 94 z 28.03.2014, str. 243, z późn. zm.3)),
      zwanej dalej „dyrektywą 2014/25/UE”,
3)    art. 8 dyrektywy 2009/81/WE Parlamentu Europejskiego i Rady z dnia 13 lipca 2009
      r. w sprawie koordynacji procedur udzielania niektórych zamówień na roboty
      budowlane, dostawy i usługi przez instytucje lub podmioty zamawiające w
      dziedzinach obronności i bezpieczeństwa i zmieniającej dyrektywy 2004/17/WE i
      2004/18/WE (Dz. Urz. UE L 216 z 20.08.2009, str. 76, z późn. zm.4)), zwanej dalej
      „dyrektywą 2009/81/WE”
– aktualizowane w aktach wykonawczych Komisji Europejskiej, wydawanych
odpowiednio na podstawie art. 6 ust. 5 dyrektywy 2014/24/UE, art. 17 ust. 4 dyrektywy
2014/25/UE i art. 68 dyrektywy 2009/81/WE.
      2. Prezes Urzędu Zamówień Publicznych, zwany dalej „Prezesem Urzędu”
informuje o:
1)    aktualnych progach unijnych, ich równowartości w złotych oraz o równowartości w
      złotych kwot wyrażonych w ustawie w euro, ustalonych zgodnie z komunikatem
      Komisji Europejskiej, wydanym odpowiednio na podstawie:
      a)      art. 6 ust. 3 dyrektywy 2014/24/UE,
      b)      art. 17 ust. 2 dyrektywy 2014/25/UE,
      c)      art. 68 ust. 2 i 3 dyrektywy 2009/81/WE,
2)    średnim kursie złotego w stosunku do euro, stanowiącym podstawę przeliczania
      wartości zamówień lub konkursów, ustalonym na podstawie kwot określonych w
      komunikacie Komisji Europejskiej, o którym mowa w pkt 1
– mających zastosowanie do postępowań o udzielenie zamówienia i konkursów
wszczętych od dnia wejścia w życie aktów wykonawczych Komisji Europejskiej,
wydawanych odpowiednio na podstawie art. 6 ust. 5 dyrektywy 2014/24/UE, art. 17 ust.
4 dyrektywy 2014/25/UE i art. 68 dyrektywy 2009/81/WE.
      3. Informacje, o których mowa w ust. 2, są ogłaszane w drodze obwieszczenia, w
Dzienniku Urzędowym Rzeczypospolitej Polskiej „Monitor Polski”, oraz zamieszczane
na stronie internetowej Urzędu Zamówień Publicznych, zwanego dalej „Urzędem”,

3) Zmiany wymienionej dyrektywy zostały ogłoszone w Dz. Urz. UE L 307 z 25.11.2015, str. 7 oraz Dz.
   Urz. UE L 337 z 19.12.2017, str. 17.
4) Zmiany wymienionej dyrektywy zostały ogłoszone w Dz. Urz. UE L 314 z 01.12.2009, str. 64; Dz.
   Urz. UE L 319 z 02.12.2011, str. 43; Dz. Urz. UE L 158 z 10.06.2013, str. 184; Dz. Urz. UE L 335 z
   14.12.2013, str. 17; Dz. Urz. UE L 330 z 16.12.2015, str. 14 oraz Dz. Urz. UE L 337 z 19.12.2017,
   str. 22.
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




niezwłocznie po publikacji komunikatu Komisji Europejskiej, o którym mowa w ust. 2,
w Dzienniku Urzędowym Unii Europejskiej.
     4. Do przeliczania kwot wartości zamówień wyrażonych w ustawie w euro stosuje
się średni kurs złotego w stosunku do euro, o którym mowa w ust. 2 pkt 2.

     Art. 4. Przepisy ustawy stosuje się do zamawiających publicznych, którymi są:
1)   jednostki sektora finansów publicznych w rozumieniu przepisów ustawy z dnia 27
     sierpnia 2009 r. o finansach publicznych (Dz. U. z 2021 r. poz. 305);
2)   inne, niż określone w pkt 1, państwowe jednostki organizacyjne nieposiadające
     osobowości prawnej;
3)   inne, niż określone w pkt 1, osoby prawne, utworzone w szczególnym celu
     zaspokajania potrzeb o charakterze powszechnym, niemających charakteru
     przemysłowego ani handlowego, jeżeli podmioty, o których mowa w tym przepisie
     oraz w pkt 1 i 2, pojedynczo lub wspólnie, bezpośrednio lub pośrednio przez inny
     podmiot:
     a)      finansują je w ponad 50% lub
     b)      posiadają ponad połowę udziałów albo akcji, lub
     c)      sprawują nadzór nad organem zarządzającym, lub
     d)      mają prawo do powoływania ponad połowy składu organu nadzorczego lub
             zarządzającego;
4)   związki podmiotów, o których mowa w pkt 1 lub 2, lub podmiotów, o których mowa
     w pkt 3.

     Art. 5. 1. Przepisy ustawy stosuje się do zamawiających sektorowych, którymi są:
1)   zamawiający publiczni w zakresie, w jakim wykonują jeden z rodzajów działalności
     sektorowej, o której mowa w ust. 4;
2)   inne, niż określone w pkt 1, podmioty, które wykonują jeden z rodzajów działalności
     sektorowej, o której mowa w ust. 4, oraz na których zamawiający publiczni,
     pojedynczo lub wspólnie, bezpośrednio lub pośrednio przez inny podmiot
     wywierają dominujący wpływ, w szczególności:
     a)      posiadają ponad połowę udziałów albo akcji lub
     b)      posiadają ponad połowę głosów wynikających z udziałów albo akcji, lub
     c)      mają prawo do powoływania ponad połowy składu organu nadzorczego lub
             zarządzającego;
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




3)   inne, niż określone w pkt 1 i 2, podmioty, które wykonują jeden z rodzajów
     działalności sektorowej, o której mowa w ust. 4, jeżeli działalność ta jest
     wykonywana na podstawie praw szczególnych lub wyłącznych.
     2. Prawami szczególnymi lub wyłącznymi w rozumieniu ust. 1 pkt 3 są prawa
przyznane w drodze ustawy lub decyzji administracyjnej, polegające na zastrzeżeniu
wykonywania określonej działalności dla jednego lub większej liczby podmiotów,
wywierające istotny wpływ na możliwość wykonywania tej działalności przez inne
podmioty, z wyłączeniem praw przyznanych w drodze ogłoszonego publicznie
postępowania na podstawie obiektywnych i niedyskryminujących kryteriów, w
szczególności postępowania:
1)   obejmującego ogłoszenie o zamówieniu lub wszczęcie postępowania o udzielenie
     koncesji na roboty budowlane lub usługi;
2)   prowadzonego na podstawie przepisów ogłoszonych w obwieszczeniu Prezesa
     Urzędu, o którym mowa w ust. 3.
     3. Prezes Urzędu ogłasza, w drodze obwieszczenia, w Dzienniku Urzędowym
Rzeczypospolitej Polskiej „Monitor Polski”, oraz zamieszcza na stronie internetowej
Urzędu, wykaz aktów prawnych wdrażających przepisy określone w załączniku II do
dyrektywy 2014/25/UE.
     4. Działalnością sektorową w zakresie:
1)   gospodarki wodnej jest:
     a)      udostępnianie lub obsługa stałych sieci przeznaczonych do świadczenia usług
             publicznych w związku z produkcją, transportem lub dystrybucją wody pitnej,
     b)      dostarczanie wody pitnej do sieci, o których mowa w lit. a, chyba że:
             –     produkcja wody pitnej przez zamawiającego sektorowego, o którym mowa
                   w ust. 1 pkt 2 i 3, jest niezbędna do prowadzenia działalności innej niż
                   określona w pkt 1–4, oraz
             –     dostarczanie wody pitnej do sieci uzależnione jest wyłącznie od własnego
                   zużycia zamawiającego i w okresie ostatnich 3 lat łącznie z rokiem, w
                   którym udziela się zamówienia, nie przekracza 30% wielkości jego łącznej
                   produkcji,
     c)      związane z działalnością, o której mowa w lit. a i b, działania w zakresie:
             –     projektów dotyczących inżynierii wodnej, nawadniania lub melioracji, pod
                   warunkiem że ilość wody wykorzystywanej do celów dostaw wody
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




                   pitnej stanowi ponad 20% łącznej ilości wody dostępnej dzięki tym
                   projektom lub instalacjom nawadniającym lub melioracyjnym,
             –     odprowadzania lub oczyszczania ścieków;
2)   energii elektrycznej jest:
     a)      udostępnianie lub obsługa stałych sieci przeznaczonych do świadczenia usług
             publicznych w związku z produkcją, przesyłaniem lub dystrybucją energii
             elektrycznej,
     b)      dostarczanie energii elektrycznej do sieci, o których mowa w lit. a, chyba że:
             –     produkcja energii elektrycznej przez zamawiającego sektorowego, o
                   którym mowa w ust. 1 pkt 2 i 3, jest niezbędna do prowadzenia działalności
                   innej niż określona w pkt 1–4, oraz
             –     dostarczanie energii elektrycznej do sieci uzależnione jest wyłącznie od
                   własnego zużycia zamawiającego i w okresie ostatnich 3 lat łącznie z
                   rokiem, w którym udziela się zamówienia, nie przekracza 30% łącznej
                   produkcji energii elektrycznej;
3)   gazu i energii cieplnej jest:
     a)      udostępnianie lub obsługa stałych sieci przeznaczonych do świadczenia usług
             publicznych w związku z produkcją, transportem lub dystrybucją gazu lub
             energii cieplnej,
     b)      dostarczanie gazu lub energii cieplnej do sieci, o których mowa w lit. a, chyba
             że:
             –     produkcja gazu lub energii cieplnej przez zamawiającego sektorowego, o
                   którym mowa w ust. 1 pkt 2 i 3, stanowi nieuniknioną konsekwencję
                   prowadzenia działalności innej niż określona w pkt 1–4, oraz
             –     dostarczanie gazu lub energii cieplnej do sieci ma na celu wyłącznie
                   ekonomiczne wykorzystanie produkcji i w okresie ostatnich 3 lat, łącznie
                   z rokiem, w którym udziela się zamówienia, nie przekracza 20%
                   przeciętnych przychodów zamawiającego;
4)   usług transportowych jest działalność polegająca na udostępnianiu lub obsłudze
     sieci przeznaczonych do świadczenia usług publicznych w zakresie transportu
     kolejowego, tramwajowego, trolejbusowego, autobusowego, koleją linową lub przy
     użyciu systemów automatycznych;
5)   portów, przystani i portów lotniczych jest działalność związana z eksploatacją
     obszaru geograficznego, w celu udostępniania przewoźnikom lotniczym,
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     przewoźnikom morskim oraz przewoźnikom śródlądowym odpowiednio portów
     lotniczych, portów morskich i portów śródlądowych, lub innych terminali;
6)   usług pocztowych jest działalność polegająca na świadczeniu usług:
     a)      przyjmowania, sortowania, przemieszczania lub doręczania przesyłek
             pocztowych,
     b)      zarządzania usługami, o których mowa w lit. a, oraz świadczeniu usług
             dotyczących przesyłek nieuwzględnionych w lit. a, takich jak druki
             bezadresowe, o ile te usługi są świadczone przez podmiot świadczący usługi,
             o których mowa w lit. a;
7)   wydobycia paliw jest działalność polegająca na wydobyciu ropy naftowej lub gazu
     i ich naturalnych pochodnych oraz poszukiwaniu lub wydobyciu węgla brunatnego,
     węgla kamiennego lub innych paliw stałych.
     5. Przez dostarczanie i dystrybucję, o których mowa w ust. 4 pkt 1–3, należy
rozumieć również produkcję, sprzedaż hurtową i detaliczną.

     Art. 6. Przepisy ustawy stosuje się do zamawiających subsydiowanych, którymi są
zamawiający inni niż zamawiający publiczni lub zamawiający sektorowi, jeżeli zachodzą
łącznie następujące okoliczności:
1)   ponad 50% wartości udzielanego przez ten podmiot zamówienia jest finansowane
     ze środków publicznych lub zamawiających, o których mowa w art. 4 i art. 5 ust. 1
     pkt 1;
2)   wartość zamówienia jest równa lub przekracza progi unijne;
3)   przedmiotem zamówienia są roboty budowlane w zakresie inżynierii lądowej lub
     wodnej określone w załączniku II do dyrektywy 2014/24/UE, budowy szpitali,
     obiektów sportowych, rekreacyjnych lub wypoczynkowych, budynków szkolnych,
     budynków szkół wyższych lub budynków wykorzystywanych przez administrację
     publiczną lub usługi związane z takimi robotami budowlanymi.

     Art. 7. Ilekroć w niniejszej ustawie jest mowa o:
1)   cenie – należy przez to rozumieć cenę w rozumieniu art. 3 ust. 1 pkt 1 i ust. 2 ustawy
     z dnia 9 maja 2014 r. o informowaniu o cenach towarów i usług (Dz. U. z 2019 r.
     poz. 178), nawet jeżeli jest płacona na rzecz osoby niebędącej przedsiębiorcą;
2)   cyklu życia – należy przez to rozumieć wszelkie możliwe kolejne lub powiązane
     fazy istnienia przedmiotu dostawy, usługi lub roboty budowlanej, w szczególności
     ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




     badanie, rozwój, projektowanie przemysłowe, testowanie, produkcję, transport,
     używanie, naprawę, modernizację, zmianę, utrzymanie przez okres istnienia,
     logistykę, szkolenie, zużycie, wyburzenie, wycofanie i usuwanie;
3)   dokumentach zamówienia – należy przez to rozumieć dokumenty sporządzone
     przez zamawiającego lub dokumenty, do których zamawiający odwołuje się, inne
     niż ogłoszenie, służące do określenia lub opisania warunków zamówienia, w tym
     specyfikacja warunków zamówienia oraz opis potrzeb i wymagań;
4)   dostawach – należy przez to rozumieć nabywanie produktów, którymi są rzeczy
     ruchome, energia, woda oraz prawa majątkowe, jeżeli mogą być przedmiotem
     obrotu, w szczególności na podstawie umowy sprzedaży, dostawy, najmu,
     dzierżawy oraz leasingu z opcją lub bez opcji zakupu, które może obejmować
     dodatkowo rozmieszczenie lub instalację;
5)   dynamicznym systemie zakupów – należy przez to rozumieć ograniczony w czasie
     elektroniczny proces udzielania zamówień, których przedmiotem są ogólnie
     dostępne usługi, dostawy lub roboty budowlane;
6)   innowacji – należy przez to rozumieć wdrażanie nowego lub znacznie
     udoskonalonego produktu, usługi lub procesu, w tym między innymi procesów
     produkcji, budowy lub konstrukcji, nowej metody marketingowej lub nowej metody
     organizacyjnej w działalności gospodarczej, organizowaniu pracy lub relacjach
     zewnętrznych;
7)   kierowniku zamawiającego – należy przez to rozumieć osobę lub organ, który
     zgodnie z obowiązującymi przepisami, statutem lub umową, jest uprawniony do
     zarządzania zamawiającym, z wyłączeniem pełnomocników ustanowionych przez
     zamawiającego;
8)   konkursie – należy przez to rozumieć przyrzeczenie publiczne, w którym
     zamawiający, przez publiczne ogłoszenie, przyrzeka nagrodę za wykonanie i
     przeniesienie prawa do pracy konkursowej wybranej przez sąd konkursowy;
9)   kryteriach selekcji – należy przez to rozumieć obiektywne i niedyskryminacyjne
     kryteria stosowane przez zamawiającego w postępowaniu o udzielenie zamówienia
     albo w konkursie, w celu ograniczenia liczby wykonawców albo uczestników
     konkursu, niepodlegających wykluczeniu i spełniających warunki udziału w
     postępowaniu albo w konkursie, których zamawiający zaprosi do złożenia ofert
     wstępnych lub ofert, do negocjacji lub dialogu albo do złożenia prac konkursowych;
      ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




10)   łańcuchu dostaw – należy przez to rozumieć wszystkie zasoby i działania niezbędne
      do wykonania dostaw, usług i robót budowlanych, które są przedmiotem
      zamówienia;
11)   newralgicznych robotach budowlanych – należy przez to rozumieć roboty
      budowlane przeznaczone do celów bezpieczeństwa, które wiążą się z korzystaniem
      z informacji niejawnych lub informacji podlegających ochronie ze względów
      bezpieczeństwa, wymagają ich wykorzystania lub je zawierają;
12)   newralgicznym sprzęcie – należy przez to rozumieć sprzęt przeznaczony do celów
      bezpieczeństwa, który wiąże się z korzystaniem z informacji niejawnych lub
      informacji podlegających ochronie ze względów bezpieczeństwa, wymaga ich
      wykorzystania lub je zawiera;
13)   newralgicznych usługach – należy przez to rozumieć usługi przeznaczone do celów
      bezpieczeństwa, które wiążą się z korzystaniem z informacji niejawnych lub
      informacji podlegających ochronie ze względów bezpieczeństwa, wymagają ich
      wykorzystania lub je zawierają;
14)   obiekcie budowlanym – należy przez to rozumieć wynik całości robót budowlanych
      w zakresie budownictwa lub inżynierii lądowej i wodnej, który może samoistnie
      spełniać funkcję gospodarczą lub techniczną;
15)   ofercie częściowej – należy przez to rozumieć ofertę przewidującą, zgodnie z
      dokumentami zamówienia, wykonanie części zamówienia;
16)   pisemności – należy przez to rozumieć sposób wyrażenia informacji przy użyciu
      wyrazów, cyfr lub innych znaków pisarskich, które można odczytać i powielić, w
      tym przekazywanych przy użyciu środków komunikacji elektronicznej;
17)   podmiotowych środkach dowodowych – należy przez to rozumieć środki służące
      potwierdzeniu braku podstaw wykluczenia, spełniania warunków udziału w
      postępowaniu lub kryteriów selekcji, z wyjątkiem oświadczenia, o którym mowa w
      art. 125 ust. 1;
18)   postępowaniu o udzielenie zamówienia – należy przez to rozumieć postępowanie
      wszczynane przez przekazanie albo zamieszczenie ogłoszenia, przekazanie
      zaproszenia do negocjacji albo zaproszenia do składania ofert, prowadzone jako
      uporządkowany ciąg czynności, których podstawą są warunki zamówienia ustalone
      przez zamawiającego, prowadzące do wyboru najkorzystniejszej oferty lub
      wynegocjowania postanowień umowy w sprawie zamówienia publicznego,
      kończące się zawarciem umowy w sprawie zamówienia publicznego albo jego
         ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




        unieważnieniem, z tym, że zawarcie umowy w sprawie zamówienia publicznego
        nie stanowi czynności w tym postępowaniu;
19)     protokole postępowania – należy przez to rozumieć dokument sporządzany przez
        zamawiającego, który potwierdza przebieg postępowania o udzielenie zamówienia;
20)     przedmiotowych środkach dowodowych – należy przez to rozumieć środki służące
        potwierdzeniu zgodności oferowanych dostaw, usług lub robót budowlanych z
        wymaganiami, cechami lub kryteriami określonymi w opisie przedmiotu
        zamówienia lub opisie kryteriów oceny ofert, lub wymaganiami związanymi z
        realizacją zamówienia;
21)     robotach budowlanych – należy przez to rozumieć wykonanie albo zaprojektowanie
        i wykonanie robót budowlanych, określonych w załączniku II do dyrektywy
        2014/24/UE, w załączniku I do dyrektywy 2014/25/UE oraz objętych działem 45
        załącznika I do rozporządzenia (WE) nr 2195/2002 Parlamentu Europejskiego i
        Rady z dnia 5 listopada 2002 r. w sprawie Wspólnego Słownika Zamówień (CPV)
        (Dz. Urz. WE L 340 z 16.12.2002, str. 1, z późn. zm.5)), zwanego dalej „Wspólnym
        Słownikiem Zamówień”, lub obiektu budowlanego, a także realizację obiektu
        budowlanego za pomocą dowolnych środków, zgodnie z wymaganiami
        określonymi przez zamawiającego;
22)     sprzęcie wojskowym – należy przez to rozumieć wyposażenie specjalnie
        zaprojektowane lub zaadaptowane do potrzeb wojskowych i przeznaczone do
        użycia jako broń, amunicja lub materiały wojenne;
23)     środkach komunikacji elektronicznej – należy przez to rozumieć środki komunikacji
        elektronicznej w rozumieniu ustawy z dnia 18 lipca 2002 r. o świadczeniu usług
        drogą elektroniczną (Dz. U. z 2020 r. poz. 344);
24)     środkach publicznych – należy przez to rozumieć środki publiczne w rozumieniu
        przepisów ustawy z dnia 27 sierpnia 2009 r. o finansach publicznych;
25)     udzieleniu zamówienia – należy przez to rozumieć zawarcie umowy w sprawie
        zamówienia publicznego;
26)     umowie ramowej – należy przez to rozumieć umowę zawartą między
        zamawiającym a jednym lub większą liczbą wykonawców, której celem jest
        ustalenie warunków dotyczących zamówień, jakie mogą zostać udzielone w

5)
     Zmiany wymienionego rozporządzenia zostały ogłoszone w Dz. Urz. UE L 329 z 17.12.2003, str. 1;
      Dz. Urz. UE L 74 z 15.03.2008, str. 1; Dz. Urz. UE L 188 z 18.07.2009, str. 14.
      ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




      danym okresie, w szczególności cen i, jeżeli zachodzi taka potrzeba,
      przewidywanych ilości;
27)   umowie o podwykonawstwo – należy przez to rozumieć umowę w formie pisemnej
      o charakterze odpłatnym, zawartą między wykonawcą a podwykonawcą, a w
      przypadku zamówienia na roboty budowlane innego niż zamówienie w dziedzinach
      obronności i bezpieczeństwa, także między podwykonawcą a dalszym
      podwykonawcą lub między dalszymi podwykonawcami, na mocy której
      odpowiednio podwykonawca lub dalszy podwykonawca, zobowiązuje się wykonać
      część zamówienia;
28)   usługach – należy przez to rozumieć wszelkie świadczenia, które nie są robotami
      budowlanymi lub dostawami;
29)   warunkach zamówienia – należy przez to rozumieć warunki, które dotyczą
      zamówienia lub postępowania o udzielenie zamówienia, wynikające w
      szczególności z opisu przedmiotu zamówienia, wymagań związanych z realizacją
      zamówienia, kryteriów oceny ofert, wymagań proceduralnych lub projektowanych
      postanowień umowy w sprawie zamówienia publicznego;
30)   wykonawcy – należy przez to rozumieć osobę fizyczną, osobę prawną albo
      jednostkę organizacyjną nieposiadającą osobowości prawnej, która oferuje na rynku
      wykonanie robót budowlanych lub obiektu budowlanego, dostawę produktów lub
      świadczenie usług lub ubiega się o udzielenie zamówienia, złożyła ofertę lub
      zawarła umowę w sprawie zamówienia publicznego;
31)   zamawiającym – należy przez to rozumieć osobę fizyczną, osobę prawną albo
      jednostkę organizacyjną nieposiadającą osobowości prawnej, obowiązaną na
      podstawie ustawy do jej stosowania;
32)   zamówieniu – należy przez to rozumieć umowę odpłatną zawieraną między
      zamawiającym             a    wykonawcą,             której   przedmiotem   jest   nabycie   przez
      zamawiającego od wybranego wykonawcy robót budowlanych, dostaw lub usług;
33)   zamówieniu klasycznym – należy przez to rozumieć zamówienie udzielane przez
      zamawiającego publicznego oraz zamawiającego subsydiowanego inne niż
      zamówienie sektorowe i zamówienie w dziedzinach obronności i bezpieczeństwa;
34)   zamówieniu na usługi społeczne i inne szczególne usługi – należy przez to rozumieć
      zamówienia klasyczne lub zamówienia sektorowe, na usługi wymienione
      odpowiednio w załączniku XIV do dyrektywy 2014/24/UE oraz załączniku XVII
      do dyrektywy 2014/25/UE;
      ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




35)   zamówieniu sektorowym – należy przez to rozumieć zamówienie udzielane przez
      zamawiającego sektorowego w celu prowadzenia jednego z rodzajów działalności
      sektorowej, o której mowa w art. 5 ust. 4;
36)   zamówieniu w dziedzinach obronności i bezpieczeństwa – należy przez to rozumieć
      zamówienie udzielane przez zamawiającego publicznego lub zamawiającego
      sektorowego, którego przedmiotem są:
      a)      dostawy sprzętu wojskowego, w tym wszelkich jego części, komponentów,
              podzespołów lub jego oprogramowania,
      b)      dostawy newralgicznego sprzętu, w tym wszelkich jego części, komponentów,
              podzespołów lub jego oprogramowania,
      c)      roboty budowlane, dostawy i usługi związane z zabezpieczeniem obiektów
              będących w dyspozycji podmiotów realizujących zamówienia w dziedzinach
              obronności i bezpieczeństwa lub związane ze sprzętem, o którym mowa w lit.
              a i b, i wszystkich jego części, komponentów i podzespołów związanych z
              cyklem życia tego produktu lub usługi,
      d)      roboty budowlane i usługi przeznaczone wyłącznie do celów wojskowych,
              newralgiczne roboty budowlane lub newralgiczne usługi.

      Art. 8. 1. Do czynności podejmowanych przez zamawiającego, wykonawców oraz
uczestników konkursu w postępowaniu o udzielenie zamówienia i konkursie oraz do
umów w sprawach zamówień publicznych stosuje się przepisy ustawy z dnia 23 kwietnia
1964 r. – Kodeks cywilny (Dz. U. z 2022 r. poz. 1360), jeżeli przepisy ustawy nie
stanowią inaczej.
      2. Termin oznaczony w godzinach rozpoczyna się z początkiem pierwszej godziny
i kończy się z upływem ostatniej godziny.
      3. Jeżeli początkiem terminu oznaczonego w godzinach jest pewne zdarzenie, nie
uwzględnia się przy obliczaniu terminu godziny, w której to zdarzenie nastąpiło.
      4. Termin obejmujący dwa lub więcej dni zawiera co najmniej dwa dni robocze.
      5. Dniem roboczym nie jest dzień uznany ustawowo za wolny od pracy oraz sobota.
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




                                                     Oddział 2

                             Wyłączenia stosowania przepisów ustawy

     Art. 9. Przepisów ustawy nie stosuje się do zamówień klasycznych oraz zamówień
sektorowych, lub konkursów:
1)   których zamawiający jest obowiązany udzielić lub które ma obowiązek
     przeprowadzić na podstawie innej, niż określona ustawą, procedury:
     a)      organizacji międzynarodowej,
     b)      wynikającej               z         porozumienia           tworzącego      zobowiązanie
             prawnomiędzynarodowe, jak umowa międzynarodowa zawarta między
             Rzecząpospolitą Polską a jednym lub wieloma państwami niebędącymi
             członkami Unii Europejskiej, w celu pozyskania dostaw, usług lub robót
             budowlanych na potrzeby zrealizowania lub prowadzenia wspólnego
             przedsięwzięcia;
2)   w całości finansowanych przez organizację międzynarodową lub międzynarodową
     instytucję finansującą, jeżeli zamawiający stosuje do tych zamówień lub konkursów
     inną, niż określona ustawą, procedurę organizacji międzynarodowej lub
     międzynarodowej instytucji finansującej;
3)   finansowanych             w     ponad       50%       przez   organizację   międzynarodową   lub
     międzynarodową instytucję finansującą, jeżeli uzgodniono z nimi zastosowanie do
     tych zamówień lub konkursów innej, niż określona ustawą, procedury organizacji
     międzynarodowej lub międzynarodowej instytucji finansującej.

     Art. 10. 1. Przepisów ustawy nie stosuje się do zamówień lub konkursów
udzielanych przez:
1)   Narodowy Bank Polski związanych z:
     a)      wykonywaniem zadań dotyczących realizacji polityki pieniężnej, a w
             szczególności zamówień na usługi finansowe związane z emisją, sprzedażą,
             kupnem i transferem papierów wartościowych lub innych instrumentów
             finansowych,
     b)      obrotem papierami wartościowymi emitowanymi przez Skarb Państwa,
     c)      obsługą zarządzania długiem krajowym i zadłużeniem zagranicznym,
     d)      emisją znaków pieniężnych i gospodarką tymi znakami,
     e)      gromadzeniem rezerw dewizowych i zarządzaniem tymi rezerwami,
     f)      gromadzeniem złota i metali szlachetnych,
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     g)      prowadzeniem rachunków bankowych i przeprowadzaniem bankowych
             rozliczeń pieniężnych;
2)   Bank Gospodarstwa Krajowego:
     a)      związanych z realizacją zadań dotyczących obsługi funduszy utworzonych,
             powierzonych lub przekazanych Bankowi Gospodarstwa Krajowego oraz
             realizacją programów rządowych, w części dotyczącej:
             –     prowadzenia rachunków bankowych, przeprowadzania bankowych
                   rozliczeń pieniężnych i działalności na rynku międzybankowym,
             –     pozyskiwania           środków          finansowych     dla    zapewnienia      płynności
                   finansowej, finansowania działalności obsługiwanych funduszy i
                   programów oraz refinansowania akcji kredytowej,
     b)      związanych          z    operacjami           na   rynku    międzybankowym          dotyczących
             zarządzania długiem Skarbu Państwa oraz płynnością budżetu państwa,
     c)      związanych          z     wykonywaniem             działalności     bankowej       przez   Bank
             Gospodarstwa Krajowego, w części dotyczącej:
             –     otwierania i prowadzenia rachunków bankowych, przeprowadzania
                   bankowych           rozliczeń           pieniężnych    i      działalności    na     rynku
                   międzybankowym,
             –     pozyskiwania           środków          finansowych     dla    zapewnienia      płynności
                   finansowej oraz refinansowania akcji kredytowej,
     d)      o wartości mniejszej niż progi unijne;
3)   zamawiających publicznych oraz zamawiających subsydiowanych, w celu
     prowadzenia działalności w zakresie:
     a)      udostępniania publicznej sieci telekomunikacyjnej lub
     b)      obsługi publicznej sieci telekomunikacyjnej, lub
     c)      świadczenia publicznie dostępnych usług telekomunikacyjnych za pomocą
             publicznej sieci telekomunikacyjnej;
4)   zamawiających sektorowych, o których mowa w art. 5 ust. 1 pkt 1, wykonujących
     działalność sektorową w zakresie usług pocztowych, o której mowa w art. 5 ust. 4
     pkt 6, w celu świadczenia usług:
     a)      o wartości dodanej związanych z systemami teleinformatycznymi w
             rozumieniu ustawy z dnia 18 lipca 2002 r. o świadczeniu usług drogą
             elektroniczną, wyłącznie za pomocą takich systemów, w tym bezpiecznego
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




             przesyłania kodowanych dokumentów za pomocą systemów
             teleinformatycznych, usług zarządzania adresami i przesyłania poleconej
             poczty elektronicznej,

     b)      finansowych, objętych kodami CPV od 66100000-1 do 66720000-3,
             określonymi we Wspólnym Słowniku Zamówień, w szczególności przekazów
             pocztowych i pocztowych przelewów na konto,
     c)      filatelistycznych lub logistycznych;
5)   uchylony
     2. Przepisów ustawy nie stosuje się do zamówień:
1)   na usługi Narodowego Banku Polskiego;
2)   na usługi Banku Gospodarstwa Krajowego, w zakresie bankowej obsługi jednostek,
     o których mowa w art. 4 pkt 1 i 2, z wyłączeniem jednostek samorządu
     terytorialnego;
3)   udzielanych instytucji gospodarki budżetowej przez organ władzy publicznej
     wykonujący funkcje organu założycielskiego tej instytucji, jeżeli łącznie są
     spełnione następujące warunki:
     a)      ponad       80%       działalności        instytucji   gospodarki   budżetowej   dotyczy
             wykonywania zadań publicznych na rzecz tego organu władzy publicznej,
     b)      organ władzy publicznej sprawuje nad instytucją gospodarki budżetowej
             kontrolę odpowiadającą kontroli sprawowanej nad własnymi jednostkami
             organizacyjnymi nieposiadającymi osobowości prawnej, polegającą na
             wpływie na cele strategiczne oraz istotne decyzje dotyczące zarządzania
             sprawami instytucji,
     c)      przedmiot zamówienia należy do zakresu działalności podstawowej instytucji
             gospodarki budżetowej określonego zgodnie z art. 26 ust. 2 pkt 2 ustawy z dnia
             27 sierpnia 2009 r. o finansach publicznych;
4)   na usługi udzielane przez zamawiającego publicznego i zamawiającego
     sektorowego zamawiającemu publicznemu, któremu wyłączne prawo do
     świadczenia tych usług przyznano na podstawie ustawy lub innego aktu
     normatywnego podlegającego publikacji.
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     3. Przy obliczaniu procentu działalności, o którym mowa w ust. 2 pkt 3 lit. a,
uwzględnia się:
1)   średni całkowity obrót osiągnięty przez instytucję gospodarki budżetowej lub
2)   inną alternatywną miarę opartą na działalności, w szczególności koszty poniesione
     przez instytucję gospodarki budżetowej
– w odniesieniu do usług, dostaw lub robót budowlanych za 3 lata poprzedzające
udzielenie zamówienia.
     4. Jeżeli ze względu na dzień utworzenia lub rozpoczęcia działalności przez
instytucję gospodarki budżetowej lub reorganizację jej działalności, dane za 3 lata
poprzedzające udzielenie zamówienia dotyczące średniego całkowitego obrotu lub inna
alternatywna miara oparta na działalności, w szczególności koszty poniesione przez
instytucję gospodarki budżetowej, są niedostępne lub nieadekwatne, przy obliczaniu
procentu działalności, o którym mowa w ust. 2 pkt 3 lit. a, uwzględnia się wiarygodną
miarę, w szczególności prognozy dotyczące obrotu, kosztów lub innej alternatywnej
miary.

     Art. 11. 1. Przepisów ustawy nie stosuje się do zamówień lub konkursów, których
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
ze społeczną i zawodową integracją osób, o których mowa w art. 94 ust. 1 pkt 5;

     Art. 12. 1. Przepisów ustawy nie stosuje się do:
1)   zamówień lub konkursów:
     a)      którym nadano klauzulę zgodnie z przepisami ustawy z dnia 5 sierpnia 2010
             r. o ochronie informacji niejawnych (Dz. U. z 2019 r. poz. 742 oraz z 2022 r.
             poz. 655) lub, którym muszą towarzyszyć, na podstawie odrębnych przepisów,
             szczególne środki bezpieczeństwa lub
     b)      jeżeli wymaga tego istotny interes bezpieczeństwa państwa
     – w zakresie, w jakim ochrona istotnych interesów bezpieczeństwa państwa nie
     może zostać zagwarantowana w inny sposób, w szczególności z zastosowaniem
     przepisów działu VI;
2)   zamówień, dotyczących produkcji lub handlu bronią, amunicją lub materiałami
     wojennymi, o których mowa w art. 346 Traktatu o funkcjonowaniu Unii
     Europejskiej, jeżeli wymaga tego podstawowy interes bezpieczeństwa państwa, a
     udzielenie zamówienia bez zastosowania ustawy nie wpłynie negatywnie na
     warunki konkurencji na rynku wewnętrznym w odniesieniu do produktów, które nie
     są przeznaczone wyłącznie do celów wojskowych w zakresie, w jakim ochrona
     podstawowych              interesów          bezpieczeństwa   państwa   nie   może   zostać
     zagwarantowana w inny sposób, w szczególności z zastosowaniem przepisów działu
     VI.
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     2. [uchylony]

     Art. 13. 1. Przepisów ustawy nie stosuje się do zamówień w dziedzinach obronności
i bezpieczeństwa:
1)   w przypadkach, o których mowa w art. 11 ust. 1 pkt 1, 3 i 6, ust. 2 pkt 1 i art. 12;
2)   podlegających szczególnej procedurze:

     a)      na podstawie umowy międzynarodowej, której stroną jest Rzeczpospolita
             Polska, zawartej z jednym lub wieloma państwami niebędącymi członkami
             Unii Europejskiej, lub takiego porozumienia zawieranego na szczeblu
             ministerialnym,
     b)      na podstawie umowy międzynarodowej, której stroną jest Rzeczpospolita
             Polska, lub porozumienia zawieranego na szczeblu ministerialnym,
             związanych ze stacjonowaniem wojsk i dotyczących przedsiębiorców,
             niezależnie od ich siedziby lub miejsca zamieszkania
     c)      organizacji międzynarodowej zakupującej do swoich celów lub do zamówień,
             które muszą być udzielane przez Rzeczpospolitą Polską zgodnie z tą procedurą;
3)   w      przypadku          których       stosowanie    przepisów   ustawy   zobowiązywałoby
     zamawiającego do przekazania informacji, których ujawnienie jest sprzeczne z
     podstawowymi interesami bezpieczeństwa państwa;
4)   udzielanych do celów działalności wywiadowczej lub kontrwywiadowczej;
5)   udzielanych w ramach programu współpracy opartego na badaniach i rozwoju,
     prowadzonych wspólnie przez Rzeczpospolitą Polską i co najmniej jedno państwo
     członkowskie Unii Europejskiej nad opracowaniem nowego produktu oraz, tam
     gdzie ma to zastosowanie, do późniejszych etapów całości lub części cyklu życia
     tego produktu;
6)   udzielanych w państwie niebędącym członkiem Unii Europejskiej, w tym zamówień
     na dostawy sprzętu innego niż wojskowy, roboty budowlane lub usługi do celów
     logistycznych, realizowanych podczas rozmieszczenia sił zbrojnych, oraz sił, do
     których podstawowych zadań należy ochrona bezpieczeństwa, w przypadku gdy
     względy operacyjne wymagają ich udzielenia wykonawcom usytuowanym w strefie
     prowadzenia działań;
7)   udzielanych przez władze państwowe, regionalne lub lokalne władzom
     państwowym, regionalnym lub lokalnym innego państwa związanych z:
     a)      dostawami sprzętu wojskowego lub newralgicznego sprzętu lub
      ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




     b)      robotami budowlanymi i usługami bezpośrednio związanymi z takim sprzętem,
             lub
     c)      robotami budowlanymi i usługami wyłącznie do celów wojskowych lub
             newralgicznymi robotami budowlanymi lub usługami;
8)   których przedmiotem są usługi finansowe, z wyjątkiem usług ubezpieczeniowych.
     2. W przypadku zamówień, o których mowa w ust. 1 pkt 5, zamawiający po
wszczęciu programu jest obowiązany informować Komisję Europejską o części
wydatków na badania i rozwój dotyczących ogólnych kosztów programu współpracy,
porozumieniu dotyczącym podziału kosztów oraz o planowanych zamówieniach dla
każdego państwa członkowskiego Unii Europejskiej, o ile są one przewidziane.

     Art. 14. 1. Przepisów ustawy nie stosuje się do zamówień lub konkursów, których
przedmiot zamówienia zawiera aspekty obronności i bezpieczeństwa, podlegających
szczególnej procedurze:
1)   na podstawie umowy międzynarodowej, której stroną jest Rzeczpospolita Polska,
     zawartej z jednym lub wieloma państwami niebędącymi członkami Unii
     Europejskiej, lub takiego porozumienia zawieranego na szczeblu ministerialnym,
     i dotyczących robót budowlanych, dostaw lub usług przeznaczonych na potrzeby
     wspólnej realizacji lub eksploatacji projektu przez sygnatariuszy,
2)   na podstawie umowy międzynarodowej, której stroną jest Rzeczpospolita Polska,
     lub porozumienia zawieranego na szczeblu ministerialnym, związanych ze
     stacjonowaniem wojsk i dotyczących przedsiębiorców, niezależnie od ich siedziby
     lub miejsca zamieszkania,
3)   stosowanej przez organizację międzynarodową
– jeżeli zamówienia muszą być udzielane przez Rzeczpospolitą Polską zgodnie z tą
procedurą.

     2. Przepisów ustawy nie stosuje się do zamówień lub konkursów, o których mowa
w ust. 1:
1)   finansowanych w całości przez organizację międzynarodową lub międzynarodową
     instytucję finansującą, jeżeli zamawiający stosuje do nich inną, niż określona
     ustawą, procedurę organizacji międzynarodowej lub międzynarodowej instytucji
     finansującej;
     ®   ApexNet. Wiedza, która chroni | www.apexnet.pl




2)   finansowanych            w     ponad       50%       przez   organizację   międzynarodową      lub
     międzynarodową instytucję finansującą, jeżeli uzgodniono z nimi zastosowanie do
     tych zamówień lub konkursów innej, niż określona ustawą, procedury organizacji
     międzynarodowej lub międzynarodowej instytucji finansującej.

     Art. 15. [uchylony]

                                                    Rozdział 2

                                      Zasady udzielania zamówień

     Art. 16. Zamawiający przygotowuje i przeprowadza postępowanie o udzielenie
zamówienia w sposób:
1)   zapewniający zachowanie uczciwej konkurencji oraz równe traktowanie
     wykonawców;
2)   przejrzysty;
3)   proporcjonalny.
     Art. 17. 1. Zamawiający udziela zamówienia w sposób zapewniający:
1)   najlepszą jakość dostaw, usług, oraz robót budowlanych, uzasadnioną charakterem
     zamówienia, w ramach środków, które zamawiający może przeznaczyć na jego
     realizację oraz
2)   uzyskanie najlepszych efektów zamówienia, w tym efektów społecznych,
     środowiskowych oraz gospodarczych, o ile którykolwiek z tych efektów jest
     możliwy do uzyskania w danym zamówieniu, w stosunku do poniesionych
     nakładów.
     2. Zamówienia udziela się wykonawcy wybranemu zgodnie z przepisami ustawy.
     3. Czynności związane z przygotowaniem oraz przeprowadzeniem postępowania o
udzielenie zamówienia wykonują osoby zapewniające bezstronność i obiektywizm.

     Art. 18. 1. Postępowanie o udzielenie zamówienia jest jawne.
     2. Zamawiający            może       ograniczyć        dostęp   do   informacji   związanych    z
postępowaniem o udzielenie zamówienia tylko w przypadkach określonych w ustawie.
     3. Nie ujawnia się informacji stanowiących tajemnicę przedsiębiorstwa w
rozumieniu przepisów ustawy z dnia 16 kwietnia 1993 r. o zwalczaniu nieuczciwej
konkurencji (Dz. U. z 2022 r. poz. 1233), jeżeli wykonawca, wraz z przekazaniem takich
informacji, zastrzegł, że nie mogą być one udostępniane oraz wykazał, że zastrzeżone
informacje stanowią tajemnicę przedsiębiorstwa. Wykonawca nie może zastrzec
informacji, o których mowa w art. 222 ust. 5.
     ®    ApexNet. Wiedza, która chroni | www.apexnet.pl




     4. Zamawiający może określić w dokumentach zamówienia lub w ogłoszeniu o
zamówieniu wymaganie dotyczące zachowania poufnego charakteru informacji
przekazanych wykonawcy w toku postępowania o udzielenie zamówienia.
     5. Jeżeli jest to uzasadnione ochroną prywatności lub interesem publicznym,
zamawiający może nie ujawniać:
1)   danych osobowych, w przypadku zamówienia udzielonego na podstawie art. 214
     ust. 1 pkt 1 lit. b,
2)   wysokości wynagrodzenia, w przypadku zamówienia udzielonego na podstawie art.
     214 ust. 1 pkt 2

– w zakresie dostaw lub usług, z zakresu działalności kulturalnej związanej z organizacją
wystaw,       koncertów,          konkursów,          festiwali,   widowisk,   spektakli   teatralnych,
przedsięwzięć z zakresu edukacji kulturalnej lub z gromadzeniem materiałów
bibliotecznych przez biblioteki lub muzealiów, a także z zakresu działalności archiwalnej
związanej z gromadzeniem materiałów archiwalnych, jeżeli zamówienia te nie służą
wyposażaniu zamawiającego w środki trwałe przeznaczone do bieżącej obsługi jego
działalności, o ile wykonawca, przed zawarciem umowy w sprawie zamówienia
publicznego, zastrzegł, że dane te nie mogą być udostępniane.
     6. Zamawiający udostępnia dane osobowe, o których mowa w art. 10
rozporządzenia Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016
r. w sprawie ochrony osób fizycznych w związku z przetwarzaniem danych osobowych i
w sprawie swobodnego przepływu takich danych oraz uchylenia dyrektywy 95/46/WE
(ogólne rozporządzenie o ochronie danych) (Dz. Urz. UE L 119 z 4.05.2016, str. 1, z
późn. zm.6)), zwanego dalej „rozporządzeniem 2016/679”, w celu umożliwienia
korzystania ze środków ochrony prawnej, o których mowa w dziale IX, do upływu
terminu na ich wniesienie.

     Art. 19. 1. Zamawiający może realizować obowiązki informacyjne, o których mowa
w art. 13 ust. 1–3 rozporządzenia 2016/679, przez zamieszczenie wymaganych informacji
w ogłoszeniu o zamówieniu lub w dokumentach zamówienia.
     2. Skorzystanie przez osobę, której dane osobowe dotyczą, z uprawnienia do
sprostowania lub uzupełnienia, o którym mowa w art. 16 rozporządzenia 2016/679, nie
może skutkować zmianą wyniku postępowania o udzielenie zamówienia ani zmianą
postanowień umowy w sprawie zamówienia publicznego w zakresie niezgodnym z
ustawą.
         ®   ApexNet. Wiedza, która chroni | www.apexnet.pl

"""


if __name__ == '__main__':
    process_and_save_file('../data/txt/pzp.txt',
        '../data/pzp_processed_with_metadata_fixed.json')