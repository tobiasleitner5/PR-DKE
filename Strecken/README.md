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

Es wurde nun eine Datenbank namens app.db erstellt.

Jetzt muss entweder über die Python-Konsole ein Admin-User in der leeren Datenbank erstellt werden oder eine bereits befüllte Datenbank muss gedownloaded werden (siehe nächstes Kapitel _Vorgefertigte Datenbank_).

Soll ein neuer Admin-User erstellt werden müssen folgende Zeilen in die **Python-Konsole** eingegeben werden:
- from app import db 
- from app.models import User 
- db.session.add(User('Admin', 'admin@oebb.at', 'pbkdf2:sha256:260000$AVcGgBYvr3vX5zUz$38f7b51af557748d3ebe4e947acd1d5967567257199fa390317348019cc63f6b', True))
- db.session.commit()

Einloggen kann man sich dann mit dem Benutzernamen _Admin_ und dem Passwort _cat_.
Es können Mitarbeiter-User durch den Button _Click to Register!_ auf der Login Page erstellt werden.

##Vorgefertigte Datenbank
Unter nachfolgendem Link ist eine Datenbank hinterlegt, in welcher sich bereits Daten zu sämtlichen Entitäten befinden.
Die Datenbank muss downgelaoded werden und die leere Datenbank des Projektes muss durch die neue Datenbank aus dem Drive ersetzt werden. Der Admin-User hat die Zugangsdaten _Jonas_ und _cat_, der Mitarbeiter-User hat die Zugangsdaten _Tobias_ und _cat_.
https://drive.google.com/drive/folders/1hCwZw1pgbxABATbyUOLY0CZ4IAXhYzbc?usp=sharing

##Start
Nach Erledigung der vorher angeführten Schritte kann die Applikation im Terminal über die Eingabe von _flask run --host=0.0.0.0 --port=5003_ gestartet werden.

## Implementierungsdetails
Das Strecken-IS wurde mittels des Flask-Frameworks und SQLite als Datenbank implementiert. Es gibt 2 Arten von Nutzern: Mitarbeiter
und Admins, auf die Unterschiede wird in folgenden Absätzen eingegangen. Die Website besteht grundsätzlich aus 3 Pages: Routes, Sections und Stations. Auf diesen Seiten werden die Daten aus der Datenbank angezeigt. Weiters gibt es einen Button zum ausloggen und eine Login Page.

### Admin
Der Admin-User kann nicht nur Daten betrachten, sondern diese auch bearbeiten. Für das Erstellen, Bearbeiten und Löschen von Entitäten wurde Flask-Admin verwendet. Das Hinzufügen und Löschen von Abschnitten zu Strecken erfolgt jedoch nicht in Flask-Admin, da bei dieser Funktionalität eine spezielle Logik nötig ist (nur zusammenhängende Abschnitte). Auch Warnings können direkt in den Pages hinzugefügt und gelöscht werden.

Für Admins gibt es im Menü einen Extra Tab _Admin_, nach Klick auf diesen wird man zur Admin-View weitergeleitet. In dieser können Entitäten bearbeitet werden. Man kann über das Klicken auf den _back to routes_ Link in der rechten oberen Ecke zu der Hauptansicht zurückkehren. In der Admin-View gibt es Tabs zu den Entitäten Strecken, Abschnitte, Stationen, Users und Warnings. Durch das Klicken auf einen der Tabs werden die bereits erstellten Entitäten angezeigt. Durch das Klicken auf _Create_ kann eine neue Entität erstellt werden. Durch das Klicken auf das Bleistift-Symbol können Daten bearbeitet werden und durch das Klicken auf das Abfallkübel-Symbol kann eine Entität gelöscht werden. Bei den Usern wurde das Passwort Feld aus Sicherheitsgründen ausgeblendet, da der Admin die Passwörter der Mitarbeiter nicht sehen soll. Weiters wurde bei den Strecken das Feld zum Hinzufügen von Abschnitten ausgeblendet.

Das Hinzufügen und Löschen von Abschnitten erfolgt auf der Routes-Page über das Klicken der + und - Symbole. Beim Klicken des + Symbols wird man zu einer Seite mit Drop-Down-Menü weitergeleitet, wo man den gewünschten Abschnitt hinzufügen kann. Das Drop-Down wird mit Abschnitten befüllt, welche zu dem letzten bereits vorhandenen Abschnitt passen (Endbahnhof = Startbahnhof). Ist noch kein Abschnitt bei einer Strecke vorhanden, existieren keine Restriktionen und das Drop-Down enthält alle Abschnitte. Beim Klicken auf das - Symbol wird der zuletzt hinzugefügte Abschnitt gelöscht, dies stellt sicher, dass der Constraint der zusammenhängenden Abschnitte gewährleistet wird.

Das Hinzufügen von Warnings erfolgt durch Klicken auf das + Symbol bei den Strecken und Abschnitten. Einzelne Warnings können durch das Klicken auf das - Symbol gelöscht werden. Die Funktionalität wurde so implementiert, dass nur Warnings hinzugefügt werden können, welche noch nicht zu einer Strecke oder einem Abschnitt hinzugefügt worden sind. 

Will man einen neuen Mitarbeiter erstellen funktioniert das über das Klicken auf _click to register_ auf der Login-Page. Hier kann sich
ein neuer Mitarbeiter registrieren. Soll der neue Mitarbeiter Admin sein, kann ein Admin diesen auf der User-Page in der Admin-View über
Klick auf _Is Admin_ zum Admin machen.

### Mitarbeiter
Mitarbeiter-User können keine Daten verändern, sondern nur Daten betrachten. Deshalb ist der Admin-Tab bei Mitarbeitern ausgeblendet.
Weiters kann er keine Abschnitte zu Strecken hinzufügen bzw. diese löschen und keine Warnings zu Strecken und Abschnitten hinzufügen bzw. diese löschen. Alle anderen
Pages sind gleich.

### Schnittstellen
Das Strecken-IS stellt Daten für die nachfolgenden Applikationen bereit. Die Daten werden als json auf den Schnittstellen ausgegeben. Schnittstellen welche zur Verfügung gestellt werden, sind:
- /routes/get - Strecken
- /sections/get - Abschnitte
- /stations/get - Stationen
- /warnings/get - Warnungen
- /trains - Züge

Die Zug-Schnittstelle wurde hier implementiert, da wegen Ausfalls eines Teamkollegen das Flotten-IS nicht implementiert wurde. Es wurde entschieden, dass das Strecken-IS auch die Züge zur Verfügung stellen soll. Auf der Schnittstelle werden Daten von ein json-File, welches Dummy-Daten enthält, ausgegeben.

##Anlegen neuer Entitäten
Beim Anlegen neuer Entitäten ist wichtig zu beachten, dass alle Felder ausgefüllt werden müssen. Nur so kann sichergestellt werden, dass die nachfolgenden Applikationen reibungslos mit den Daten arbeiten können.
