# Ticketing-System

## Dependencies

[requirements.txt](./requirements.txt)

## Anleitung

### Installation
1. Git Repository clonen
2. Mittels Command Line ins Root Verzeichnis `tickets` wechseln
3. Virtual environment erstellen. Linux: `python3 -m venv .venv`
4. Virtual environment aktivieren: Linux: `source .venv/bin/activate`
5. Installation der externen Pakete: Linux: `pip install -r requirements.txt`
6. Erster Start

### Start
#### Erster Start - Datenbank erstellen/Admin einfügen
Beim ersten Start muss die Datenbank mittels flask-migrate erstellt werden. Es müssen folgende Befehle im Terminal ausgeführt werden (sollte eine Datenbank bereits existieren ist es sinnvoll sie bei erstmaliger Ausführung zu löschen):
1. flask db init (falls dabei der _Fehler ConnectionRefusedError: [Errno 61]_ auftritt ist für die Erstellung der DB die Variable `dummydata` in [api.py](./api.py) auf True zu setzen)
2. `flask db migrate -m "database creation"`
3. `flask db upgrade`
4. Es wurde nun eine Datenbank namens app.db erstellt
5. Manuelles Einfügen des Administrator-Benutzers in die Datenbank (dazu kann mit dem Befehl `python3` in der Command Line die Python Console aufgerufen werden)
-> Folgende Befehle sind in der Python Console einzugeben, um den Admin der Datenbank hinzuzufügen:
- from app import db
- from app.models import User
- u = User(username='admin', email='admin@example.com')
- u.set_password('admin')
- u.set_access('admin')
- db.session.add(u)
- db.session.commit()

Info:
- Um die Daten über die Schnittstellen zu konsumieren, muss die Variable `dummydata` in [api.py](./api.py) auf False gesetzt sein. 
- Um Dummydaten zu konsumieren, muss die Variable `dummydata` in [api.py](./api.py) auf True gesetzt sein

#### Start der Applikation
Das Programm kann im Terminal mit dem Befehl `flask run` gestartet werden, wobei standardmäßig der Port 5000 verwendet wird.
Sollte standardmäßig nicht der Port 5000 verwendet werden, kann die Applikation auch mit folgendem Befehl `flask run --host=0.0.0.0 --port=5000` ausgeführt werden.

### Admin
Der Admin kann nach dem Login (User & Password = 'admin') über die Seitenleiste zwischen drei verschiedenen Ansichten wechseln.
Im ersten Reiter 'Aktionen' hat der Admin die Möglichkeit Aktionen festzulegen. Dabei kann er entweder Aktionen für alle Strecken oder nur für eine bestimmte Strecke festlegen.
Im zweiten Reiter 'Übersicht' können alle ausgegebenen Aktionen eingesehen bzw. auch gelöscht werden.
Im dritten Reiter können die persönlichen Daten des eigenen Profils bearbeitet werden.

#### Kunde
Der Kunde kann nach der Registrierung bzw. nach Login über die Seitenleiste zwischen drei verschiedenen Ansichten wechseln.
Im ersten Reiter 'Ticketsuche' hat der Kunde die Möglichkeit unter Angabe des Datums sowie des Start- und Endbahnhofs eine Fahrtdurchführung zu suchen. 
Im zweiten Reiter 'Meine Tickets' kann der Kunde alle gekauften Tickets inkl. Status einsehen. Zudem hat er die Möglichkeit Sitzplätze für Tickets zu reservieren.
Im dritten Reiter können die persönlichen Daten des eigenen Profils bearbeitet werden.

#### Schnittstellen
Die Applikation konsumiert Daten sowohl vom Streckeninformationssystem als auch vom Fahrplaninformationssystem. Da die Applikation zum Verwalten der Flotten nicht umgesetzt wurde, werden entsprechende Daten über eine Schnittstelle im Streckensystem zur Verfügung gestellt.
Alternativ kann die Applikation mit Dummydaten gestartet werden. Hierzu muss (vor dem Start) im File [api.py](./api.py) die Variable `dummydata` auf True gesetzt werden.