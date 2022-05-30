<a href="Development.en.md"><img src="images/en.svg" valign="top" align="right"/></a>
<a href="Development.md"><img src="images/de.svg" valign="top" align="right"/></a>
[![Version][version-badge]][version-url]
[![License][license-badge]][license-url]
<!--
[![Bugs][bugs-badge]][bugs-url]
-->

### Home Assistant Blueprint - Einrichtung der Entwicklungsumgebung
<br/>

[![Logo][logo]][project-url]
### ![ggshield](images/ggshield.png) GitGuardian einrichten (falls gewünscht)

Nachdem du in der ReadMe bereits erfahren hast, wo und wie du dein(e) persönlichen Zugriffstoken für GitGuardian erzeugen kannst, müssen die Token "nur" noch an den richtigen Stellen eingetragen werden. Fangen wir mit deiner Entwicklungsumgebung an. Ich empfehle die Konfiguration über die Datei ```~/.gitguardian.yml```. Du kannst dort GitGuardian an deine Bedürfnisse anpassen und obwohl es in der Dokumentation nicht zu finden ist, kannst du dort auch **deinen API_KEY eintragen**. (Ich liebe es, wenn die Docus das Wichtigste verschweigen.) Deine Konfigurationsdatei könnte dann in etwa so aussehen:

```
api-key: <Dein gerade erzeugtes persönliches Zugriffstoken>
...
# weitere persönliche Einstellungen
```

So ist es auch relativ einfach, ein neues Token einzutragen, wenn dein vorheriges abgelaufen ist. Du könntest dir für deine Entwicklungsumgebung natürlich auch ein Token erzeugen, das kein Ablaufdatum hat, ohne das die Sicherheit darunter leiden würde. Aber nach meiner Erfahrungen nehmen wir uns alle vor unsere Passwörter regelmäßig zu ändern, aber wenn wir nicht durch ein Ablaufdatum dazu gezwungen werden, gerät es dann doch immer wieder in Vergessenheit.

Kommen wir nun zur Konfiguration der GitHub-Actions. Als erstes solltest du deine Repositories, die du von GitGuardian überprüfen lassen möchtest, schon mal vorbereiten. Du musst für jedes Repository in die Einstellungen (```Settings```) gehen. Dort findest du unter ```Secrets``` den Punkt ```Actions```. Nutze den Button ```New repository secret```. Dort kannst du dann dein zweites persönliches Zugriffstoken eintragen. Bei ```Name``` musst du den Namen **GITGUARDIAN_API_KEY** eintragen und bei Value dein Token. Fertig!

Nachdem deine Repositories vorbereitet sind, musst du die API "nur noch" auf GitGuardian aktivieren. Dazu gehst du im Dashboard auf ```INTEGRATIONS```. Unter VCS Integrations findest du GitHub und dort musst du dann nur noch den ```Install```-Button drücken, die Einstellungen vornehmen. Damit hast du es dann geschafft.





[logo]: images/hassio-icon.png
[project-url]: https://homeassistant.io

[license-badge]: images/lizenz.svg
[license-url]: ../LICENSE.md

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/Home-Assistant-Blueprint/releases

