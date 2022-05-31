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

### [![ggshield][ggshield]][ggshield-url]GitGuardian einrichten (falls gewünscht)

Um die Überprüfungen von [GitGuardian][ggshield-url] zu verwenden, benötigst du zunächst ein kostenloses Konto. Der Link im vorherigen Satz führt dich direkt auf die Startseite und dort nutze den ```Start for free```-Button. Nachdem du dein Konto eingerichtet hast, kannst du über ```API``` / ```Personal access tokens``` die benötigten persönlichen Zugangstoken erzeugen lassen. Nach dem Drücken von ```Create token``` gib deinem Token einen Namen, damit du später erkennen kannst, wofür du es verwendest und nimm dann die folgenden Einstellungen vor:

- ```Expires:``` Für das Token, das du in deiner Entwicklungsumgebung einsetzen möchtest, empfehle ich eine Ablauffrist von 6 Monaten bis max. 1 Jahr. Für das Token, das du auf GitHub verwendest empfehle ich max. 6 Monate.
- ```Scope:``` Bitte nur "scan" auswählen.

Nachdem du den ```Create token```-Button gedrückt hast, wird dir dein neues Zugangstoken angezeigt (etwas unauffällig ganz oben, grün hinterlegt). Kopier es in eine Datei oder in deinen Passwort-Manager. Du wirst es nie wieder sehen. Nachdem du die beiden Token erzeugt hast, müssen sie "nur noch" an den richtigen Stellen hinterlegt werden, um dann zum Abschluss GitGuardian als GitHub Apps zu aktivieren.

#### Integration von GitGuardian in die pre-commit Überprüfungen

Die eigentliche Integration von GitGuardian in die pre-commit Überprüfungen hat dieses Blueprint bereits für dich vorgenommen. Du musst allerdings noch dein Zugangstoken an geeigneter Stelle hinterlegen und bei der Vorbereitung des virtuellen Python-Environment GitGuardian installieren. Die Details für die Installation erfährst du im Abschnitt **Vorbereitung des virtuellen Python-Environments**. Hier bleiben wir erst einmal bei der geeigneten Stelle für dein Zugangstoken.

Du kannst dein Token entweder in der Umgebungsvariablen ```GITGUARDIAN_API_KEY``` speichern (z.B. indem des es in ```~/.bashrc``` exportierst) oder es in die Konfigurationsdatei von GitGuardian ```~/.gitguardian.yml``` eintragen (meine bevorzugte Variante). Bei der zweiten Variante hast du den Vorteil, dass du GitGuardian an der gleichen Stelle an deine persönlichen Bedürfnisse anpassen kannst (siehe GitGuardian-Dokumentation) und, obwohl es in der Dokumentation nicht zu finden ist, hier auch **dein Zugangstoken** hinterlegen kannst. (Ich liebe es, wenn die Docus das Wichtigste verschweigen.) Deine Konfigurationsdatei könnte dann in etwa so aussehen:

```
api-key: <Dein gerade erzeugtes persönliches Zugriffstoken>
...
# weitere persönliche Einstellungen
```

#### Integration von GitGuardian in die GitHub-Workflows

Als erstes solltest du deine Repositories schon mal vorbereiten. Dazu musst du für jedes Repository in die Einstellungen (```Settings```) gehen. Dort findest du unter ```Secrets``` den Punkt ```Actions```. Nutze den ```New repository secret```-Button. Dort kannst du dann dein zweites persönliches Zugriffstoken eintragen. Bei ```Name``` musst du den Namen **GITGUARDIAN_API_KEY** verwenden und bei ```Value``` dein Token. Fertig!

Abschliessend muss GitGuardian dann noch als GitHub-App aktiviert werden (zu finden unter deinen Konto-Settings / Applications). Der Vorgang muss allerdings **auf GitGuardian** eingeleitet werden. Dazu gehst du im [Dashboard][gg-dash] auf ```INTEGRATIONS```. Unter *VCS Integrations* findest du GitHub und dort musst du dann nur noch den ```Install```-Button drücken und die Einstellungen vornehmen. Damit hast du es dann geschafft.

### [![python][python]][python-url]Vorbereitung des virtuellen Python-Environments





[logo]: images/hassio-icon.png
[project-url]: https://homeassistant.io

[license-badge]: images/lizenz.svg
[license-url]: ../LICENSE.md

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/Home-Assistant-Blueprint/releases

[ggshield]: images/ggshield.png
[ggshield-url]: https://www.gitguardian.com/
[gg-dash]: https://dashboard.gitguardian.com/
[python]: images/python.svg
[python-url]: https://www.python.org/