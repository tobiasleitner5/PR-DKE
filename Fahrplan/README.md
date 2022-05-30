# Fahrplan-System

## Dependencies

[requirements.txt](./requirements.txt)

## Anleitung

### Installation
1. Git Repository clonen
2. Mittels Command Line ins Root Verzeichnis `Fahrplan` wechseln
3. Virtual environment erstellen. Linux: `python3 -m venv .venv`
4. Virtual environment aktivieren: Linux: `source .venv/bin/activate`
5. Installation der externen Pakete: Linux: `pip install -r requirements.txt`
6. Erster Start

### Start
#### Erster Start und Resets
1. `python3 mockdata.py`
2. `python3 main.py --reset True`

Beim ersten Start wird die Datenbank erstellt. 

Für Testzwecke kann die Fahrplan-Applikation auch allein (ohne Strecken- und Flotteninformationssystem) auf Basis von 
Mockdaten gestartet werden. Da das Flotteninformationssystem in unserer Gruppe nicht implementiert wurde, muss 
folgender Schritt beim ersten Start/Reset-Start immer durchgeführt werden: `python3 mockdata.py`.

#### Weitere Starts
Wird die Applikation neu gestartet, kann man entweder mit jenen Daten arbeiten, die in der Datenbank
gespeichert sind `python3 main.py`, oder man setzt die Datenbank wieder zurück und lädt die aktuellen Daten vom 
Strecken- und Flotteninformationssystem `python3 main.py --reset True`.

## Implementierungsdetails
Für die Implementierung wurde das Flask Framework verwendet. Des Weiteren ist eine SQLite-Datenbank im Einsatz.

