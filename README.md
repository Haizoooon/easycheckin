<p align="center">
  <img src="https://raw.githubusercontent.com/DEIN_NUTZERNAME/easycheckin/main/icon.png" alt="easycheckin Logo" width="200">
</p>

# 🏠 easycheckin - Die smarte AirBnB Suite

**easycheckin** ist eine professionelle Home Assistant Integration für AirBnB-Hosts. Nach der Installation erstellt die Suite automatisch drei feste Szenen und einen Status-Sensor, mit denen du deine Unterkunft per Klick verwalten kannst.

## ✨ Funktionen

* **Drei feste Modi:** Automatisches Setup für **Check-In**, **Check-Out** und **Reinigung**.
* **Eingebauter Status-Sensor:** Ein globaler Sensor (`sensor.easycheckin_status`) zeigt jederzeit an, ob Gäste im Haus sind oder ob gereinigt wird.
* **Volle Flexibilität:** Nutze den nativen Home Assistant Action-Selector, um beliebig viele Aktionen (Lichter, Schlösser, Musik, Benachrichtigungen) pro Modus festzulegen.
* **Kein Neustart nötig:** Änderungen an den Aktionen werden sofort übernommen.

---

## 🚀 Installation

### 1. Über HACS (Empfohlen)
Da dies eine Custom Integration ist, musst du sie in HACS als benutzerdefiniertes Repository hinzufügen:
1. Öffne **HACS** in Home Assistant.
2. Klicke oben rechts auf die drei Punkte und wähle **Benutzerdefinierte Repositories**.
3. Füge die URL deines GitHub-Repositorys ein und wähle als Kategorie **Integration**.
4. Klicke auf **Installieren**.
5. Starte Home Assistant neu.

### 2. Integration aktivieren
1. Gehe zu **Einstellungen > Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen** und suche nach **easycheckin**.
3. Nach der Installation findest du drei neue Szenen und einen Sensor in deinen Entitäten.

---

## 🛠 Konfiguration

Um die Aktionen für die einzelnen Modi festzulegen:
1. Gehe zu **Einstellungen > Geräte & Dienste**.
2. Suche die **easycheckin** Kachel.
3. Klicke auf **Konfigurieren**.
4. Hier kannst du nun für jeden Modus (Check-In/Out/Service) die gewünschten Geräte und Dienste hinzufügen.

---

## 🎨 Dashboard (Modern Mushroom UI)

> [!IMPORTANT]
> Für die Darstellung dieser Karten muss die [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) Erweiterung via HACS installiert sein. Für die farbigen Hintergründe wird zusätzlich [card-mod](https://github.com/thomasloven/lovelace-card-mod) empfohlen.

### Status-Zentrale & Steuerung
Kopiere diesen Code in ein **Gitter-Layout (Grid)** in deinem Dashboard:

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-template-card
    primary: "Status: {{ states('sensor.easycheckin_status') }}"
    secondary: >
      {% if is_state('sensor.easycheckin_status', 'checkin') %} Gäste im Haus
      {% elif is_state('sensor.easycheckin_status', 'maintenance') %} Reinigung läuft
      {% else %} Haus bereit für Gäste {% endif %}
    icon: "{{ state_attr('sensor.easycheckin_status', 'icon') }}"
    icon_color: >
      {% if is_state('sensor.easycheckin_status', 'checkin') %} green
      {% elif is_state('sensor.easycheckin_status', 'maintenance') %} blue
      {% elif is_state('sensor.easycheckin_status', 'checkout') %} orange
      {% else %} grey {% endif %}
    entity: sensor.easycheckin_status

  - type: grid
    columns: 2
    square: false
    cards:
      - type: custom:mushroom-entity-card
        entity: scene.easycheckin_checkin
        name: Check-In
        icon_color: green
        layout: vertical
        tap_action:
          action: call-service
          service: scene.turn_on
          target:
            entity_id: scene.easycheckin_checkin

      - type: custom:mushroom-entity-card
        entity: scene.easycheckin_checkout
        name: Check-Out
        icon_color: orange
        layout: vertical
        tap_action:
          action: call-service
          service: scene.turn_on
          target:
            entity_id: scene.easycheckin_checkout