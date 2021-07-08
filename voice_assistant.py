import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import getpass

stop = [True]

opts = {
    "name": (
        'sara', 'sarai', 'sar', 'siri', 'zara', 'car', 'zaraz', 'katar', 'sam', 'para', 'sasa', 'soro', 'szare',
        'stara',
        'szara'),

    "show": ('znajdź', 'włącz', 'pokaż', 'w jakim roku', 'w którym roku', 'proszę pokazać', 'otwórz',
             'odpal', 'uruchom', 'wyszukaj na necie', 'zapuść', 'wejdź do', 'wejdź na', 'przejdź na',
             'przejdź do', 'wyszukaj', 'prosę wyszukać', 'proszę otwórzyć', 'proszę odpalić', 'proszę uruchomic'),

    "programscut": ('otwórz program', 'odpal program', 'uruchom program',
                    'proszę otwórzyć program', 'proszę odpalić program', 'proszę uruchomic program', 'program'),

    "cut": (),

    "cmds": {
        "hello": ('cześć', 'hej', 'hejka'),

        "my_name": ('jak się nazywasz', 'jak masz na imię', 'powiedź swoję imię'),

        "time": ('która godzina', 'jaka godzina', 'powiedź czas', 'co tam z czasem', 'czas', 'godzina'),

        "day": ('który dzisiaj dzień', 'jaki dzisiaj dzień', 'powiedź dzień', 'który teraz dzień', 'jaki teraz dzień'),

        "year": ('który dzisiaj rok', 'jaki dzisiaj rok', 'powiedź rok', 'który teraz rok', 'jaki teraz rok'),

        "mount": ('który dzisiaj miesiąc', 'jaki dzisiaj miesiąc', 'powiedź miesiąc', 'który teraz miesiąc', 'jaki teraz miesiąc'),

        "date": ('dzisiejsza data', 'jaka dzisiaj data', 'powiedź datę', 'która teraz data', 'jakia teraz data', 'jaka jest data', 'powiedź dzisiejszą datę'),

        "mood": ('co słychać', 'jak się masz', 'co tam', 'jak tam'),

        "programs": ('otwórz program', 'odpal program', 'uruchom program',
                     'proszę otwórzyć program', 'proszę odpalić program', 'proszę uruchomic program', 'program'),

        "skils": ('co ty umiesz', 'powiedź swoję możliwości', 'co ty morzesz zrobić', 'pokaż swoję możliwości',
                  'jakie masz komande', 'opowiedź o swoich umiejęntnościach'),

        "weather": (
            'jaka pogoda', 'jaka jest pogoda', 'powiedź jaka jest pogoda', 'powiedź pogodę', 'powiedź jaka pogoda',
            'pogoda', 'temperatura', 'powiedź temperaturę'),

        "open_web": (
            'otwórz przeglądarkę', 'odpal przeglądarkę', 'uruchom przeglądarkę', 'zapuść przeglądarkę', 'otwórz google',
            'przejdź do googla', 'odpal google', 'uruchom google', 'zapuść googla', 'wejdź do googla', 'otwórz chrom',
            'odpal chroma',
            'uruchom google chrom', 'zapuść googl chrom'),

        "quit": ('koniec', 'zakończ', 'stop', 'stap', 'wylącz się'),

        "facebook": ('otwórz facebook', 'odpal facebook', 'wejdź na facebook', 'przejdź do facebooka', 'facebook'),

        "weather_web": ('wyszukaj pogodę', 'pokaż jaka jest pogoda', 'pokaż pogodę', 'pokaż temperaturę'),

        "youtube": ('otwórz youtube', 'odpal youtube', 'przejdź na youtube', 'wejdź do youtube', 'youtube'),

        "youtube_song": ('zagraj piosenkę', 'włącz piosenkę', 'włącz video'),

        "news": ('pokaż mi nowiny', 'włącz mi nowiny', 'pokaż listę nowin', 'włącz listę nowin', 'nowiny',
                 'pokaż mi aktualności', 'włącz mi aktualności', 'pokaż listę aktualności', 'włącz listę aktualności',
                 'aktualności'),

        "wiki": ('otwórz wikipediję', 'odpal wikipedję', 'przejdź na wikipedia', 'wejdź do wikipedii', 'wikipedia')

    }

}

