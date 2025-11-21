import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# --- KONFIGURACJA ---
HISTORY_FILE = "history.csv"
PASSING_SCORE = 80  # Procent

# --- BAZA PYTAŃ (15 pytań) ---
QUESTIONS_DB = [
    {
        "question": "Co to jest Phishing?",
        "options": [
            "Metoda łowienia ryb w internecie",
            "Rodzaj wirusa komputerowego niszczącego dysk",
            "Podszywanie się pod inną osobę/instytucję w celu wyłudzenia danych",
            "Legalna technika marketingowa"
        ],
        "answer": "Podszywanie się pod inną osobę/instytucję w celu wyłudzenia danych",
        "explanation": "Phishing to technika socjotechniczna, w której przestępcy próbują oszukać ofiarę, aby podała poufne informacje."
    },
    {
        "question": "Jakie hasło jest najsilniejsze?",
        "options": [
            "Admin123",
            "Kasia1990",
            "M0j3_B@rdz0_Trudn3_H@sl0!",
            "12345678"
        ],
        "answer": "M0j3_B@rdz0_Trudn3_H@sl0!",
        "explanation": "Silne hasło powinno być długie i zawierać małe/wielkie litery, cyfry oraz znaki specjalne."
    },
    {
        "question": "Co oznacza skrót RODO?",
        "options": [
            "Rozporządzenie o Ochronie Danych Osobowych",
            "Rządowa Organizacja Danych Osobistych",
            "Rejestr Ochrony Danych Obywatelskich",
            "Ruch Oporu Danych Osobistych"
        ],
        "answer": "Rozporządzenie o Ochronie Danych Osobowych",
        "explanation": "RODO to unijne rozporządzenie regulujące zasady przetwarzania danych osobowych."
    },
    {
        "question": "Znalazłeś nieznany pendrive na parkingu firmowym. Co robisz?",
        "options": [
            "Podłączam do komputera, żeby sprawdzić czyj jest",
            "Zanoszę go do działu IT lub ochrony",
            "Wyrzucam do kosza",
            "Zabieram do domu"
        ],
        "answer": "Zanoszę go do działu IT lub ochrony",
        "explanation": "Nigdy nie podłączaj nieznanych nośników! Mogą zawierać złośliwe oprogramowanie."
    },
    {
        "question": "Co to jest uwierzytelnianie dwuskładnikowe (2FA)?",
        "options": [
            "Logowanie za pomocą dwóch różnych haseł",
            "Wymóg podania loginu i hasła",
            "Logowanie z użyciem hasła i drugiego składnika (np. kod SMS, aplikacja)",
            "Logowanie na dwóch urządzeniach jednocześnie"
        ],
        "answer": "Logowanie z użyciem hasła i drugiego składnika (np. kod SMS, aplikacja)",
        "explanation": "2FA znacząco zwiększa bezpieczeństwo, wymagając czegoś, co znasz (hasło) i czegoś, co masz (telefon/klucz)."
    },
    {
        "question": "Otrzymałeś e-mail od 'Prezesa' z prośbą o pilny przelew na nowe konto. Co robisz?",
        "options": [
            "Natychmiast wykonuję przelew, to polecenie służbowe",
            "Odpisuję na maila z pytaniem o szczegóły",
            "Weryfikuję prośbę innym kanałem (np. telefonicznie) u nadawcy",
            "Ignoruję wiadomość"
        ],
        "answer": "Weryfikuję prośbę innym kanałem (np. telefonicznie) u nadawcy",
        "explanation": "To typowy atak 'CEO Fraud'. Zawsze weryfikuj nietypowe prośby finansowe inną drogą komunikacji."
    },
    {
        "question": "Czy HTTPS w pasku adresu oznacza, że strona jest w 100% bezpieczna?",
        "options": [
            "Prawda",
            "Fałsz"
        ],
        "answer": "Fałsz",
        "explanation": "HTTPS oznacza tylko szyfrowane połączenie. Strona nadal może być fałszywa (phishingowa) lub zawierać wirusy."
    },
    {
        "question": "Co to jest Ransomware?",
        "options": [
            "Program do czyszczenia pamięci RAM",
            "Oprogramowanie szpiegujące",
            "Złośliwe oprogramowanie szyfrujące dane dla okupu",
            "Darmowy program antywirusowy"
        ],
        "answer": "Złośliwe oprogramowanie szyfrujące dane dla okupu",
        "explanation": "Ransomware blokuje dostęp do systemu lub plików i żąda opłaty za ich odblokowanie."
    },
    {
        "question": "Dlaczego należy blokować ekran komputera odchodząc od biurka?",
        "options": [
            "Żeby oszczędzać prąd",
            "Żeby nikt niepowołany nie miał dostępu do danych",
            "Żeby monitor się nie wypalił",
            "Nie trzeba blokować, w biurze są sami swoi"
        ],
        "answer": "Żeby nikt niepowołany nie miał dostępu do danych",
        "explanation": "Pozostawienie odblokowanego komputera to ryzyko wycieku danych lub nieautoryzowanych działań na Twoim koncie."
    },
    {
        "question": "Jak często należy robić kopie zapasowe (backup) ważnych danych?",
        "options": [
            "Raz na rok",
            "Tylko gdy komputer zaczyna wolno działać",
            "Regularnie (np. codziennie lub w czasie rzeczywistym)",
            "Nigdy, dyski są bezawaryjne"
        ],
        "answer": "Regularnie (np. codziennie lub w czasie rzeczywistym)",
        "explanation": "Regularny backup to jedyny pewny sposób na odzyskanie danych po awarii lub ataku ransomware."
    },
    {
        "question": "Socjotechnika (Social Engineering) polega na:",
        "options": [
            "Włamywaniu się do serwerów przez luki w kodzie",
            "Manipulowaniu ludźmi w celu uzyskania informacji",
            "Tworzeniu portali społecznościowych",
            "Naprawianiu sprzętu komputerowego"
        ],
        "answer": "Manipulowaniu ludźmi w celu uzyskania informacji",
        "explanation": "Najsłabszym ogniwem bezpieczeństwa jest często człowiek. Socjotechnika atakuje ludzką psychikę, a nie technologię."
    },
    {
        "question": "Czy publiczne, otwarte sieci Wi-Fi (np. w kawiarni) są bezpieczne do logowania się do banku?",
        "options": [
            "Prawda",
            "Fałsz"
        ],
        "answer": "Fałsz",
        "explanation": "W otwartych sieciach ruch może być łatwo podsłuchany. Należy używać VPN lub danych komórkowych."
    },
    {
        "question": "Co zrobisz, gdy przeglądarka poinformuje Cię, że Twoje hasło wyciekło?",
        "options": [
            "Ignoruję to, to pewnie błąd",
            "Zmieniam to hasło natychmiast w każdym serwisie, gdzie go używam",
            "Zmieniam przeglądarkę",
            "Piszę skargę do dostawcy internetu"
        ],
        "answer": "Zmieniam to hasło natychmiast w każdym serwisie, gdzie go używam",
        "explanation": "Wyciek hasła oznacza, że przestępcy mogą mieć do niego dostęp. Należy je niezwłocznie zmienić."
    },
    {
        "question": "Czym jest 'Menedżer Haseł'?",
        "options": [
            "Osobą w dziale IT resetującą hasła",
            "Programem do bezpiecznego przechowywania i generowania haseł",
            "Kartką przyklejoną do monitora",
            "Funkcją w BIOSie"
        ],
        "answer": "Programem do bezpiecznego przechowywania i generowania haseł",
        "explanation": "Menedżery haseł pozwalają używać unikalnych, skomplikowanych haseł do każdego serwisu bez konieczności ich zapamiętywania."
    },
    {
        "question": "Aktualizacje oprogramowania należy instalować:",
        "options": [
            "Jak najszybciej, gdyż często łatają luki bezpieczeństwa",
            "Tylko gdy dodają nowe, ciekawe funkcje",
            "Raz na kilka lat",
            "Nigdy, aktualizacje psują komputer"
        ],
        "answer": "Jak najszybciej, gdyż często łatają luki bezpieczeństwa",
        "explanation": "Nieaktualne oprogramowanie jest podatne na znane ataki. Aktualizacje to podstawa higieny cyfrowej."
    }
]