Die Applikation wurde mittels Flask-Blueprints modular aufgeteilt. Die Admin-Funktionalitäten wurden in 
[admin.py](admin.py) und die general/employee-Funktionalitäten wurden in [general.py](general.py) implementiert.
In [reset.py](reset.py) wurden die Reset-Funktionalitäten implementiert. [read_input.py](read_input.py) wird für
das Einlesen der Daten aus dem Strecken- und Flotteninformationssystem (bzw. aus [mockdata.py](mockdata.py) verwendet. 
Die Mockdaten befinden sich in [testdata](testdata). 

### Admin
Für die Admin-View wurde das Flask-Admin-Paket verwendet. Damit konnten einfache Views für die im [models.py](./models.py)
erstellten Klassen erstellt werden. Dabei werden standardmäßig Create, Update und Delete Operationen unterstützt.
Diese können zudem sehr individuell angepasst werden. Da jedoch für die Erstellung der Fahrtstrecken und der
Fahrtdurchführungen sehr spezielle Funktionalitäten implementiert werden mussten, wurden die Standard-Views nur für 
Mitarbeiter vollständig genutzt. Die anderen Elemente in der Navigationsbar im Admin-Bereich wurden nahezu vollständig
mit eigenen Funktionalitäten hinterlegt. Um den Zugang nur Admins zu gewähren, wurde die Methode `is_accessible(self)`
für alle Views überschrieben und dementsprechend angepasst. Im Folgenden werden nun die Funktionalitäten des Admin-Bereichs, gegliedert
nach den Elementen der Navigationsbar, beschrieben.

#### Mitarbeiter
Wie bereits erwähnt, wurde für die Mitarbeiterverwaltung die Standard ModelView Anzeige verwendet. Im Reiter Mitarbeiter
können also alle Standard-Operationen im Zusammenhang mit den Mitarbeitern durchgeführt werden.

#### Fahrtstrecke planen
Im Reiter "Fahrtstrecke planen" werden Fahrtstrecken angelegt. Dabei werden zuerst alle Routen aus der Datenbank
mittels diesem [HTML File](./templates/admin/admin_routes_overview.html) angezeigt.
Wird der Link in der jeweiligen Zeile angeklickt, kann für diese Route eine Fahrtstrecke erzeugt werden.
Für die Fahrtstrecke wird dann ein Name und die Abschnitte gewählt. Die Daten werden dann anschließend an den 
Endpoint `/admin/route/store` geschickt und in der Datenbank persistiert.

#### Fahrtdurchführung planen
Die geplanten Fahrtstrecken werden in einer [Tabelle](./templates/admin/admin_plannedroutes_overview.html) angezeigt. Es gibt wieder zwei Links in der Tabelle. Einmal 
für die Planung einer Intervall-Fahrtdurchführung und der zweite Link ist für die Planung der Einzel-Fahrtdurchführung.
 - Einzel-Fahrtdurchführung: Ein einfaches [HTML-Formular](./templates/admin/plan_single_ride_step1.html) mit lediglich einem Eingabefeld wird aufgerufen. Es wird 
    das Datum und die Uhrzeit für die Fahrtdurchführung ausgewählt. Mit diesem Formular werden folgende Daten an
    den Endpoint `/admin/ride/store` mittels GET-Request-Argumenten weitergegeben. Auf Basis dieser Informationen werden
    die verfügbaren Züge und Mitarbeiter im darauffolgenden Formular angezeigt.
   - `time`: Datum und Uhrzeit der Fahrtdurchführung.
   - `interval`: False, da es sich um eine Einzel-Fahrtdurchführung handelt.
   - `plannedroute_id`: Die Fahrtstrecken-ID für die Ermittlung der Abschnitte.

    Nun wird ein weiteres [Formular](./templates/admin/plan_single_ride_step2.html) geöffnet in welchem die `Mitarbeiter`, der `Zug` und der `Preis`* angegeben werden.
    Die Daten vom vorherigen Formular werden nun zusammen mit den Daten aus diesem zweiten Formular an den Endpoint
    `admin/ride/store` mittels POST-Request gesendet und in die Datenbank gespeichert.
   
 - Intervall-Fahrtdurchführung: Ein einfaches [HTML-Formular](./templates/admin/plan_interval_ride_step1.html) mit den folgenden Eingabefeldern wird geöffnet: 
    - `start`: Start-Datum und Uhrzeit für die Intervalldurchführung 
    - `end`: End-Datum des Intervalls
    - `rep_type`: wöchentlich oder täglich 
 
   Diese Daten werden ebenfalls wieder zusammen mit `plannedroute_id` und `interval = True`
   an den Endpoint `/admin/ride/store` mittels GET-Request-Argumenten weitergegeben. Es wird anschließend wieder
   das zweite [Formular](./templates/admin/plan_interval_ride_step2.html) zurückgegeben, in welchem die `Mitarbeiter`,
    der `Zug` und der `Preis`* angegeben werden. Die Daten werden wieder genau gleich verarbeitet wie bei der Planung
    einer einzelnen Fahrtdurchführung; jedoch werden zuerst mithilfe der Informationen (start und end) die konkreten
    Zeiten für die jeweiligen Fahrtdurchführungen ermittelt. 

*Anmerkung zum Preis: Der Preis wird relativ zum kostendeckenden Preis angegeben. Wird im Formular der Wert 0 ausgewählt, 
dann bedeutet dies, dass genau der kostendeckende Preis in der Datenbank gespeichert wird. Wenn beispielsweise 2 
ausgewählt wird, dann wird der Preis auf 2 Einheiten über dem kostendeckenden Preis festgelegt. Somit kann nie ein 
niedrigerer Preis als der kostendeckende Preis gewählt werden.

#### Fahrtdurchführungen
Hier werden alle Fahrtdurchführungen angezeigt. Es können keine Fahrtdurchführungen erstellt werden; jedoch können 
sie bearbeitet und gelöscht werden.

### Employee
Nach dem Login wird auf der Index-Seite eine [HTML-Tabelle](./templates/general/show_rides.html) mit allen Fahrtdurchführungen angezeigt. In dieser Tabelle
kann nach Substrings gesucht bzw. können die Einträge sortiert werden. Die Funktionalitäten wurden Clientseitig
mit Javascript implementiert.

#### Mein Dienstplan
Hier wird dieselbe Tabelle wie auf der Index-Page dargestellt, nur mit dem Unterschied, dass diesmal
die Fahrtdurchführungen auf den angemeldeten User gefiltert werden.

### Login
Die Login-Funktionalitäten wurden mit dem Flask-Login-Manager implementiert.