# Funkcja która daję głos temu assystentu.
def assistant_voice(phrase):
    speak_engine = pyttsx3.init()  # Inicializacja biblioteki.
    speak_engine.setProperty('rate', 170)  # Ustawienie szybkości głosu.
    voices = speak_engine.getProperty('voices')  # Pobieranie szczegółów aktualnego głosu.
    speak_engine.setProperty('voice', voices[1].id)  # Zmiana indeksu, zmiana głosów.
    speak_engine.say(phrase)  # Kolejkuje polecenie wypowiedzenia frazy.
    speak_engine.runAndWait()  # Blokuje podczas przetwarzania wszystkich oczekujących poleceń. Prawidłowo wywołuje wywołania zwrotne powiadomień silnika.
    speak_engine.stop()  # Zatrzymuje bieżącą wypowiedź i czyści kolejkę poleceń.

# Funkcja rozpoznająca głos.
def listen(r, audio):
    try:
        speech = r.recognize_google(audio, language="pl").lower()  # speech przyjmuję rozpoznany tekst
        print("Powiedziałes: ", speech)
        if speech.startswith(opts["name"]):  # usuwam z speech imię asystęnta
            command = speech
            command1 = speech
            for x in opts['name']:
                command = command.replace(x, "").strip()
                command1 = command1.replace(x, "").strip()
            if command1.startswith(opts["show"]):
                for x1 in opts['show']:
                    command1 = command1.replace(x1, "").strip()
                print("Rozpoznane polecenie: ", command1)
                command1 = recognize_command(command1)
                openinweb(command1, speech)
            else:
                print("Rozpoznane polecenie: ", command)
                command = recognize_command(command)
                execute_command(command['command'])
        else:
            command = speech
            command = recognize_command(command)
            standart_command(command['command'])
    except sr.UnknownValueError:
        print("Nie udało się rozpoznać!")
    except sr.RequestError as e:
        print("Nieznany błąd!")

# Funkcja porównania rozmytego
def recognize_command(command1):
    RC = {'command': '', 'percent': 80}
    for c, v in opts['cmds'].items():
        for x in v:
            pr = fuzz.WRatio(command1,
                             x)  # Porównanie które uwzględnia wielkość liter i znaki interpunkcyjne (nie dzielące ciągu)
            if pr > RC['percent']:
                RC['command'] = c
                RC['percent'] = pr

    return RC

# Funkcja z podstawowymi poleceniami, które nie potrzebują zwrotu przez imię assystenta
def standart_command(command):
    if command == 'hello':
        q1 = ["witam", 'Dzień dobry']
        x1 = random.choice(q1)
        assistant_voice(x1)

    elif command == 'my_name':
        q2 = ["nazywam się Sara", 'Sara']
        x2 = random.choice(q2)
        assistant_voice(x2)

    # elif command == 'quit':
    #     a = ['dowidzenia', 'do usłyszenia', 'dowidzenia i miłego dnia']
    #     b = random.choice(a)
    #     assistant_voice(b)
    #     stop[0] = False
    #     exit()

    else:
        print('Proszę zwracać się do mnie po imieniu.')

# Dodatkowa funkcja do rozpoznania głosu
def listen_weather():
    mic1 = sr.Microphone()
    r1 = sr.Recognizer()
    with mic1 as source:
        audio1 = r1.listen(source)
    try:
        city = r1.recognize_google(audio1, language="pl").lower()
        # print("Powiedziłes: ", city)
        return city
    except sr.UnknownValueError:
        return 'error'
    except sr.RequestError:
        return 'error'

