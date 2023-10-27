# railways
Test task from SilkwayTransit

# How to run?
1. Clone the repo
2. ```cd railways```
3. ```python manage.py migrate```

## To run import via simple max_match algo
4. ```python manage.py import_data```
5. ```python manage.py runserver```
6. open localhost:8000 on your web browser

## To run import via simple Trie Max Prefix Mathcing algo
7. ```python manage.py clean_db``` (If you ran first method before)
8. ```python manage.py import_trie```
5. ```python manage.py runserver```
6. open localhost:8000 on your web browser