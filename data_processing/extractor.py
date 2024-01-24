import re


def extract_paragraphs(text):
    paragraph_pattern = r'§ \d+\. '
    matches = [(match.start(), match.end()) for match in re.finditer(paragraph_pattern, text)]

    # print("Positions of findings:")
    paragraphs = []
    for i, (start, end) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        substring = text[start:next_start]
        paragraphs.append(substring)
        # print(f"Start: {start}, End: {end}, Match: {text[start:end]}, Extracted: {substring}")
    return paragraphs


def process_text(text):
    chapter_pattern = re.compile(r'Rozdział\s+(\d+)')
    # Find all chapters
    chapters = [m for m in chapter_pattern.finditer(text)]
    paragraph_nb = 0
    records = []
    for i, chapter in enumerate(chapters):
        chapter_nb = chapter.group(1)
        # Determine the text scope for the current chapter
        start = chapter.end()
        end = chapters[i + 1].start() if i + 1 < len(chapters) else len(text)
        chapter_text = text[start:end]

        # Title is first line of each chapter
        title = chapter_text.strip().splitlines()[0]
        print(f'Chapter {chapter_nb} title: {title}')
        # print(f'TXT: {chapter_text}')
        paragraphs = extract_paragraphs(chapter_text)

        for paragraph in paragraphs:
            paragraph_nb += 1
            print(f'Paragraph {paragraph_nb}: {paragraph}')
        #         record = {
        #             "txt": point_text,
        #             "chapter": chapter_nb,
        #             "paragraph": paragraph_nb,
        #             "point": point_nb,
        #             "title": title
        #         }
        #         records.append(record)

    return records