# Funkcja która korzysta z przegłądarki i otwiera programy z pulpitu
def openinweb(command1, speech):
    if command1['command'] == 'programs':
        try:
            # czyścimy polecenie, żeby zdobyć nazwę programu
            for x in opts['name']:
                speech = speech.replace(x, "").strip()
            for x1 in opts['programscut']:
                speech = speech.replace(x1, "").strip()

            user = getpass.getuser()
            os.startfile('C:\\Users\\' + user + '\\Desktop\\' + speech)  # startuję program
            q1 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram program',
                  'Już uruchamiam program', 'Otwieram program', 'Uruchamiam program',
                  'Już otwieram' + speech, 'Już uruchamiam' + speech, 'Już otwieram program' + speech,
                  'Już uruchamiam program' + speech, 'Otwieram program' + speech, 'Uruchamiam program' + speech]
            x1 = random.choice(q1)
            assistant_voice(x1)
        except:
            q2 = ['Nie rozumiem, proszę powtórzyc', 'Nie rozumiem nazwy programu, proszę powtórzyć całe polecenie',
                  'Przepraszam, ale nie zrozumiałam jaki program mam uruchomić, więc proszę powtórzyć całe polecenie',
                  'Nie znam programu o nazwie' + speech + '. Proszę powtórzyć całe polecenie',
                  'Coś poszło nie tak, proszę powtórzyć całe polecenie', 'Nie znalażłam program o nazwie: ' + speech + ', albo nie mam do niego dostępu']
            x2 = random.choice(q2)
            assistant_voice(x2)

    elif command1['command'] == 'open_web':
        url = 'https://google.com'
        q3 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram przeglądarkę',
              'Już uruchamiam przeglądarkę',
              'Otwieram przeglądarkę', 'Uruchamiam przeglądarkę', 'Otwieram googla', 'Uruchamiam googla']
        x3 = random.choice(q3)
        assistant_voice(x3)
        webbrowser.open(url)

    elif command1['command'] == 'wiki':
        url = 'https://pl.wikipedia.org'
        q4 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram wikipedje', 'Już uruchamiam wikipedje',
              'Otwieram wikipedje', 'Uruchamiam wikipedje', 'Otwieram wikipedje', 'Uruchamiam wikipedje']
        x4 = random.choice(q4)
        assistant_voice(x4)
        webbrowser.open(url)

    elif command1['command'] == 'youtube':
        url = 'https://youtube.com'
        q5 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram youtube', 'Już uruchamiam youtube',
              'Otwieram youtube', 'Uruchamiam youtube', 'Otwieram youtube', 'Uruchamiam youtube']
        x5 = random.choice(q5)
        assistant_voice(x5)
        webbrowser.open(url)

    elif command1['command'] == 'facebook':
        url = 'https://facebook.com'
        q6 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram facebook', 'Już uruchamiam facebook',
              'Otwieram facebook', 'Uruchamiam facebook', 'Otwieram facebook', 'Uruchamiam facebook']
        x6 = random.choice(q6)
        assistant_voice(x6)
        webbrowser.open(url)

    elif command1['command'] == 'news':
        url = 'https://news.google.com/topstories?hl=pl&gl=PL&ceid=PL:pl'
        q6 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram nowiny', 'Już uruchamiam nowiny',
              'Otwieram nowiny', 'Uruchamiam nowiny', 'Otwieram nowiny', 'Uruchamiam nowiny',
              'Już otwieram aktualności',
              'Już uruchamiam aktualności', 'Otwieram aktualności', 'Uruchamiam aktualności', 'Otwieram aktualności',
              'Uruchamiam aktualności', 'Już pokazuję', 'Już pokazuję nowiny', 'Już pokazuję aktualności',
              'Pokazuję nowiny', 'Pokazuję aktualności']
        x6 = random.choice(q6)
        assistant_voice(x6)
        webbrowser.open(url)

    elif command1['command'] == 'youtube_song':
        for x in opts['name']:
            speech = speech.replace(x, "").strip()
        for x1 in opts['show']:
            speech = speech.replace(x1, "").strip()

        q7 = ['Już otwieram', 'Już uruchamiam', 'Już to robię']
        x7 = random.choice(q7)
        assistant_voice(x7)
        url = 'https://www.youtube.com/results?search_query=' + speech
        webbrowser.open(url)

    else:
        for x in opts['name']:
            speech = speech.replace(x, "").strip()
        for x1 in opts['show']:
            speech = speech.replace(x1, "").strip()
        url = 'https://google.com/search?q=' + speech
        q8 = ['Już szukam', 'Proszę chilkę poczekać', 'Już to robię', 'Zaczynam szukać']
        x8 = random.choice(q8)
        assistant_voice(x8)
        webbrowser.open(url)