# --- FUNKCJE POMOCNICZE ---

def init_session():
    """Inicjalizacja stanu sesji."""
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = None
    if 'quiz_started' not in st.session_state:
        st.session_state['quiz_started'] = False
    if 'quiz_questions' not in st.session_state:
        st.session_state['quiz_questions'] = []
    if 'current_q_index' not in st.session_state:
        st.session_state['current_q_index'] = 0
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False
    if 'last_answer_correct' not in st.session_state:
        st.session_state['last_answer_correct'] = None
    if 'quiz_finished' not in st.session_state:
        st.session_state['quiz_finished'] = False

def start_quiz(name):
    """Rozpoczęcie quizu: zapisanie imienia i wylosowanie pytań."""
    st.session_state['user_name'] = name
    st.session_state['quiz_started'] = True
    # Losowanie 10 pytań z bazy
    st.session_state['quiz_questions'] = random.sample(QUESTIONS_DB, 10)
    st.session_state['current_q_index'] = 0
    st.session_state['score'] = 0
    st.session_state['submitted'] = False
    st.session_state['quiz_finished'] = False

def save_score(name, score):
    """Zapis wyniku do pliku CSV."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[name, score, date_str]], columns=['Imie_Nazwisko', 'Wynik', 'Data'])
    
    if not os.path.isfile(HISTORY_FILE):
        new_data.to_csv(HISTORY_FILE, index=False)
    else:
        new_data.to_csv(HISTORY_FILE, mode='a', header=False, index=False)

def load_leaderboard():
    """Wczytanie i sortowanie tablicy wyników."""
    if not os.path.isfile(HISTORY_FILE):
        return pd.DataFrame(columns=['Imie_Nazwisko', 'Wynik', 'Data'])
    
    df = pd.read_csv(HISTORY_FILE)
    # Sortowanie malejąco po wyniku
    df = df.sort_values(by='Wynik', ascending=False).head(10)
    return df

# --- INTERFEJS APLIKACJI ---

st.set_page_config(page_title="Quiz Cyberbezpieczeństwa", page_icon="🔒")
init_session()

st.title("🔒 Quiz Wiedzy o Cyberbezpieczeństwie")

# 1. EKRAN LOGOWANIA
if not st.session_state['quiz_started']:
    st.markdown("""
    Witaj w szkoleniu z cyberbezpieczeństwa!
    
    Przed Tobą **10 pytań**. Aby otrzymać certyfikat, musisz uzyskać co najmniej **80%** poprawnych odpowiedzi.
    
    Proszę podaj swoje Imię i Nazwisko, aby rozpocząć.
    """)
    
    name_input = st.text_input("Imię i Nazwisko")
    
    if st.button("Rozpocznij Quiz"):
        if name_input.strip():
            start_quiz(name_input.strip())
            st.rerun()
        else:
            st.error("Proszę wprowadzić Imię i Nazwisko.")

# 2. EKRAN QUIZU
elif not st.session_state['quiz_finished']:
    q_index = st.session_state['current_q_index']
    questions = st.session_state['quiz_questions']
    total_q = len(questions)
    current_q = questions[q_index]
    
    # Pasek postępu
    progress = (q_index / total_q)
    st.progress(progress)
    st.caption(f"Pytanie {q_index + 1} z {total_q}")
    
    st.subheader(current_q["question"])
    
    # Formularz odpowiedzi
    # Używamy klucza widgetu, aby zresetować wybór przy nowym pytaniu, ale tutaj
    # musimy obsłużyć to ostrożnie. Radio button w Streamlit trzyma stan.
    # Najprościej: unikalny klucz dla każdego pytania.
    answer = st.radio(
        "Wybierz odpowiedź:",
        current_q["options"],
        key=f"q_{q_index}",
        disabled=st.session_state['submitted']
    )
    
    # Przycisk Zatwierdź
    if not st.session_state['submitted']:
        if st.button("Zatwierdź odpowiedź"):
            st.session_state['submitted'] = True
            if answer == current_q["answer"]:
                st.session_state['score'] += 1
                st.session_state['last_answer_correct'] = True
            else:
                st.session_state['last_answer_correct'] = False
            st.rerun()
            
    # Wyświetlanie wyniku i przycisk Dalej
    else:
        if st.session_state['last_answer_correct']:
            st.success("✅ Poprawna odpowiedź!")
        else:
            st.error(f"❌ Błąd! Poprawna odpowiedź to: {current_q['answer']}")
        
        st.info(f"ℹ️ Wyjaśnienie: {current_q['explanation']}")
        
        if q_index < total_q - 1:
            if st.button("Następne pytanie"):
                st.session_state['current_q_index'] += 1
                st.session_state['submitted'] = False
                st.rerun()
        else:
            if st.button("Zakończ i zobacz wyniki"):
                st.session_state['quiz_finished'] = True
                save_score(st.session_state['user_name'], st.session_state['score'])
                st.rerun()

# 3. EKRAN WYNIKÓW
else:
    score = st.session_state['score']
    total = len(st.session_state['quiz_questions'])
    percentage = (score / total) * 100
    
    st.divider()
    st.header(f"Koniec Quizu, {st.session_state['user_name']}!")
    st.metric(label="Twój Wynik", value=f"{score} / {total}", delta=f"{percentage}%")
    
    if percentage >= PASSING_SCORE:
        st.balloons()
        st.success(f"""
        ### 🎓 GRATULACJE!
        
        **Certyfikat Ukończenia Szkolenia Cyberbezpieczeństwa**
        
        Niniejszym zaświadcza się, że:
        **{st.session_state['user_name']}**
        
        Ukończył(a) szkolenie z wynikiem pozytywnym.
        """)
    else:
        st.warning(f"Niestety, nie udało się uzyskać certyfikatu (wymagane {PASSING_SCORE}%). Spróbuj ponownie!")
    
    st.divider()
    
    # Leaderboard
    st.subheader("🏆 Top 10 Pracowników")
    leaderboard = load_leaderboard()
    if not leaderboard.empty:
            # st.dataframe wymaga pyarrow, który nie jest dostępny. Używamy st.columns.
        cols = st.columns([3, 1, 2])
        cols[0].markdown("**Imię i Nazwisko**")
        cols[1].markdown("**Wynik**")
        cols[2].markdown("**Data**")
        
        for _, row in leaderboard.iterrows():
            c = st.columns([3, 1, 2])
            c[0].write(row['Imie_Nazwisko'])
            c[1].write(f"{row['Wynik']}")
            c[2].write(row['Data'])
    else:
        st.write("Brak wyników w historii.")
        
    if st.button("Rozpocznij nowy quiz"):
        # Reset stanu
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- INSTRUKCJA URUCHOMIENIA ---
# 1. Zainstaluj biblioteki: pip install streamlit pandas
# 2. Uruchom aplikację: streamlit run cyber_quiz_app.py
