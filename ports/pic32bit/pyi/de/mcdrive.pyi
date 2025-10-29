"""Antriebsbibliothek Stub/Schnittstelle für fullmo MovingCap Servoantriebe

Die Antriebsbibliothek ermöglicht den Zugriff auf das MovingCap DS402/CiA402 Objektverzeichnis für
Micropython-Skripte, die auf MovingCap Ethernet-Antriebe geladen und ausgeführt werden können 
(MC349 ETH oder MCN23 ETH).

* WriteObject und ReadObject bieten allgemeinen Zugriff auf alle verfügbaren Objekte des 
MovingCap's Laufwerksverzeichnis. Wenn Sie mit den DS402/CiA402-Standardobjekten vertraut sind 
und den herstellerspezifischen Objekten, wie sie im MovingCap Benutzerhandbuch dokumentiert sind, vertraut sind, ist dies
ist dies alles, was Sie brauchen, um eine vollständige Antriebsmaster-Anwendung zu schreiben. 

* Zusätzliche Funktionen werden als Abkürzung und zur schnelleren Erstellung Ihrer Anwendungen bereitgestellt.
Sie führen im Wesentlichen mehrere Schreib-/Leseoperationen auf den DS402/CiA402-Objekten für
die gewünschte Funktion. In unseren Beispielen können Sie sehen, wie Sie Ihren Antrieb
mit nur ein paar Zeilen Code in Gang bringen.
"""
__author__ = "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.05.xxx"
__date__ = "2023-03-09"

def WriteObject(index : int, subindex : int, value : int) -> int:
    """CANopen-Objektwert schreiben (nur numerisch)

    :param index: CANopen-Index [unsigned16], z.B. 0x607A für "Zielposition"
    :Typ index: int
    :param subindex: CANopen-Subindex [unsigned8], z.B. 0
    :typ subindex: int
    :param value: neuer Wert für dieses Objekt [integer32]
    :typ wert: int
    :return: 0, wenn erfolgreich, oder der interne Fehlercode vom CANopen-Stack.
        Sie können diesen Wert normalerweise ignorieren. Prüfen Sie nur, wenn Sie sich nicht sicher sind 
        ob der Index/Subindex überhaupt ein gültiges Objekt für den Schreibzugriff ist. 
    :rtype: int
    """
    ret = 0
    return ret

def ReadObject(index : int, subindex : int) -> int:
    """CANopen-Objektwert lesen (nur numerisch)

    :param index: CANopen-Index [unsigned16], z.B. 0x6064 für "Positions-Istwert"
    :Typ index: int
    :param subindex: CANopen-Subindex [unsigned8], z.B. 0
    :typ subindex: int
    :return: aktueller Objektwert [integer32]. Wenn das Objekt kein gültiges Objekt für den Lesezugriff ist,
        wird ein interner CANopen-Stack-Fehlerwert zurückgegeben. Beachten Sie, dass der Rückgabewert immer integer32 ist,
        auch wenn der Eintrag im Objektverzeichnis einen anderen CANopen-Datentyp hat. 
    :rtype: int
    """
    Wert = 0
    Rückgabewert

def WriteControl(control : int):
    """DS402-Steuerwort schreiben (CANoypen-Objekt 6040h.0h)

    :param control: neuer Wert [unsigned8]
    :Typ Steuerung: int
    """
    pass


def EnableDrive():
    """Für den Betrieb vorbereiten. 
    
    Diese Funktion schaltet durch die erforderlichen Zustände der DS402-Zustandsmaschine,
    bis "Betrieb freigegeben" erreicht ist. 
    
    Dies ist gleichbedeutend mit der Überprüfung des Antriebsstatuswortes
    über `ReadStatusword` zu überprüfen und die erforderlichen Zustandsänderungen mit 
    `WriteControl`. Der Ablauf ist wie folgt:

    * Wenn Antrieb im Fehlerzustand: WriteControl(0x80) fault reset -> neuer Zustand "switch on disabled"
    * WriteControl(0x6) shutdown -> neuer Zustand "ready to switch on"
    * WriteControl(0x7) switch on -> neuer Zustand "switched on"
    * WriteControl(0xf) enable operation -> neuer Zustand "operation enabled"
    
    Es werden nur die erforderlichen Übergänge durchgeführt. Wenn der Antrieb bereits im Zustand "Betrieb freigegeben" ist
    Zustand (ReadStatusword ist 0x27), kehrt die Funktion sofort zurück.

    Siehe auch `PowerQuit`

    :Rückgabe: 1 wenn Wechsel zu "operation enabled" erfolgreich. 0 wenn fehlgeschlagen.
    :rtype: int
    """
    Wert = 0
    Rückgabewert

