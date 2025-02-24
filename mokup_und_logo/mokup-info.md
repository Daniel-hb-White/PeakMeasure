# mokup-info.md

## **App-Name**: PeakMeasure  

## **App-Beschreibung**  
PeakMeasure ist eine App zur Messung von Höhen und Entfernungen mithilfe der Kamera und des Neigungssensors eines mobilen Geräts. Die App nutzt die Kamera-Vorschau als zentrales Element und zeigt über ein Overlay Messwerte an. Der Benutzer kann eine manuelle Anpassung des Bodenabstands vornehmen, indem er auf den entsprechenden Wert tippt und eine neue Zahl eingibt. Außerdem werden erfasste Höhen in einer JSON-Datei gespeichert.

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

### **Widgets & UI-Elemente (Kivy-kompatibel)**  
| Bereich | Kivy-Widget | Beschreibung |
|---------|------------|--------------|
| **Kameravorschau** | `Camera` | Zeigt das Livebild der Kamera an. |
| **Fadenkreuz** | `Image` oder `Widget` mit `canvas` | Wird zentriert als Orientierungshilfe dargestellt. |
| **Messwert-Anzeigen** | `Label` (oben links und rechts) | Dynamische Anzeige der Messwerte (Höhe & Distanz). |
| **Messauslöser-Button** | `Button` oder `FloatLayout` mit `Button` (unten mittig) | Startet eine neue Messung. |
| **Bodenabstand-Anzeige** | `Label` (unten rechts, klickbar) | Zeigt den aktuellen Bodenabstand an. Beim Antippen erscheint ein Eingabedialog. |
| **Bodenabstand-Eingabe** | `TextInput` (Popup-Dialog) | Ermöglicht dem Benutzer, den Bodenabstand manuell anzupassen. |

### **Interaktionen & Funktionen**  
1. **Messung starten**:  
   - Der Nutzer hält das Gerät auf das gewünschte Ziel ausgerichtet.  
   - Drücken des Messauslösers erfasst die aktuelle Höhe und Distanz.  

2. **Bodenabstand ändern**:  
   - Tippen auf den **Bodenabstandswert (1,5m)** öffnet ein **Eingabefeld** (`TextInput` im `Popup`).  
   - Der Nutzer gibt den neuen Wert ein und bestätigt mit **OK**.  
   - Die Messung wird basierend auf diesem neuen Wert aktualisiert.  

## **Layout-Manager**  
- **Hauptbildschirm**: `FloatLayout`  
  - Die **Kamera-Vorschau** (`Camera`) wird als Hintergrund in einem `FloatLayout` dargestellt.  
  - Alle UI-Elemente (Messwerte, Fadenkreuz, Buttons) werden als Overlays innerhalb des `FloatLayout` positioniert.  
  - `AnchorLayout` oder `GridLayout` kann für die exakte Anordnung von UI-Elementen verwendet werden.  