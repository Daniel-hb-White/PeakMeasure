# 🛠️ Qualitätssicherung für das Messsystem (Soll-Ist-Vergleich)

## 🔍 1. Soll-Ist-Vergleich

Der Soll-Ist-Vergleich ist ein wichtiger Teil der Qualitätssicherung. Hierbei wird überprüft, ob das Messsystem so funktioniert, wie es geplant war und ob es alle Anforderungen erfüllt. Es wird geschaut, ob die tatsächliche Umsetzung im Code die festgelegten Anforderungen erfüllt. Außerdem wird getestet, ob das System wie gewünscht arbeitet und die richtigen Ergebnisse liefert.

### 📝 Soll-Anforderungen:

- **Entfernung berechnen**: Die Entfernung soll basierend auf dem Pitch-Winkel (Neigungswinkel der Messung um die X-Achse) richtig berechnet werden. Das heißt, der Winkel muss in die Berechnung der Entfernung einfließen, damit die Messung genau ist.
- **Höhenanpassung**: Die Höhe muss je nach Messmodus und der Körpergröße richtig angepasst werden. Das System muss erkennen, ob es sich um ein kleines oder großes Objekt handelt und die Körpergröße entsprechend in die Berechnung einfließen lassen.
- **Fehlerbehandlung**: Wenn der Pitch-Wert fehlerhaft ist (zum Beispiel kleiner als 1° oder größer als 89°), soll das System das verhindern und mit einem korrigierten Wert weiterarbeiten. Bei einem Wert unter 1° wird der Wert auf 1° gesetzt, bei einem Wert über 89° auf 89°.

---

### 🔎 Ist-Analyse:

- **Pitch-Wert Begrenzung**: Der Pitch-Wert wird im Bereich von 1° bis 89° begrenzt.
  - **Analyse**: Der Code überprüft, ob der Pitch-Wert im richtigen Bereich liegt. Wenn der Wert unter 1° oder über 89° liegt, wird der Wert auf den erlaubten Bereich korrigiert.
  - **Ergebnis**: ✅ Das System stellt sicher, dass nur gültige Pitch-Werte verarbeitet werden und keine fehlerhaften Berechnungen gemacht werden.
  
- **Berechnung der Entfernung**: Die Entfernung wird mit der trigonometrischen Funktion `tan` (Tangens) berechnet.
  - **Analyse**: Der Pitch-Winkel wird genutzt, um die Entfernung durch die Tangens-Funktion zu berechnen. Außerdem wird die Entfernung auf zwei Nachkommastellen gerundet.
  - **Ergebnis**: ✅ Die Berechnung funktioniert korrekt, und die Entfernung wird genau berechnet und richtig gerundet angezeigt.

- **Höhenanpassung**: Die Höhe wird je nach Messmodus (kleine oder große Objekte) angepasst, wobei auch die Körpergröße berücksichtigt wird.
  - **Analyse**: Das System erkennt, ob das Objekt groß oder klein ist. Wenn es größer als die Körpergröße ist, wird der Modus für große Objekte verwendet. Wenn es kleiner ist, wird der Modus für kleine Objekte genutzt. Je nach Modus wird die Körpergröße entweder hinzugefügt oder abgezogen.
  - **Ergebnis**: ✅ Das System erkennt die verschiedenen Messmodi und passt die Höhe richtig an.

- **Fehlerbehandlung**: Fehler bei Eingaben werden erkannt und angezeigt.
  - **Analyse**: Das System überprüft, ob die Eingaben der Körpergröße gültig sind. Wenn etwas nicht stimmt, wird der Benutzer informiert.
  - **Ergebnis**: ✅ Fehlerhafte Eingaben werden erkannt, und der Benutzer erhält eine klare Fehlermeldung.

---

### ✅ Ergebnis:

Der Soll-Ist-Vergleich zeigt, dass das Messsystem alle wichtigen Anforderungen erfüllt. Alle Funktionen arbeiten wie erwartet, und es werden keine falschen oder unrealistischen Ergebnisse angezeigt. Das System funktioniert wie gewünscht und erfüllt alle festgelegten Anforderungen, was zu einer erfolgreichen Implementierung führt.

---

### Zusammenfassung der Umsetzung:

1. **Pitch-Wert Begrenzung**: Der Pitch-Wert wurde richtig überprüft, sodass nur gültige Werte verwendet werden.
2. **Entfernungsberechnung**: Die Entfernung wird korrekt mit der Tangens-Funktion berechnet.
3. **Höhenanpassung**: Je nach Messmodus wird die Körpergröße korrekt in die Berechnung der Höhe einbezogen.
4. **Fehlerbehandlung**: Ungültige Eingaben werden erkannt und der Benutzer wird informiert.

Alle Tests und Vergleiche haben gezeigt, dass das Messsystem wie gewünscht funktioniert und die Qualität des Systems gewährleistet ist.