def StopMotion():
    """Kommandiert einen Schnellstopp ("Abbremsen auf Schnellstopp-Option Rampe"). 
    Verwendet Objekt 6085h.0h Schnellstopp-Verzögerungswert. 
    """
    pass

def PowerQuit():
    """Setzt den Betriebsmodus auf Null zurück (siehe `SetOpMode`), 
    schaltet dann die DS402 Zustandsmaschine auf "switch on disabled". 

    Siehe auch `EnableDrive`
    """
    pass

def GoPosAbs(targetPos : int):
    """Neue Bewegung zu einer absoluten Position starten.

    * Falls erforderlich, auf Betriebsart 1 - Profilpositionierung - umschalten (SetOpMode(1))
    * Setzen des neuen Ziels (siehe `SetTargetPos`)
    * Starten Sie die Positionierung im DS402 "single setpoint"-Modus: Die neue Zielposition wird sofort verarbeitet.

    Die Positioniersteuerung verwendet "6083h.0h profile acceleration" (`SetAcc`) und 
    "6084h.0h Profilverzögerung" (`SetDec`) für die Bewegung. 

    Verwenden Sie `ChkReady` und `ChkError`, um auf das Ende der Positionierung zu warten und Fehler während der Fahrt zu erkennen. 

    Siehe auch 'GoPosRel'

    :param targetPos: neue absolute Zielposition [integer32]
    :Typ targetPos: int
    """
    pass

def GoPosRel(relativePos : int):
    """Neue Bewegung zur relativen Position starten.

    Dasselbe wie `GoPosAbs`, aber mit Angabe einer relativen Position. 

    Standardmäßig bedeutet "relativ" "relativ zur vorher verwendeten Zielposition", 
    aber das Objekt "60F2h.0h positioning option code" kann eine andere Bedeutung angeben 
    Bedeutung angeben, z.B. "relativ zur aktuellen Ist-Position".

    :param relativePos: neue relative Zielposition [integer32]
    :Typ relativePos: int
    """
    pass

def GoVel(ZielGeschwindigkeit : int):
    """Neue Operation mit konstanter Geschwindigkeit starten.

    * Falls erforderlich, auf Betriebsart 3 - Profilgeschwindigkeitsmodus - umschalten (SetOpMode(3))
    * Neue Zielgeschwindigkeit einstellen und 
    
    Geschwindigkeitsänderungen werden über das Objekt "6083h.0h profile acceleration" übernommen (siehe `SetAcc`). 
    Wenn die Richtung geändert wird (z.B. von positiver zu negativer Geschwindigkeit), wird das Objekt 
    "6085h.0h quickstop deceleration" verwendet, bis die Geschwindigkeit Null ist, 
    dann wird 6083h.0h verwendet, um in die entgegengesetzte Richtung zu beschleunigen. 
    
    Der Verzögerungsparameter hat keinen Einfluss. 

    :param targetVelocity: neue Zielgeschwindigkeit [integer32]
    :type targetVelocity: int
    """
    pass

def SetTargetPos(targetPos : int):
    """Shortcut zum Schreiben des Objekts "607Ah.0h target position"

    :param targetPos: neue Zielposition [integer32]
    :type targetPos: int
    """
    pass

def SetPosVel(profileVelocity : int):
    """Shortcut zum Schreiben des Objekts "6081h.0h profile velocity"

    :param profileVelocity: neue Profil-Geschwindigkeit [unsigned32]
    :type profileVelocity: int
    """
    pass

def SetAcc(profileAcceleration : int):
    """Shortcut zum Schreiben des Objekts "6083h.0h profile acceleration"

    :param profileAcceleration: neue Profilbeschleunigung [unsigned32]
    :type profileAcceleration: int
    """
    pass

def SetDec(profileDeceleration : int):
    """Shortcut zum Schreiben des Objekts "6084h.0h profile deceleration"

    :param profileDeceleration: neue Profilverzögerung [unsigned32]
    :type profileDeceleration: int
    """
    pass

def GoHome(method : int, velocity : int, acceleration : int, offset : int):
    """Start DS402 Referenzfahrt/Homing Run

    * Umschalten auf Betriebsmodus 6 - Profilgeschwindigkeitsmodus (SetOpMode(3))
    * Setzen der Objekte 6098h.0h Referenzfahrtmethode, 6099h.1h Referenzfahrtgeschwindigkeit, 609Ah.0h Referenzfahrtbeschleunigung und 607Ch.0h Referenzfahrtoffset
    * Start der Bewegung 
    
    Kommende `Methode` Werte für MovingCap sind: 
    * 37 oder 35 = nicht bewegen. Aktuelle Istposition als neue Nullposition setzen. 
    * -18 = Satzreferenzfahrt in positiver Richtung
    * -19 = Satzreferenzfahrt in negativer Richtung
    
    Verwenden Sie `ChkReady` und `ChkError`, um auf das Ende der Referenzfahrt zu warten und Fehler während der Fahrt zu erkennen. 

    :param Methode: DS402 Referenzfahrtmethode [unsigned8]
    :Typ Methode: int
    :param velocity: Referenzfahrt-Geschwindigkeit [unsigned32]
    :type velocity: int
    :param acceleration: Homing acceleration [unsigned32]
    :Typ Beschleunigung: int
    :param offset: Offset-Position der Referenzfahrt [integer32]. Nach erfolgreicher Referenzfahrt wird dieser Positionswert 
        Wert zur neuen Ist-Position. 
    :Typ Versatz: int
    """
    pass

