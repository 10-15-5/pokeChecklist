<h1 style="text-align:center;">PokeChecklist</h1>

Computer Science project to display pokemon needed to catch.

## Current Capabilities:

- Keep track of Pokemon you have caught and what Pokemon you need to catch
- Displays charts of how many Pokemon you have caught and of what type you've caught most
- Click on Pokemon pictures to see a detailed view of their stats and supereffective types

## Future Capabilities:
Home Page:
- Add Pokemon for each generation.
- Search field to find Pokemon easily

Graphs:
- Redesign page to be better layed out
- Add more graphs and information

Wiki:
- More details about each Pokemon
- Select box to choose a game that will display the route/area to find the Pokemon


## How to Install

- Clone Codebase
- Create Virtual Environment in project dir<br>
    `python -m venv .venv`
- Run virtual environment<br>
    - Windows<br>
    `.venv\Scripts\activate.bat`
    - Linux<br>
    `source .venv/bin/activate`
- Pip install requirements<br>
    `pip install -r requirements.txt`
- Have django-sass watch files and recompile them as they change (Only needed if you want to make changes to the code)<br>
    `python manage.py sass static/scss/ static/css/ --watch`
- Run server<br>
    `python manage.py runserver`