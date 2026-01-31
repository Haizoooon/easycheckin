# 🏠 easycheckin - Die smarte AirBnB Suite

**easycheckin** ist eine leistungsstarke Home Assistant Integration, die speziell für Hosts entwickelt wurde. Erstelle maßgeschneiderte Modi für Check-In, Reinigung oder Leerstand und steuere Licht, Musik und Benachrichtigungen mit nur einem Klick.

## ✨ Funktionen

* **Unbegrenzte Modi:** Erstelle so viele Zustände wie du brauchst (z. B. „Check-In“, „Check-Out“, „Reinigungs-Modus“).
* **Multi-Geräte-Steuerung:** Verknüpfe Lichter, Schalter und Media Player in einer einzigen Szene.
* **Atmosphären-Garantie:** Setze beim Check-In automatisch die perfekte Lautstärke und starte deine Willkommens-Musik.
* **Gast-Kommunikation:** Sende individuelle Benachrichtigungen direkt bei Aktivierung eines Modus.
* **Live-Konfiguration:** Ändere Einstellungen, Geräte oder Texte im Nachhinein über die Benutzeroberfläche – ganz ohne Neustart dank integriertem Update-Listener.

---

## 🚀 Installation

### Manuell
1. Kopiere den Ordner `easycheckin` in dein `custom_components` Verzeichnis deiner Home Assistant Instanz.
2. Starte Home Assistant neu.
3. Gehe zu **Einstellungen > Geräte & Dienste > Integration hinzufügen**.
4. Suche nach **"easycheckin"** und folge den Anweisungen.

---

## 🛠 Konfiguration

Beim Erstellen eines Modus kannst du folgende Parameter festlegen:

| Parameter | Beschreibung |
| :--- | :--- |
| **Name** | Der Anzeigename der Szene (z. B. „Check-In Gast“). |
| **Icon** | Ein beliebiges MDI-Icon (z. B. `mdi:hand-wave`). |
| **Entitäten** | Wähle Lichter, Media Player und Notify-Dienste aus. |
| **Nachricht** | Der Text, der als Benachrichtigung gesendet werden soll. |
| **Lautstärke** | Die Ziel-Lautstärke für Media Player (0-100%). |

---

## 🎨 Dashboard Integration (Mushroom Style)

Für den perfekten Look empfehlen wir die Verwendung der **Mushroom Chips Card**. Hier ein Beispiel für dein Dashboard:

```yaml
type: custom:mushroom-chips-card
chips:
  - type: template
    entity: scene.easycheckin_checkin
    icon: "{{ state_attr(entity, 'icon') }}"
    icon_color: green
    content: "Check-In"
    tap_action:
      action: call-service
      service: scene.turn_on
      target:
        entity_id: scene.easycheckin_checkin