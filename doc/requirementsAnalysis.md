# Anforderungen

- Das System ist eine Art "Moorgrundbuch"
- WebUI mit DB Backend
- Für verschiedene Standorte verschiedene Daten eingeben und auslesen
- Eingabe mit Validierung/Plausibilisierung
- Nutzerverwaltung?!
- Die Datenbank ist Grundlage für die Organisation von Begehungen der einzelnen Standorte
- Grundlage für Dokumentationen, die für Verträge benötigt werden
- perspektivisch sollen pro Standort noch weitere (Forschungs)daten hinterlegt werden

## technische Details

- Python und Flask für UI für Middleware
- HTML, CSS VanillaJS für Frontend
- PostgreSQL als DB

## Startseite

- Kartenübersicht als Start mit Suchfunktion
- bei Klick auf Standort --> Detailansicht
- Bei Details gibt es Details zur Anlage (Stammdaten) sowie Metadaten (zuletzt besucht von ... etc); erstmal keine Bewegungsdaten

## Listenübersicht

- alle der folgenden Listen mit Sortierung/Filterung etc.
- Alle Anlagen als Liste 
- Alle Personen als Liste
- Alle Institutionen als Liste

## Datenschema
- Cluster
- Standort
- Ein Standort hat zu einem Zeitpunkt genau eine Nutzungsart
- Ein Standort hat zu jedem Zeitpunkt eine hydrologische Situation
- Ein Standort hat zu jedem Zeitpunkt einen bestimmten Bodentyp
- Ein Standort hat zu jedem Zeitpunkt einen bestimmte Vegetation
- Pro Standort gibt es eine Menge an installierter Messtechnik, die erfasst und verwaltet werden soll
- Pro Standort soll es ein Journal der dort getätigten Aktionen geben
- Aktionen werden von Personen durchgeführt
- Auch pro Person soll es ein Journal der durchgeführten Aktionen geben
- Es gibt Flurstücke
- Ein Standort kann auf einem oder mehreren Flurstücken liegen
- Jedes Flurstück hat einen Eigentümer
- Es gibt Personen
- Personen können in Bezug zu einem Standort verschiedenen Rollen einnehmen
- Es gibt folgende Rollen: Bewirtschafter, Eigentümer, Pächter, Ansprechpartner, sonstiges
- Personen haben noch weitere Eigenschaften haben wie Anrede, Name, Anschrift, Email, Telefonnummer, IBAN, Beruf
- Es gibt Institutionen, wie z.B. Unis, Hochschulen, Forschungseinrichtungen, Firmen, Behörden etc. mit allen nötigen Feldern
- Personen gehören zu Institutionen und können die Institution wechseln.


## Berichte

- pro Standort soll es einen Bericht geben