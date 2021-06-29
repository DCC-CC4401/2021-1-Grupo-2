# Pichangapp

![PichangApp](pichapp/static/pichapp/NavPortada.png)

About
- PichanApp is the app to make sport encounters in Chile in a easy and fast way.

Running The Aplication
- Install dependencies (use Pipfile).
- Run `python manage.py migrate`.
- To load sports use: `python manage.py loaddata Sports`
- Run the app with: `python manage.py runserver`.

Adding new Sports
- Add them to `Sports.json`.
- Add the sport image to `static/pichapp/deportes`.
- Run `python manage.py loaddata Sports`.


