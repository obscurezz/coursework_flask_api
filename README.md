# Backend for coursework "Developing Flask API"

## Describe
* Installing requirements
```
pip install -r requirements.txt
```
* DEV environment
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```
* Creating security settings
```
python create_security.py
```
* Creating (recreating) tables
```
python create_tables.py
```
* Creating test data with fixtures
```
python load_fixtures.py
```
* Launching the application
```
python run.py
```
* or
```
flask run
```
***
## Views
`/movies/` returns all movies   
`/movies/?page=1` returns first page of all movies  
`/movies/?status=NEW` returns all movies ordered by year    
`/movies/?page=1&status=NEW` returns first page of all movies ordered by year   
`/movies/1` returns single movie by id
***
`/genres/` returns all genres   
`/genres/1` returns single genre by id
***
`/directors/` returns all directors   
`/directors/1` returns single director by id
***
```
WORK IN PROGRESS...
```