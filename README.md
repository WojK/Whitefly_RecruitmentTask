# Whitefly - Zadanie rekrutacyjne

## Opis rozwiązania 

W ramach zadania zostały przygotowane dwa serwisy z wykorzystaniem frameworku Flask oraz FastAPI. Oba serwisy implementują dwa formularze przyjmujące opinie użytkowników, które trafiają do relacyjnej bazy danych.  Jaką bazę danych wybrałem SQLite ze względu na szybkość i prostotę rozwiązania. Baza danych obsługiwana jest poprzez mapowanie obiektowo-relacyjne za pomocą narzędzia SQLAlchemy. 
Request przyjęcia formularza w pierwszym przypadku jest obsługiwany w sposób synchroniczny, co oznacza, że dane z formularza zapisywane są do bazy danych i zwracany jest wynikowy Response z przekierowaniem na stronę główną. W przypadku drugiego formularza zadanie obsługiwane jest w sposób asynchroniczny. Zadanie zapisu do bazy danych dodawane jest do kolejki zadań za pomocą Celery gdzie brokerem jest Redis. Do obsługi zadań dodanych do kolejki w systemie zostaje uruchomiony jeden demon, który pracuje jako worker Celery, monitorując kolejkę i przetwarzając zadania w tle.

## Deploy 

Obie aplikacje zostały wdrożone na platformie DigitalOcean w tej samej architekturze systemowej (Ubuntu 24.04 (LTS) x64, 512MB / 1 CPU, 10GB).  Rozwiązanie we Flask opiera się na zastosowaniu uWSGI i Nginx, które pełni rolę reverse proxy. FastAPI działa na ASGI i również z Nginx. 

## Testy 

Do przeprowadzenia testów wykorzystano platformę Loader.io. Obiektem testów było odrębne sprawdzenie wydajności żądań POST, obsługujących formularze. Celem było sprawdzenie czy zastosowanie systemu kolejkowego w przypadku asynchronicznego rozwiązania przynosi widoczne korzyści. Parametry testów to 15s trwania testu podczas którego serwis miał obsłużyć 1000 żądań POST. Podsumowanie testów przedstawia poniższa tabela:

|                   | FastApi |       | Flask |       |
|-------------------|---------|-------|-------|-------|
|                   | Sync    | Async | Sync  | Async |
| Avg Response Time | 215ms   | 220ms | 230ms | 226ms |

## Wnioski

W przypadku tak prostego zadania jak zapisanie danych do lokalnie przechowywanej plikowej bazy danych nie są widoczne korzyści z zastosowania systemu kolejkowego, ze względu na nieznaczne różnicę między średnim czasem otrzymania odpowiedzi od aplikacji. Gdyby jednak zadanie było bardziej kosztowne obliczeniowo, albo gdyby system musiałby komunikować się z bazą danych, która nie jest przechowywana lokalnie i czas połączenia byłby znaczący przypuszczam, że asynchroniczne obsługiwane takie zadania miałoby znaczący wpływ na wydajność systemu.

## Adresy aplikacji

FastApi: http://164.92.182.123

Flask:   http://165.232.116.16 
