# Strecken-Informationssystem

## Dependencies

[requirements.txt](./requirements.txt)

## Anleitung

### Installation
1. Git Repository clonen
2. Mittels Command Line ins Root Verzeichnis `Strecken` wechseln
3. Virtual environment erstellen. Linux: `python3 -m venv .venv`
4. Virtual environment aktivieren: Linux: `source .venv/bin/activate`
5. Installation der externen Pakete: Linux: `pip3 install -r requirements.txt`

### Start
#### Erster Start - Datenbank erstellen
Beim ersten Start muss die Datenbank mittels flask-migrate erstellt werden. Es müssen folgende Befehle im Terminal ausgeführt werden:
1. flask db init
2. flask db migrate -m "database creation"
3. flask db upgrade
4. Es wurde nun eine Datenbank namens app.db erstellt, diese muss gelöscht werden und die Datenbank

#### Weitere Starts
Nach dem ersten Start kann das Programm im Terminal über _flask run --host=0.0.0.0 --port=5003_ gestartet werden.

## Implementierungsdetails
Das Strecken-IS wurde mittels des Flask-Frameworks und SQLite als Datenbank implementiert. Es gibt 2 Arten von Nutzern: Mitarbeiter
und Admins, auf die Unterschiede wird in folgenden Absätzen eingegangen. Die Website besteht grundsätzlich aus 3 Pages: Routes, Sections und Stations. Auf diesen Seiten werden die Daten aus der Datenbank angezeigt. Weiters gibt es einen Tab zum ausloggen.

### Admin
Der Admin-User soll nicht nur Daten betrachten, sondern auch bearbeiten können. Für das Erstellen, Bearbeiten und Löschen von Entitäten wurde Flask-Admin verwendet. Die Erweiterung der Strecken um Abschnitte  erfolgt jedoch nicht in Flask-Admin, da bei dieser Funktionalität eine spezielle Logik nötig ist (nur zusammenhängende Abschnitte).
Für Admins gibt es im Menü einen Extra Tab _Admin_, nach Klick auf diesen wird man zur Admin-View weitergeleitet. In dieser können Entitäten bearbeitet werden. Man kann über das Klicken auf den _back to routes_ Link in der rechten oberen Ecke zu der Hauptansicht zurückkehren. In der Admin-View gibt es Tabs zu den Entitäten Strecken, Abschnitte, Stationen, Users und Warnings, durch das Klicken auf einen der Tabs werden die bereits erstellten Entitäten angezeigt. Durch das Klicken auf _Create_ kann eine neue Entität erstellt werden. Durch das Klicken auf das Bleistift-Symbol können Daten bearbeitet werden und durch das Klicken auf das Abfallkübel-Symbol kann eine Entität gelöscht werden. Bei den Usern wurde das Passwort Feld aus Sicherheitsgründen ausgeblendet, da der Admin die Passwörter der Mitarbeiter nicht sehen soll. Weiters wurde bei den Strecken das Feld zum Hinzufügen von Abschnitten ausgeblendet.
Das Hinzufügen von Abschnitten erfolgt auf der Routes-Page über das Klicken des + Symbols. Man wird zu einer Seite mit Drop-Down-Menü weitergeleitet, wo man den gewünschten Abschnitt hinzufügen kann. Das Drop-Down wird mit Abschnitten befüllt, welche zu dem letzten bereits vorhandenen Abschnitt passen (Endbahnhof = Startbahnhof). Ist noch kein Abschnitt bei einer Strecke vorhanden, existieren keine Restriktionen und das Drop-Down enthält alle Abschnitte.
Will man einen neuen Mitarbeiter erstellen funktioniert das über das Klicken auf _click to register_ auf der Login-Page. Hier kann sich
ein neuer Mitarbeiter registrieren. Soll der neue Mitarbeiter Admin sein, kann ein Admin diesen auf der User-Page in der Admin-View über
Klick auf _Is Admin_ zum Admin machen.

#### Mitarbeiter
Mitarbeiter-User sollen keine Daten verändern, sondern nur Daten betrachten können. Deshalb ist der Admin-Tab bei Mitarbeitern ausgeblendet.
Weiters existiert das + Symbol bei den Strecken, mit welchem man neue Abschnitte hinzufügen kann, beim Mitarbeiter nicht. Alle anderen
Pages sind gleich.

#### Schnittstellen
Das Strecken-IS stellt Daten für die nachfolgenden Applikationen bereit. Die Daten werden als json auf den Schnittstellen ausgegeben. Schnittstellen welche zur Verfügung gestellt werden, sind:
- /routes/get - Strecken
- /sections/get - Abschnitte
- /stations/get - Stationen
- /warnings/get - Warnungen
- /trains - Züge

Die Zug-Schnittstelle wurde hier implementiert, da wegen Ausfalls eines Teamkollegen das Flotten-IS nicht implementiert wurde. Es wurde entschieden, dass das Strecken-IS auch die Züge zur Verfügung stellen soll. Auf der Schnittstelle werden Daten von ein json-File, welches Dummy-Daten enthält, ausgegeben.