def SetOpMode(opMode: int):
    """Shortcut zum Schreiben des Objekts "6060h.0h modes of operation"

    :param opMode: neue Betriebsart [unsigned8]: 0 - kein Modus. 1 - Profilpositionsmodus. 3 - Profilgeschwindigkeitsmodus. 6 - Referenzfahrt-Modus.
    :Typ opMode: int
    """
    pass

def GetOpMode() -> int:
    """Shortcut zum Lesen des Objekts "6060h.0h modes of operation"

    :return: Betriebsart [unsigned8], siehe `SetOpMode`
    :rtype: int
    """
    opMode = 0
    return opMode

def SetTorque(torque : int):
    """Shortcut zum Schreiben des Objekts "6073h.0h max current"

    :param torque: neuer max. Stromwert [unsigned16], der sich direkt auf das maximale Drehmoment im Betrieb bezieht. 
        Die Einheit des Wertes ist 0,1%, d.h. Drehmoment = 100 bedeutet "10% Drehmoment" und Drehmoment = 1000 bedeutet "100% Drehmoment" (Standard).
    :Typ Drehmoment: int
    """
    pass

def ChkIn(inNo : int) -> int:
    """Digitalen Eingang prüfen

    :param inNo: Eingangs-Nr. von 1..8 (je nach MovingCap-Modell)
    :Typ inNo: int
    :return: 0 wenn niedrig. 1 wenn high (aktiv)
    :rtype: int
    """
    pass

def SetOut(outNo : int):
    """Digitalen Ausgang setzen/aktivieren

    :param outNo: Ausgangsnummer von 1..4 (je nach MovingCap-Modell)
    :Typ outNo: int
    """
    pass

def ClearOut(outNo : int):
    """Digitalen Ausgang zurücksetzen/deaktivieren

    :param outNo: Ausgangsnummer von 1..4 (je nach MovingCap-Modell)
    :Typ outNo: int
    """
    pass

def GetActualPos() -> int:
    """Shortcut zum Lesen des Objekts "6064h.0h Positions-Istwert"

    :return: aktuelle Position [integer32]
    :rtype: int
    """
    aktuellePosition = 0
    return actualPos

def ReadStatusword() -> int:
    """Shortcut zum Lesen des Objekts "6041h.0h statusword"

    :return: DS402 statusword Wert [unsigned16]
    :rtype: int
    """
    statusWort = 0
    return statusWord


def ChkReady() -> int:
    """Prüfen, ob der Antrieb die aktuelle Bewegung beendet hat (statusword "Ziel erreicht" Bit ist gesetzt), 
    oder ein Fehler aufgetreten ist ("error"-Bit ist gesetzt).

    Verwenden Sie dies nach einem neuen `GoPosAbs`, `GoPosRel` oder `GoHome` Aufruf. 

    :Rückgabe: 1 wenn bereit. 0 wenn (noch) nicht bereit.
    :rtype: int
    """
    isReady = 0
    return isReady

def ChkError() -> int:
    """Prüfen, ob das Statusword "error" Bit gesetzt ist.

    :return: 1 wenn Fehler. 0, wenn kein Fehler.
    :rtype: int
    """   
    isError = 0
    return isError

def ChkMfrStatus(bitIndex : int) -> int:
    """Prüfe ein bestimmtes Bit aus dem Objekt 1002h.0h manufacturer status register.

    MovingCap Ethernet-Fehlerbits verfügbar:
    0 Fehler über Volt (Uzk)
    1 Fehler unter Volt (Uzk)
    2 Fehler Ack
    3 Fehler über Temp
    4 Fehler I2T / Derating
    5 Abbruch der Verbindung
    6 Fehler Hub
    7 Fehler Kommunikation
    8 Fehler Sensor
    9 Fehler Hardware-Freigabe
    11 Fehler Überstrom
    12 Fehler Externe Kraft/Drehmoment

    :param bitIndex: die Bitnummer von 0..15
    :Typ bitIndex: int
    :return: 1 bei Fehler. 0 wenn kein Fehler.
    :rtype: int
    """
    isError = 0
    return isError 