# Funkcja wypełniająca naszę polecenia
def execute_command(command):
    if command == 'hello':
        q1 = ["witam", 'Dzień dobry']
        x1 = random.choice(q1)
        assistant_voice(x1)

    elif command == 'my_name':
        q2 = ["nawet nie wiem , chyba Sara", 'serio ? przed chwilią powiedziałeś Sara']
        x2 = random.choice(q2)
        assistant_voice(x2)

    elif command == 'skils':
        assistant_voice('mogę powiedzieć czas, pogodę, umiem korzystać z przeglądarki,'
                        ' uruchamiać aplikację z pulpitu i jeszcze kilka rzeczy')
        assistant_voice('aby wyłączyć mnie powiedź na przykład koniec')
        assistant_voice('mam nadzieję że będę w stanie ci pomóc')

    elif command == 'mood':
        q3 = ["morze być, dziękuję", 'wszystko dobrze, dziękuję', 'wszystko jest okej, dziękuję']
        x3 = random.choice(q3)
        assistant_voice(x3)

    elif command == 'time':
        now = datetime.datetime.now()
        assistant_voice("Teraz " + str(now.hour) + ":" + str(now.minute))

    elif command == 'day':
        now = datetime.datetime.now()
        if now.weekday() == 0:
            assistant_voice("Dzisiaj" + str(now.day) + ", poniedziałek")
        elif now.weekday() == 1:
            assistant_voice("Dzisiaj" + str(now.day) + ", wtorek")
        elif now.weekday() == 2:
            assistant_voice("Dzisiaj" + str(now.day) + ", środa")
        elif now.weekday() == 3:
            assistant_voice("Dzisiaj" + str(now.day) + ", czwartek")
        elif now.weekday() == 4:
            assistant_voice("Dzisiaj" + str(now.day) + ", piątek")
        elif now.weekday() == 5:
            assistant_voice("Dzisiaj" + str(now.day) + ", sobota")
        elif now.weekday() == 6:
            assistant_voice("Dzisiaj" + str(now.day) + ", niedziela")

    elif command == 'year':
        now = datetime.datetime.now()
        assistant_voice("Dzisiaj " + str(now.year) + " rok")

    elif command == 'mount':
        now = datetime.datetime.now()
        assistant_voice("Dzisiaj " + str(now.month) + " miesiąc")

    elif command == 'date':
        now = datetime.datetime.now()
        assistant_voice("Dzisiaj " + str(now.year) + " rok, " + str(now.month) + ' miesiąc' + str(now.day) + 'dzień')

    elif command == 'open_web':
        q4 = ['Już otwieram', 'Już uruchamiam', 'Już to robię', 'Już otwieram przeglądarkę',
              'Już uruchamiam przeglądarkę',
              'Otwieram przeglądarkę', 'Uruchamiam przeglądarkę', 'Otwieram googla', 'Uruchamiam googla']
        x4 = random.choice(q4)
        assistant_voice(x4)
        webbrowser.open('https://google.com')

    elif command == 'weather':
        try:
            assistant_voice("powiedz w jakim miaście")
            city = listen_weather()
            config_dict = get_default_config()  # dostęp do konfiguracji
            config_dict['language'] = 'pl'  # zmiana języka
            owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa', config_dict)  # podaję swój darmowy lucz API
            mgr = owm.weather_manager() # Menedżer obiektów zapewniający pełny interfejs do OWM Weather API
            obs = mgr.weather_at_place(city)  # szukam odpowiednie miasto
            w = obs.weather  # pobieram dane pogody
            k = w.detailed_status  # Wybieram szczegóły np. pochmurno
            x = w.temperature(unit='celsius')  # pobieram temperaturę
            print(
                'W %s jest %s. Temperatura = %0.2f, maksymalna temperatura = %0.2f, a minimalna = %0.2f Stopni Celsjusza' %
                (city, k, x['temp'], x['temp_max'], x['temp_min']))
            assistant_voice(
                'W tej chwili w %s jest %s. Temperatura wynosi %0.2f Stopni Celśjusza' %
                (city, k, x['temp']))

        except:
            return assistant_voice('nie znam tego miasta, proszę sprubować powturzyć pytanie')

    elif command == 'quit':
        a = ['dowidzenia', 'do usłyszenia', 'dowidzenia i miłego dnia']
        b = random.choice(a)
        assistant_voice(b)
        quit()

    else:
        print('nie rozumiem polecenia')
        assistant_voice('nie rozumiem polecenia')

def quit():
    stop[0] = False
    exit()

if __name__ == '__main__':
    mic = sr.Microphone()  # Dostęp do mikrofonu systemowego
    r = sr.Recognizer()  # Tworzenie instancji rozpoznawania
    with mic as source:
        r.pause_threshold = 1  # Reprezentuje minimalną długość ciszy (w sekundach), która jest rejestrowana jako koniec frazy.
        r.adjust_for_ambient_noise(source,
                                   duration=1)  # Metoda odczytuje pierwszą sekundę ze strumienia i kalibruje aparat rozpoznawania do poziomu szumów audio. duration - czas (standartowo 1 sekunda)
        print('Witam, proszę się przywitać. Muszę nagrać twoję tło, żeby lepiej cię rozumieć.')
        assistant_voice('Witam, proszę przywitać się, muszę nagrać twoję tło, żeby lepiej cie rozumieć.')
        audio = r.listen(
            source)  # Metoda przyjmuje źródło dźwięku jako pierwszy argument i zapisuje dane wejściowe ze źródła do momentu wykrycia ciszy.

    print('W czym mogę pomóc?')
    assistant_voice('W czym mogę pomóc?')

    stop_listening = r.listen_in_background(mic,
                                            listen)  # Zacznij słuchać w tle, tworzy nowy strumień do przepisywania fraz ze źródła
    while stop[0]:
        time.sleep(
            0.2)  # już nie słuchamy, chociaż wątek w tle może nadal działać przez sekundę lub dwie podczas czyszczenia i zatrzymywania


