# Moorgrundbuch

Eine Webanwendung zur Verwaltung von Moorstandorten, Personen, Institutionen und Messtechnik.

## Beschreibung

Das Moorgrundbuch ist eine Webanwendung, die als Grundlage für die Organisation von Begehungen einzelner Moorstandorte dient. Es ermöglicht die Verwaltung von Standortdaten, Personen, Institutionen und Messtechnik. Die Anwendung bietet eine Kartenübersicht, Detailansichten für Standorte und Funktionen zur Dokumentation von Aktivitäten an den Standorten.

## Technologien

- **Backend**: Python mit Flask
- **Frontend**: HTML, CSS, VanillaJS
- **Datenbank**: PostgreSQL mit PostGIS für geografische Daten

## Voraussetzungen

- Python 3.8 oder höher
- PostgreSQL 12 oder höher mit PostGIS-Erweiterung
- pip (Python-Paketmanager)

## Installation

1. Repository klonen:
   ```
   git clone <repository-url>
   cd moorgrundbuch
   ```

2. Python-Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

3. PostgreSQL-Datenbank einrichten:
   - PostgreSQL und PostGIS installieren
   - Datenbank erstellen:
     ```
     createdb moorgrundbuch
     ```
   - Datenbank-Schema importieren:
     ```
     psql -d moorgrundbuch -f database/setup.sql
     ```

4. Umgebungsvariablen konfigurieren:
   Erstellen Sie eine `.env`-Datei im Hauptverzeichnis mit folgendem Inhalt:
   ```
   DATABASE_URL=postgresql://username:password@localhost/moorgrundbuch
   SECRET_KEY=your-secret-key
   ```
   Ersetzen Sie `username`, `password` und `your-secret-key` mit Ihren eigenen Werten.

## Starten der Anwendung

1. Flask-Anwendung starten:
   ```
   cd backend
   python app.py
   ```

2. Öffnen Sie einen Webbrowser und navigieren Sie zu:
   ```
   http://localhost:5000
   ```

## Projektstruktur

```
/moorgrundbuch
  /backend
    app.py              # Hauptanwendungsdatei
    database.py         # Datenbankmodelle und -verbindung
    /templates          # HTML-Templates (falls benötigt)
    /static             # Statische Dateien für das Backend
  /frontend
    index.html          # Hauptseite mit Kartenübersicht
    locations.html      # Standortliste
    persons.html        # Personenliste
    institutions.html   # Institutionenliste
    login.html          # Login-Seite
    /css
      styles.css        # Hauptstilvorlage
    /js
      map.js            # Karten-Funktionalität
      scripts.js        # Allgemeine Funktionalität
  /database
    setup.sql           # SQL-Skript zum Einrichten der Datenbank
  requirements.txt      # Python-Abhängigkeiten
  README.md             # Projektdokumentation
```

## Funktionen

- **Kartenübersicht**: Zeigt alle Standorte auf einer interaktiven Karte an
- **Standortverwaltung**: Hinzufügen, Bearbeiten und Löschen von Standorten
- **Personenverwaltung**: Verwaltung von Personen und ihren Beziehungen zu Standorten
- **Institutionsverwaltung**: Verwaltung von Institutionen und ihren Beziehungen zu Personen
- **Journalführung**: Dokumentation von Aktivitäten an Standorten und durch Personen
- **Messtechnikverwaltung**: Verwaltung von Messtechnik an Standorten

## Lizenz

Dieses Projekt ist lizenziert unter [Ihre Lizenz hier]. 