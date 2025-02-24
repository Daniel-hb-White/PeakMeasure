## **Nutzungsorientierung**  
- Die App wird primär im **Hochformat** genutzt.  
- Die UI ist für eine **einhändige Bedienung** optimiert.  

## **Hauptbildschirm**  
### **Allgemeine Struktur**  
Die App besteht aus einer einzigen Ansicht, die in folgende Bereiche unterteilt ist:  
1. **Kameravorschau** (Hintergrund, nimmt den gesamten Bildschirm ein).  
2. **Overlay mit Messwerten und Bedienelementen**:
   - Fadenkreuz zur Zielerfassung.  
   - Anzeigen für Höhe und Distanz.  
   - Button zur Messdatenerfassung.  
   - Manuelle Eingabe für Bodenabstand.  

### **Widgets & UI-Elemente**  
| Bereich | Element-Typ | Beschreibung |
|---------|------------|--------------|
| **Kameravorschau** | `ImageView` oder direkter Kamera-Feed | Zeigt das Livebild der Kamera an. |
| **Fadenkreuz** | `ImageView` oder `Canvas` | Wird zentriert als Orientierungshilfe dargestellt. |
| **Messwert-Anzeigen** | `TextView` (oben links und rechts) | Dynamische Anzeige der Messwerte (Höhe & Distanz). |
| **Messauslöser-Button** | `FloatingActionButton` (unten mittig) | Startet eine neue Messung. |
| **Bodenabstand-Anzeige** | `TextView` (unten rechts, klickbar) | Zeigt den aktuellen Bodenabstand an. Beim Antippen erscheint ein Eingabedialog. |
| **Bodenabstand-Eingabe** | `EditText` (Popup-Dialog) | Ermöglicht dem Benutzer, den Bodenabstand manuell anzupassen. |

### **Interaktionen & Funktionen**  
1. **Messung starten**:  
   - Der Nutzer hält das Gerät auf das gewünschte Ziel ausgerichtet.  
   - Drücken des Messauslösers erfasst die aktuelle Höhe und Distanz.  

2. **Bodenabstand ändern**:  
   - Tippen auf den **Bodenabstandswert (1,5m)** öffnet ein **Eingabefeld**.  
   - Der Nutzer gibt den neuen Wert ein und bestätigt mit **OK**.  
   - Die Messung wird basierend auf diesem neuen Wert aktualisiert.  