text_to_process = """
                                                      Rozdział 1
                                                   Przepisy ogólne
     § 1. Rozporządzenie określa:
1)   tryb przeprowadzania postępowania kwalifikacyjnego oraz uzupełniającego postępowania kwalifikacyjnego, a także
     sposób ustalania jego wyniku, jak również sposób wniesienia odwołania od wyniku oraz tryb i sposób rozpatrzenia
     odwołania;
2)   dokumenty, które należy dołączyć do zgłoszenia kandydata na członka Izby, potwierdzające spełnianie warunków,
     o których mowa w art. 474 ust. 2 pkt 1–6 i 8–10 ustawy z dnia 11 września 2019 r. – Prawo zamówień publicznych,
     oraz zakres danych, które ma zawierać to zgłoszenie;
3)   szczegółowy zakres zagadnień, w oparciu o które przeprowadzane jest postępowanie kwalifikacyjne oraz uzupełnia-
     jące postępowanie kwalifikacyjne;
4)   sposób powoływania komisji kwalifikacyjnej, szczegółowe wymagania wobec członków komisji kwalifikacyjnej oraz
     organizację jej pracy.

                                                      Rozdział 2
                           Zgłoszenie kandydata na członka Krajowej Izby Odwoławczej
      § 2. 1. Zgłoszenie kandydata na członka Krajowej Izby Odwoławczej, zwanej dalej „Izbą”, jest składane w postępo-
waniu kwalifikacyjnym, w miejscu wskazanym w ogłoszeniu, o którym mowa w art. 477 ust. 4 ustawy z dnia 11 września
2019 r. – Prawo zamówień publicznych, zwanej dalej „ustawą”, w tym na adres tam wskazany. Za datę złożenia zgłoszenia
uważa się datę jego wpływu na adres, o którym mowa w zdaniu pierwszym. Zgłoszenie uznaje się za złożone w terminie,
jeżeli wpłynie ono na wskazany adres nie później niż w dniu, w którym upływa termin przyjmowania zgłoszeń.
     2. Zgłoszenie kandydata na członka Izby, zwane dalej „zgłoszeniem”, zawiera wniosek o dopuszczenie kandydata do
postępowania kwalifikacyjnego, w którym:
1)   podaje się imię i nazwisko, drugie imię – o ile kandydat je posiada, datę i miejsce urodzenia, numer PESEL, imiona
     rodziców, serię i numer dowodu osobistego, adres miejsca zameldowania kandydata, adres jego miejsca zamieszkania
     oraz adres do korespondencji, jeżeli jest inny niż adres miejsca zamieszkania;
2)   opisuje się posiadane przez kandydata wykształcenie, doświadczenie oraz przebieg kariery zawodowej, odpowiadające
     warunkom, o których mowa w art. 474 ust. 2 pkt 2–4 ustawy.
Dziennik Ustaw                                               –2–                                                      Poz. 381

     3. Do zgłoszenia kandydat na członka Izby, zwany dalej „kandydatem”, może dołączyć oświadczenie o wyrażeniu
zgody na doręczanie mu pism w postępowaniu kwalifikacyjnym przy użyciu środków komunikacji elektronicznej wraz
z podaniem adresu poczty elektronicznej, pod jakim korespondencja będzie przez kandydata odbierana. Złożenie zgłoszenia
bez oświadczenia, o którym mowa w zdaniu pierwszym, jest równoznaczne z brakiem zgody na doręczanie pism w postępo-
waniu kwalifikacyjnym przy użyciu środków komunikacji elektronicznej.

    4. Do zgłoszenia, w celu potwierdzenia spełniania warunków, o których mowa w art. 474 ust. 2 pkt 1–6 i 8–10 ustawy,
kandydat dołącza:
1)   oświadczenie o posiadaniu polskiego obywatelstwa;
2)   kopię dyplomu potwierdzającego ukończenie studiów na kierunku prawo;
3)   kopię uchwały o uzyskaniu pozytywnego wyniku z egzaminu sędziowskiego, prokuratorskiego, notarialnego, adwo-
     kackiego lub radcowskiego lub kopię powołania na stanowisko sędziowskie, prokuratorskie lub stanowisko notariu-
     sza, lub kopię uchwały właściwego organu samorządu zawodowego adwokatury lub samorządu radców prawnych
     o wpisie odpowiednio na listę adwokatów lub radców prawnych;
4)   oświadczenie o posiadaniu minimum pięcioletniego doświadczenia zawodowego w zakresie zamówień publicznych
     oraz prawa cywilnego, wraz z kopią dokumentów potwierdzających to doświadczenie;
5)   oświadczenie o posiadaniu pełnej zdolności do czynności prawnych;
6)   oświadczenie o korzystaniu z pełni praw publicznych;
7)   aktualną informację z Krajowego Rejestru Karnego, wystawioną nie wcześniej niż 30 dni przed dniem złożenia zgło-
     szenia, potwierdzającą, że nie był skazany prawomocnym wyrokiem za przestępstwo umyślne lub umyślne przestęp-
     stwo skarbowe;
8)   kopię poświadczenia bezpieczeństwa upoważniającego do dostępu do informacji niejawnych o klauzuli „poufne” lub
     wyższej albo oświadczenie o wyrażeniu zgody na przeprowadzenie postępowania sprawdzającego, o którym mowa
     w art. 22 ust. 1 pkt 1 lub 2 ustawy z dnia 5 sierpnia 2010 r. o ochronie informacji niejawnych (Dz. U. z 2019 r. poz. 742).

     § 3. 1. W przypadku gdy kandydat nie dołączył do zgłoszenia dokumentów, o których mowa w § 2 ust. 4, lub dołą-
czone dokumenty zawierają błędy, lub w zgłoszeniu nie podał danych, o których mowa w § 2 ust. 2, lub nie zostało ono
opatrzone własnoręcznym podpisem kandydata, w przypadku zgłoszenia składanego w formie pisemnej, lub kwalifikowa-
nym podpisem elektronicznym, podpisem osobistym lub podpisem zaufanym, w przypadku zgłoszenia składanego
w postaci elektronicznej, kandydat wzywany jest do uzupełnienia braków formalnych, w tym uzupełnienia lub poprawienia
dokumentów lub zgłoszenia, w terminie 7 dni od dnia doręczenia wezwania.

     2. Kandydat składa uzupełnione lub poprawione dokumenty lub zgłoszenie w miejscu, o którym mowa w § 2 ust. 1
zdanie pierwsze. Przepisy § 2 ust. 1 zdanie drugie i trzecie stosuje się odpowiednio.

    3. Niezwłocznie po upływie terminu przyjmowania zgłoszeń lub upływie terminu uzupełnienia braków formalnych
komisja kwalifikacyjna powołana do przeprowadzenia postępowania kwalifikacyjnego, zwana dalej „komisją”, podejmuje
uchwałę o dopuszczeniu kandydata do udziału w postępowaniu kwalifikacyjnym.

      4. Jeżeli kandydat nie uzupełnił w terminie braków formalnych lub złożył zgłoszenie po terminie, o którym mowa
w art. 477 ust. 4 pkt 2 ustawy, komisja podejmuje uchwałę o odmowie dopuszczenia kandydata do udziału w tym postępowaniu.

     5. Przewodniczący komisji, za pośrednictwem operatora pocztowego, w rozumieniu ustawy z dnia 23 listopada 2012 r. –
Prawo pocztowe (Dz. U. z 2020 r. poz. 1041 i 2320), zwanego dalej „operatorem pocztowym”, przesyłką poleconą, za
pośrednictwem posłańca albo przy użyciu środków komunikacji elektronicznej, o ile kandydat złożył oświadczenie, o którym
mowa w § 2 ust. 3, pouczając o prawie do wniesienia odwołania, terminie na jego wniesienie, organie, do którego należy je
wnieść, oraz adresie, na który odwołanie powinno być wniesione, zawiadamia:
1)   kandydatów dopuszczonych do udziału w postępowaniu kwalifikacyjnym – o miejscu i terminie przeprowadzenia
     egzaminu pisemnego;
2)   pozostałych kandydatów – o odmowie dopuszczenia ich do udziału w postępowaniu kwalifikacyjnym, podając przy-
     czyny odmowy dopuszczenia.

     6. W przypadku wniesienia przez kandydata odwołania od uchwały komisji kwalifikacyjnej o odmowie dopuszczenia
do udziału w postępowaniu kwalifikacyjnym termin 7 dni na jego wniesienie jest liczony od dnia doręczenia uchwały.
Dziennik Ustaw                                           –3–                                                   Poz. 381

     7. Minister właściwy do spraw gospodarki:
1)   odrzuca odwołanie złożone po upływie terminu na wniesienie odwołania albo
2)   oddala odwołanie i utrzymuje w mocy uchwałę komisji, albo
3)   uwzględnia odwołanie, zmienia uchwałę komisji i dopuszcza kandydata do udziału w postępowaniu kwalifikacyjnym.

      8. Minister właściwy do spraw gospodarki niezwłocznie, nie później niż w terminie 7 dni od dnia wniesienia odwoła-
nia, przekazuje kandydatowi rozstrzygnięcie odwołania za pośrednictwem operatora pocztowego, przesyłką poleconą, za
pośrednictwem posłańca albo przy użyciu środków komunikacji elektronicznej, o ile kandydat złożył oświadczenie,
o którym mowa w § 2 ust. 3.

                                                      Rozdział 3
 Tryb przeprowadzania postępowania kwalifikacyjnego oraz wnoszenie odwołania od wyniku tego postępowania
    § 4. 1. Komisja przeprowadza egzamin pisemny w warunkach umożliwiających kandydatom samodzielną pracę, pod
nadzorem przewodniczącego komisji oraz jej członków.

     2. Wszyscy zgłoszeni kandydaci przystępują do sprawdzianu wiedzy oraz sporządzenia pracy pisemnej w tym samym
terminie i w tym samym miejscu.

     § 5. 1. Egzamin pisemny składa się:
1)   ze sprawdzianu wiedzy, mającego na celu sprawdzenie teoretycznej wiedzy z zakresu zamówień publicznych oraz
     prawa cywilnego;
2)   z pracy pisemnej, mającej na celu sprawdzenie praktycznej wiedzy z zakresu zamówień publicznych oraz prawa
     cywilnego.

     2. Przerwa między częściami egzaminu pisemnego nie może trwać dłużej niż 30 minut.

     3. Egzamin pisemny jest przeprowadzany w oparciu o zestaw materiałów do sprawdzianu wiedzy oraz zestaw mate-
riałów do pracy pisemnej. Zestawy wybiera komisja spośród propozycji czterech zestawów materiałów służących do prze-
prowadzenia każdej z części egzaminu pisemnego, zawierających pytania testowe do sprawdzianu wiedzy i zadanie do
pracy pisemnej oraz arkusze odpowiedzi i klucze ich oceny, przygotowane z uwzględnieniem zakresu zagadnień do prze-
prowadzenia postępowania kwalifikacyjnego określonego w załączniku nr 1 do rozporządzenia.

     4. Wybrane zestawy są:
1)   powielane w liczbie odpowiadającej liczbie kandydatów dopuszczonych do udziału w postępowaniu kwalifikacyjnym
     i umieszczane w zamkniętych opakowaniach opatrzonych pieczęcią Urzędu Zamówień Publicznych, zwanego dalej
     „Urzędem”;
2)   przechowywane i zabezpieczone w siedzibie Urzędu w sposób uniemożliwiający ich nieuprawnione ujawnienie;
3)   dostarczane w zamkniętych opakowaniach opatrzonych pieczęcią Urzędu na salę egzaminacyjną przez przewodniczą-
     cego komisji i wskazanego przez niego członka komisji, najwcześniej na pół godziny przed rozpoczęciem egzaminu
     pisemnego.

     § 6. 1. Sprawdzian wiedzy ma formę testu jednokrotnego wyboru i składa się z 50 pytań. Za każdą prawidłową odpo-
wiedź kandydat otrzymuje dwa punkty, a za brak odpowiedzi – zero punktów. Maksymalna liczba punktów możliwych do
uzyskania ze sprawdzianu wiedzy wynosi 100.

     2. Sprawdzian wiedzy trwa 60 minut.

     § 7. 1. Praca pisemna polega na dokonaniu przez kandydata oceny prawnej stanu faktycznego (kazusu) na podstawie
zestawu materiałów do pracy pisemnej, o którym mowa w § 5 ust. 3, składającego się z dokumentów zakwalifikowanych
przez komisję na potrzeby egzaminu pisemnego lub dokumentów opracowanych na potrzeby tego egzaminu. Każdy kan-
dydat ocenia ten sam stan faktyczny.

     2. Praca pisemna trwa 120 minut.

     3. Praca pisemna jest oceniana pod względem merytorycznym, języka i stylu pracy, zgodnie z punktacją określoną
w załączniku nr 2 do rozporządzenia. Maksymalna liczba punktów możliwych do uzyskania z pracy pisemnej wynosi 100.
Dziennik Ustaw                                             –4–                                                   Poz. 381

     § 8. 1. Przed rozpoczęciem sprawdzianu wiedzy:
1)   kandydat:
     a)   okazuje dokument zawierający zdjęcie, potwierdzający jego tożsamość, i potwierdza własnoręcznym podpisem
          na liście obecności udział w sprawdzianie wiedzy,
     b) losuje kopertę z oznaczeniem „Sprawdzian wiedzy”, w której znajduje się karta z indywidualnym numerem kodu
        do oznaczenia arkusza odpowiedzi do sprawdzianu wiedzy,
     c)   przekazuje komisji do depozytu na czas trwania egzaminu pisemnego wyłączony telefon komórkowy i inne urzą-
          dzenia służące do komunikacji elektronicznej, o ile takie posiada; telefon i inne złożone do depozytu urządzenia
          służące do komunikacji elektronicznej przechowuje się w zaklejonych i podpisanych kopertach lub opakowaniach;
2)   przewodniczący, wiceprzewodniczący lub sekretarz komisji informuje kandydatów o:
     a)   warunkach organizacyjnych i sposobie przeprowadzenia egzaminu pisemnego,
     b) przepisach porządkowych obowiązujących w trakcie przeprowadzania egzaminu pisemnego,
     c)   zasadach dokonywania oceny udzielonych odpowiedzi oraz oceny pracy pisemnej,
     d) sposobie zawiadomienia o wynikach egzaminu pisemnego,
     e)   sposobie zawiadomienia o terminie i miejscu przeprowadzenia rozmowy kwalifikacyjnej.
     2. Otwarcie opatrzonego pieczęcią Urzędu opakowania z pytaniami testowymi następuje w dniu i o godzinie rozpo-
częcia sprawdzianu wiedzy, w obecności osób przystępujących do egzaminu pisemnego. Z czynności tej sporządza się
protokół podpisany przez członków komisji.
     3. Przed rozpoczęciem sprawdzianu wiedzy kandydat:
1)   otrzymuje opatrzone pieczęcią Urzędu:
     a)   arkusz z pytaniami testowymi,
     b) arkusz odpowiedzi do sprawdzianu wiedzy;
2)   wpisuje w prawym górnym rogu na pierwszej stronie arkusza odpowiedzi do sprawdzianu wiedzy indywidualny numer
     kodu znajdujący się na karcie w wylosowanej kopercie;
3)   zapisuje swoje imię i nazwisko na karcie z numerem kodu, umieszcza kartę z powrotem w kopercie, zakleja i oddaje
     komisji.
     § 9. 1. Przed rozpoczęciem pracy pisemnej kandydat:
1)   okazuje dokument zawierający zdjęcie, potwierdzający jego tożsamość, i potwierdza własnoręcznym podpisem na
     liście obecności udział w pracy pisemnej;
2)   losuje kopertę z oznaczeniem „Praca pisemna”, w której znajduje się karta z indywidualnym numerem kodu do ozna-
     czenia pracy pisemnej.
     2. Otwarcie opatrzonego pieczęcią Urzędu opakowania z zadaniem pracy pisemnej następuje w dniu i o godzinie roz-
poczęcia pracy pisemnej w obecności osób przystępujących do egzaminu pisemnego. Z czynności tej sporządza się proto-
kół podpisany przez wszystkich członków komisji obecnych podczas pracy pisemnej.
     3. Przed rozpoczęciem pracy pisemnej kandydat:
1)   otrzymuje opatrzone pieczęcią Urzędu:
     a)   nieoznakowaną zaklejoną kopertę z zadaniem pracy pisemnej,
     b) spięte i ponumerowane czyste karty przeznaczone do sporządzenia pracy pisemnej;
2)   wpisuje w prawym górnym rogu na pierwszej czystej karcie przeznaczonej do sporządzenia pracy pisemnej indywi-
     dualny numer kodu znajdujący się na karcie w wylosowanej kopercie;
3)   zapisuje swoje imię i nazwisko na karcie z numerem kodu, umieszcza kartę z powrotem w kopercie, zakleja i oddaje
     komisji.
    § 10. 1. Przewodniczący komisji, wiceprzewodniczący lub sekretarz tej komisji wyklucza bez ostrzeżenia z postępo-
wania kwalifikacyjnego kandydata, który podczas sprawdzianu wiedzy lub pracy pisemnej:
1)   korzysta z pomocy innej osoby;
2)   posługuje się niedozwolonymi materiałami;
Dziennik Ustaw                                            –5–                                                   Poz. 381

3)   korzysta z urządzeń służących do przekazu lub odbioru informacji;
4)   porozumiewa się lub pomaga pozostałym kandydatom;
5)   w inny sposób zakłóca przebieg postępowania kwalifikacyjnego.
     2. Wykluczenie zostaje odnotowane w protokole z przebiegu egzaminu pisemnego oraz na arkuszu odpowiedzi lub na
pracy pisemnej.
    3. W trakcie egzaminu pisemnego kandydat może opuścić salę egzaminacyjną po uzyskaniu zgody przewodniczącego
komisji kwalifikacyjnej, pod nadzorem członka komisji wskazanego przez przewodniczącego. Przed opuszczeniem sali
kandydat przekazuje arkusz odpowiedzi do sprawdzianu wiedzy lub pracę pisemną przewodniczącemu komisji. Członek
komisji odnotowuje na egzemplarzu arkusza odpowiedzi lub pracy pisemnej kandydata godzinę wyjścia i powrotu na salę.

     4. Opuszczenie przez kandydata sali egzaminacyjnej bez zgody przewodniczącego komisji stanowi zakończenie
udziału w postępowaniu kwalifikacyjnym. Przed opuszczeniem sali egzaminacyjnej kandydat zwraca arkusz odpowiedzi do
sprawdzianu wiedzy lub pracę pisemną.

     5. Po upływie czasu wskazanego odpowiednio w § 6 ust. 2 i § 7 ust. 2 członkowie komisji zbierają arkusze z pytaniami
testowymi i arkusze odpowiedzi do sprawdzianu wiedzy albo zadanie pracy pisemnej i pracę pisemną. W momencie oddania
kandydat otrzymuje pokwitowanie odbioru odpowiednio arkusza z pytaniami testowymi i arkusza odpowiedzi do spraw-
dzianu wiedzy albo zadania pracy pisemnej i pracy pisemnej.

     6. Z czynności odbioru odpowiednio arkusza z pytaniami testowymi i arkusza odpowiedzi do sprawdzianu wiedzy
albo zadania pracy pisemnej i pracy pisemnej sporządza się protokół, który zawiera w szczególności godzinę odbioru dla
danego numeru kodu i podpis odbierającego członka komisji kwalifikacyjnej.

     7. Członkowie komisji obecni w sali egzaminacyjnej sporządzają protokół z przebiegu egzaminu pisemnego, który
zawiera imiona i nazwiska członków komisji, oznaczenie godziny rozpoczęcia i zakończenia sprawdzianu wiedzy oraz
pracy pisemnej, liczbę osób uczestniczących w każdej części egzaminu pisemnego, informację o wykluczeniu kandydata
albo opuszczeniu przez niego sali egzaminacyjnej bez zgody przewodniczącego – oznaczonego indywidualnym numerem
kodu znajdującego się na karcie w wylosowanej kopercie do oznaczenia odpowiednio sprawdzianu wiedzy albo pracy
pisemnej, o ile wykluczenie albo opuszczenie miało miejsce, a także uwagi dotyczące przebiegu egzaminu, oraz podpisy
członków komisji egzaminacyjnej.

     § 11. 1. Komisja uwzględnia tylko odpowiedzi udzielone na arkuszu odpowiedzi do sprawdzianu wiedzy oraz kartach
przeznaczonych do sporządzenia pracy pisemnej, opatrzonych pieczęcią Urzędu.
     2. Arkusze odpowiedzi do sprawdzianu wiedzy i prace pisemne kandydatów oznaczone indywidualnymi kodami są
rozkodowywane po sprawdzeniu wszystkich prac.
     3. Do rozkodowania arkuszy odpowiedzi do sprawdzianu wiedzy i prac pisemnych przewodniczący komisji wyznacza
co najmniej dwóch członków tej komisji, którzy nie sprawdzali odpowiedzi albo prac pisemnych. Z rozkodowania sporzą-
dza się protokół, który podpisują członkowie komisji dokonujący rozkodowania.
    § 12. Po zakończeniu egzaminu pisemnego komisja ustala wyniki. Przewodniczący komisji zawiadamia kandydatów
za pośrednictwem operatora pocztowego, przesyłką poleconą, za pośrednictwem posłańca albo przy użyciu środków
komunikacji elektronicznej, o ile kandydat złożył oświadczenie, o którym mowa w § 2 ust. 3, o:
1)   wynikach egzaminu pisemnego z podziałem na sprawdzian wiedzy i pracę pisemną,
2)   terminie i miejscu przeprowadzenia rozmowy kwalifikacyjnej albo o odmowie dopuszczenia do rozmowy kwalifika-
     cyjnej
– pouczając o prawie do wniesienia odwołania od wyników, terminie na jego wniesienie, organie, do którego należy je
wnieść, oraz adresie, na który odwołanie powinno być wniesione.

     § 13. 1. Do rozmowy kwalifikacyjnej dopuszcza się kandydatów, którzy uzyskali nie mniej niż 50 punktów ze spraw-
dzianu wiedzy oraz nie mniej niż 50 punktów z pracy pisemnej.
      2. Jeżeli liczba kandydatów, którzy uzyskali minimalną liczbę punktów ze sprawdzianu wiedzy oraz pracy pisemnej,
jest większa niż dwukrotność limitu osób określonego w ogłoszeniu o postępowaniu kwalifikacyjnym, do rozmowy kwali-
fikacyjnej zaprasza się kandydatów, którzy otrzymali kolejno największą liczbę punktów w ramach dwukrotności limitu.
Limit może zostać przekroczony, jeżeli dwóch lub więcej kandydatów uzyska taką samą liczbę punktów umożliwiającą
zaproszenie do rozmowy kwalifikacyjnej w ramach dwukrotności limitu.
    § 14. 1. Podczas rozmowy kwalifikacyjnej sprawdza się cechy osobowe kandydata, kompetencje i predyspozycje do
wykonywania obowiązków członka Izby, biorąc pod uwagę kryteria oceny określone w załączniku nr 3 do rozporządzenia.
Dziennik Ustaw                                            –6–                                                    Poz. 381

     2. Rozmowa kwalifikacyjna z kandydatem trwa nie dłużej niż 20 minut.

     3. Rozmowę z kandydatem przeprowadza komisja w składzie co najmniej trzech jej członków. Komisja nie może
w tym samym czasie przeprowadzać rozmowy kwalifikacyjnej z więcej niż jednym kandydatem.
     4. Ocena jest sporządzana przez każdego członka komisji biorącego udział w rozmowie kwalifikacyjnej. Ocenę kan-
dydata w danym kryterium stanowi średnia arytmetyczna ocen członków komisji. Maksymalna liczba punktów możliwych
do uzyskania podczas rozmowy kwalifikacyjnej wynosi 30. O uzyskanej liczbie punktów podczas rozmowy kwalifikacyj-
nej przewodniczący komisji zawiadamia kandydatów za pośrednictwem operatora pocztowego, przesyłką poleconą, za
pośrednictwem posłańca albo przy użyciu środków komunikacji elektronicznej, o ile kandydat złożył oświadczenie,
o którym mowa w § 2 ust. 3.

      5. Po zakończeniu wszystkich rozmów kwalifikacyjnych przewodniczący komisji zawiadamia kandydatów, którzy zo-
stali dopuszczeni do rozmowy kwalifikacyjnej, o zakończeniu rozmów oraz o ostatecznych wynikach za pośrednictwem
operatora pocztowego, przesyłką poleconą, za pośrednictwem posłańca albo przy użyciu środków komunikacji elektro-
nicznej, o ile kandydat złożył oświadczenie, o którym mowa w § 2 ust. 3, pouczając o prawie do wniesienia odwołania,
terminie na jego wniesienie, organie, do którego należy je wnieść, oraz adresie, na który odwołanie powinno być wniesione.

     § 15. 1. W przypadku wniesienia przez kandydata odwołania od uchwały komisji dotyczącej wyników:
1)   egzaminu pisemnego,
2)   rozmowy kwalifikacyjnej
– termin 7 dni na wniesienie odwołania jest liczony od dnia otrzymania zawiadomienia o wyniku, o którym mowa odpo-
wiednio w § 12 albo § 14 ust. 5.

     2. Odwołanie wnosi się na adres wskazany w zawiadomieniu, o którym mowa odpowiednio w § 12 albo § 14 ust. 5.
Odwołanie może być wniesione osobiście, za pośrednictwem operatora pocztowego, przesyłką poleconą albo za pośrednic-
twem posłańca, a także przy użyciu środków komunikacji elektronicznej, w tym na elektroniczną skrzynkę podawczą urzę-
du obsługującego ministra właściwego do spraw gospodarki lub na adres poczty elektronicznej, jeżeli został wskazany
w zawiadomieniu, o którym mowa odpowiednio w § 12 albo § 14 ust. 5. Odwołanie wnoszone w postaci elektronicznej
wymaga opatrzenia, przez wnoszącego, kwalifikowanym podpisem elektronicznym, podpisem osobistym albo podpisem
zaufanym.

     3. Za datę wniesienia odwołania uznaje się datę wpływu odwołania na adres wskazany w zawiadomieniu, o którym
mowa odpowiednio w § 12 albo § 14 ust. 5, albo datę złożenia odwołania w placówce pocztowej operatora wyznaczonego,
w rozumieniu ustawy z dnia 23 listopada 2012 r. – Prawo pocztowe, jeżeli odwołanie zostało złożone za pośrednictwem
tego operatora. Jeżeli odwołanie jest wnoszone w postaci elektronicznej, za datę jego wniesienia uznaje się datę wpływu
odwołania na elektroniczną skrzynkę podawczą urzędu obsługującego ministra właściwego do spraw gospodarki lub na
adres poczty elektronicznej, wskazany w zawiadomieniu, o którym mowa odpowiednio w § 12 albo § 14 ust. 5.
     4. W terminie na wniesienie odwołania kandydat ma prawo wglądu do:
1)   dotyczącej jego osoby uchwały komisji wraz z jej uzasadnieniem;
2)   dokumentów zawierających jego indywidualne wyniki;
3)   zawiadomień dotyczących jego osoby.

     5. Kandydat ma prawo sporządzenia notatek oraz fotokopii dokumentów zawierających jego indywidualne wyniki.

    6. Minister właściwy do spraw gospodarki, po zasięgnięciu opinii Prezesa Urzędu Zamówień Publicznych, rozpatruje
odwołanie w terminie 10 dni od dnia upływu terminu na wniesienie odwołania.

     7. Minister właściwy do spraw gospodarki:
1)   odrzuca odwołanie złożone po upływie terminu na wniesienie odwołania albo
2)   oddala odwołanie i utrzymuje w mocy uchwałę komisji, albo
3)   uwzględnia odwołanie, uchyla czynności komisji podjęte w zakresie dotyczącym kandydata, którego odwołanie zosta-
     ło uwzględnione, i nakazuje ich powtórzenie.
      8. Minister właściwy do spraw gospodarki niezwłocznie przekazuje kandydatowi rozstrzygnięcie odwołania za po-
średnictwem operatora pocztowego, przesyłką poleconą, za pośrednictwem posłańca albo przy użyciu środków komunika-
cji elektronicznej, o ile kandydat złożył oświadczenie, o którym mowa w § 2 ust. 3.

     9. Na czynność komisji wykonaną w wyniku rozpatrzenia odwołania nie przysługuje odwołanie.
Dziennik Ustaw                                            –7–                                                   Poz. 381

     § 16. 1. Po zakończeniu postępowania kwalifikacyjnego i rozpatrzeniu odwołań, o ile zostały wniesione:
1)   komisja ustala, w drodze uchwały, ocenę końcową z postępowania kwalifikacyjnego, którą stanowi suma punktów
     uzyskanych przez kandydata z egzaminu pisemnego i rozmowy kwalifikacyjnej;
2)   przewodniczący komisji zawiadamia pisemnie, za potwierdzeniem odbioru, kandydatów, którzy zostali dopuszczeni
     do postępowania kwalifikacyjnego, o zakończeniu postępowania kwalifikacyjnego, z tym że kandydatów, którzy zo-
     stali dopuszczeni do rozmowy kwalifikacyjnej, zawiadamia także o łącznej liczbie punktów uzyskanej przez każdego
     z nich w postępowaniu kwalifikacyjnym wraz z informacją, czy uzyskana liczba punktów uprawnia do powołania
     kandydata na członka Izby.
     2. Po ustaleniu przez komisję wyników postępowania kwalifikacyjnego w Biuletynie Informacji Publicznej, na stronie
podmiotowej Kancelarii Prezesa Rady Ministrów oraz stronie podmiotowej Urzędu niezwłocznie zamieszcza się wyniki
wraz z łączną liczbą punktów uzyskaną przez tych kandydatów, którzy uzyskali liczbę punktów uprawniającą do powołania
na członka Izby, oraz podaniem imion i nazwisk tych kandydatów, a także imion ich rodziców. Wyniki są udostępniane
przez 6 miesięcy od dnia ich zamieszczenia.
      § 17. 1. Jeżeli dwóch lub więcej kandydatów uzyskało w postępowaniu kwalifikacyjnym taką samą liczbę punktów
umożliwiającą powołanie na członka Izby, minister właściwy do spraw gospodarki powołuje tego kandydata lub tych kan-
dydatów, którzy uzyskali wyższą liczbę punktów z pracy pisemnej, a jeżeli liczba punktów uzyskanych z pracy pisemnej
jest taka sama – kandydatów, którzy uzyskali wyższą liczbę punktów z rozmowy kwalifikacyjnej.
     2. Jeżeli po przeprowadzeniu czynności określonych w ust. 1 nie jest możliwe wyłonienie kandydatów bez przekro-
czenia limitu osób określonego w ogłoszeniu o postępowaniu kwalifikacyjnym, żaden z kandydatów, którzy uzyskali taką
samą liczbę punktów, nie jest powoływany.

                                                       Rozdział 4
        Powołanie komisji kwalifikacyjnej, organizacja jej pracy oraz wymagania wobec członków komisji
     § 18. 1. Minister właściwy do spraw gospodarki powołuje komisję do przeprowadzenia postępowania kwalifikacyjne-
go niezwłocznie po upływie terminu przyjmowania zgłoszeń i podaje do publicznej wiadomości imiona i nazwiska jej
członków. Informację o składzie komisji zamieszcza się w Biuletynie Informacji Publicznej, na stronie podmiotowej Urzę-
du, na stronie podmiotowej urzędu obsługującego ministra właściwego do spraw gospodarki oraz na stronie podmiotowej
Kancelarii Prezesa Rady Ministrów.
    2. Przewodniczącego komisji wyznacza minister właściwy do spraw gospodarki, spośród członków komisji. Człon-
kowie komisji wybierają ze swojego grona wiceprzewodniczącego komisji, który wykonuje zadania przewodniczącego
komisji w przypadku jego nieobecności, oraz sekretarza komisji.
     3. Członkiem komisji nie może być osoba:
1)   kandydująca na członka Izby;
2)   pozostająca w związku małżeńskim albo we wspólnym pożyciu, w stosunku pokrewieństwa lub powinowactwa w linii
     prostej, pokrewieństwa lub powinowactwa w linii bocznej do drugiego stopnia albo związana z tytułu przysposobie-
     nia, opieki lub kurateli z kandydatem;
3)   pozostająca z kandydatem w takim stosunku prawnym lub faktycznym, że może to budzić uzasadnione wątpliwości co
     do jej bezstronności.
      4. Członek komisji, niezwłocznie po zapoznaniu się ze złożonymi zgłoszeniami, składa oświadczenie o braku lub ist-
nieniu okoliczności, o których mowa w ust. 3. W przypadku istnienia okoliczności, o których mowa w ust. 3, minister właś-
ciwy do spraw gospodarki dokonuje zmiany w składzie komisji i uznaje za nieważne dotychczasowe czynności komisji,
jeżeli osoba, o której mowa w ust. 3, brała w nich udział. Komisja w składzie zmienionym powtarza unieważnione czynności,
z wyjątkiem czynności faktycznych, które nie mają wpływu na wynik postępowania kwalifikacyjnego.
     5. Obsługę organizacyjno-techniczną postępowania kwalifikacyjnego zapewnia Urząd Zamówień Publicznych.

    § 19. 1. Komisja obraduje na posiedzeniach. Pierwsze posiedzenie komisji zwołuje minister właściwy do spraw gos-
podarki nie później niż w terminie 7 dni od dnia powołania komisji.
     2. Komisja podejmuje uchwały jednomyślnie, przy obecności co najmniej 2/3 składu komisji. W przypadku nieosiąg-
nięcia jednomyślności przewodniczący komisji zarządza przeprowadzenie imiennego głosowania za pomocą kart do gło-
sowania, przy obecności co najmniej 2/3 składu komisji. W przypadku określonym w zdaniu drugim, uchwały są podej-
mowane większością głosów, a w razie równej liczby głosów rozstrzyga głos przewodniczącego komisji.
     3. Z posiedzenia komisji jest sporządzany protokół, który podpisują członkowie komisji obecni na posiedzeniu.
Dziennik Ustaw                                                   –8–                                                        Poz. 381

                                                             Rozdział 5
                                          Uzupełniające postępowanie kwalifikacyjne
      § 20. Do przeprowadzenia uzupełniającego postępowania kwalifikacyjnego stosuje się odpowiednio przepisy § 2–19.

                                                             Rozdział 6
                                                         Przepis końcowy
      § 21. Rozporządzenie wchodzi w życie po upływie 14 dni od dnia ogłoszenia.1)
"""

if __name__ == '__main__':
    process_text(text_to_process)



