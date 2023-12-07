![WebPi](https://github.com/NathZenh/WebPiRover/assets/46894591/07e1f6d5-aca2-45ab-937c-b88e44dba939)

# WebPiRover

## Discription
Das Rasperry Pi Mini Car übermittelt Livebilder der Kamera an dessen Webseite worüber man das Fahrzeug mit WASD steueren kann.

## Visualisierung
![Bildschirmfoto 2023-12-06 um 16 12 34](https://github.com/NathZenh/WebPiRover/assets/46894591/02a4f395-c886-4206-9343-beaa665c8bb4)


<details>
  <summary>Video</summary>
  
</details>

## Material
Damit dieses Programm angewendet werden kann gebrauchen Sie:
- Ein Raspberry Pi mit Wlan verbindung
- Ein Mini-Car aufbau
- Ein Batteriepacket für das Raspberry Pi

## Installation
- Installieren Sie (falls noch nicht vorhanden) die zwei Packete *picamera* und *RPi.GPIO*.
- Lade die Dateien **app.py** auf deinen Raspberry Pi (Raspi).
- Passe die Variablen an.

![Code in](https://github.com/NathZenh/WebPiRover/assets/46894591/95af7f05-d5a8-41b5-94c0-4cad5eaa07e9)


- Verbinde deinen Raspberry Pi mit dem Motorcontroller. Du musste es mir nicht gleich machen. !Passe dann aber die Variablen richtig an!

![pinout2](https://github.com/NathZenh/WebPiRover/assets/46894591/7737d144-a787-4287-a419-e274fc234d56)

- Nach dem Start der App auf dem Raspi können Sie von Ihrem Gerät aus die IP-Adresse deines Raspi über einen Browser aufrufen.
  Achten Sie darauf das sie :8000 als Port anhängen.
## Documentation
Dieses Projekt beinhaltet nur eine Datei
- app.py

### Kamera verbinden.
Um mich mit der Kamera auf dem Raspi zu verbinden habe ich die folgende Dokumentation durchgearbeitet:
- https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

Dies hat bei mir auf Anhieb geklappt.

### GPIO von WebServer ansteuern
Um eine LED welche über die GPIO Pins vom Raspi anzusteueren befolgte ich folgendes Tutorial:
- https://www.youtube.com/watch?v=owgRkU_-4lw

Dazu wurde der Code aus diesem Repository kopiert:
- https://github.com/davidrazmadzeExtra/RaspberryPi_HTTP_LED

### Zusammenfügen und anpassen
Anschliessend musste ich beide Dateien in eines bringen. Dies war das umständlichste an diesem Projekt.
Mit viel googlen und befragen von ChatGPT welches beides meist erfolglos war brachte ich es nach vielen Stunden dann zum laufen.

### Rückgabewerte | Javascript & Jquery für Testeneingabe
Besonders mühsam war das zurückliefern der Input von der Webseite in das Python programm während die Kamera läuft. Doch mit Ajax wurde dies dann gelöst.

Im HTML Programm ist ein grosser Codeblock für Javascript. Dort werden die Keyeingaben an die versteckten Inputs geschickt um die Daten per Post dann zurück ans Pythonprogramm zu schicken.
Folglich können Sie den HTML-Code sauber lesen:

![Code in (1)](https://github.com/NathZenh/WebPiRover/assets/46894591/f18ec0c7-18fa-466f-91ff-598cb14d0bdb)


## Lizenz
[MIT](https://choosealicense.com/licenses/mit/)
