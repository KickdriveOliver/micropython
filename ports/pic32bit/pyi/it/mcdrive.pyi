"""stub/interfaccia della libreria di azionamenti per i servoazionamenti fullmo MovingCap

La libreria di azionamenti consente di accedere al dizionario degli oggetti MovingCap DS402/CiA402 per gli
script micropython che possono essere caricati ed eseguiti sui servoazionamenti MovingCap Ethernet (MC349 ETH o MCN23). 
(MC349 ETH o MCN23 ETH).

* WriteObject e ReadObject forniscono un accesso generale a tutti gli oggetti disponibili nel dizionario dei drive di MovingCap. 
MovingCap. Se si ha dimestichezza con gli oggetti standard DS402/CiA402 
e gli oggetti specifici del produttore, come documentato nel manuale d'uso di MovingCap, questo è tutto ciò di cui si ha bisogno per
è tutto ciò che serve per scrivere un'applicazione master completa. 

* Le funzioni aggiuntive sono fornite come scorciatoia e modo più rapido per scrivere le applicazioni.
Esse eseguono essenzialmente diverse operazioni di scrittura/lettura sugli oggetti DS402/CiA402 per ottenere la funzionalità desiderata.
funzionalità desiderate. Per vedere come far funzionare l'unità con poche righe di codice, consultare i nostri esempi.
con poche righe di codice.
"""
__autore__ = "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.05.xxx"
__date__ = "2023-03-09"

def WriteObject(index : int, subindex : int, value : int) -> int:
    """Scrive il valore dell'oggetto CANopen (solo numerico)

    :param indice: indice CANopen [unsigned16], ad esempio 0x607A per "posizione di destinazione"
    :tipo indice: int
    :param subindex: Sottoindice CANopen [unsigned8], ad es. 0
    :tipo subindex: int
    :param value: nuovo valore per questo oggetto [integer32].
    :type value: int
    :return: 0 in caso di successo, oppure il codice di errore interno dello stack CANopen.
        Di solito si può ignorare questo valore. Controllare solo se non si è sicuri 
        se l'indice/sottoindice è un oggetto valido per l'accesso in scrittura. 
    :rtype: int
    """
    ret = 0
    return ret

def ReadObject(index : int, subindex : int) -> int:
    """Lettura del valore dell'oggetto CANopen (solo numerico)

    :param indice: indice CANopen [unsigned16], ad esempio 0x6064 per il "valore effettivo della posizione".
    :tipo indice: int
    :param subindex: Sottoindice CANopen [unsigned8], ad es. 0
    :tipo sottoindice: int
    :return: valore attuale dell'oggetto [integer32]. Se l'oggetto non è un oggetto valido per l'accesso in lettura,
        viene restituito un valore di errore interno allo stack CANopen. Si noti che il valore di ritorno è sempre intero32,
        anche se la voce del dizionario degli oggetti ha un tipo di dati CANopen diverso. 
    :rtype: int
    """
    valore = 0
    valore di ritorno

def WriteControl(control : int):
    """Scrivi la parola di controllo DS402 (oggetto CANoypen 6040h.0h)

    :param controllo: nuovo valore [unsigned8]
    :tipo controllo: int
    """
    pass


def EnableDrive():
    """Prepara il funzionamento. 
    
    Questa funzione passa attraverso gli stati richiesti della macchina a stati DS402,
    finché non viene raggiunto "funzionamento abilitato". 
    
    Ciò equivale a controllare la parola di stato del drive
    tramite `ReadStatusword` e comandare i cambiamenti di stato richiesti tramite 
    `WriteControl`. La sequenza è la seguente:

    * Se l'azionamento è in stato di errore: WriteControl(0x80) reset dell'errore -> nuovo stato "accensione disabilitata"
    * WriteControl(0x6) spegnimento -> nuovo stato "pronto per l'accensione".
    * WriteControl(0x7) switch on -> nuovo stato "acceso".
    * WriteControl(0xf) enable operation -> nuovo stato "operation enabled".
    
    Vengono eseguite solo le transizioni necessarie. Se l'azionamento si trova già nello stato "operation enabled" (ReadStatusword è 0x27).
    (ReadStatusword è 0x27), la funzione ritorna immediatamente.

    Vedere anche `PowerQuit`

    ritorno: 1 se il passaggio a "operation enabled" è riuscito. 0 se non è riuscito.
    :rtype: int
    """
    valore = 0
    return il valore

def StopMotion():
    """Comanda un arresto rapido ("rallenta sulla rampa dell'opzione di arresto rapido"). 
    Utilizza l'oggetto 6085h.0h valore di decelerazione dell'arresto rapido. 
    """
    pass

def PowerQuit():
    """Azzera la modalità operativa (vedere `SetOpMode`), 
    quindi commuta la macchina a stati DS402 in "accensione disabilitata". 

    Vedere anche `EnableDrive`
    """
    pass

def GoPosAbs(targetPos : int):
    """Avvia un nuovo movimento verso una posizione assoluta.

    * Se necessario, passare alla modalità operativa 1 - modalità di posizionamento del profilo (SetOpMode(1))
    * Imposta il nuovo target (vedere `SetTargetPos`).
    * Avviare il posizionamento con la modalità "single setpoint" del DS402: la nuova posizione del target viene elaborata immediatamente.

    Il controllo del posizionamento utilizza "6083h.0h accelerazione profilo" (`SetAcc`) e "6084h.0h accelerazione profilo" (`SetAcc`). 
    "6084h.0h profilo di decelerazione" (`SetDec`) per il movimento. 

    Utilizzare `ChkReady` e `ChkError` per attendere la fine del posizionamento e rilevare gli errori durante l'esecuzione. 

    Vedere anche 'GoPosRel'

    :param targetPos: nuova posizione assoluta di destinazione [integer32]
    :tipo targetPos: int
    """
    pass

def GoPosRel(relativePos : int):
    """Avvia un nuovo movimento verso la posizione relativa.

    Come `GoPosAbs`, ma specifica una posizione relativa. 

    Per impostazione predefinita, "relativo" significa "relativo alla posizione di destinazione utilizzata in precedenza", 
    ma l'oggetto "codice opzione di posizionamento 60F2h.0h" può specificare un significato diverso, ad es. 
    significato diverso, ad esempio "relativo alla posizione attuale".

    :param relativePos: nuova posizione di destinazione relativa [integer32]
    :tipo relativePos: int
    """
    pass

def GoVel(targetVelocity : int):
    """Avvia una nuova operazione a velocità costante.

    * Se necessario, passare alla modalità operativa 3 - modalità velocità del profilo (SetOpMode(3))
    * Imposta la nuova velocità di destinazione e 
    
    Le modifiche alla velocità vengono applicate utilizzando l'oggetto "6083h.0h accelerazione profilo" (vedere `SetAcc`). 
    Se la direzione viene cambiata (ad esempio, da una velocità positiva a una negativa), l'oggetto "6085h.0h accelerazione profilo" viene applicato. 
    "6085h.0h decelerazione quickstop" viene utilizzato finché la velocità non è zero, 
    quindi viene applicato l'oggetto 6083h.0h per accelerare nella direzione opposta. 
    
    Il parametro di decelerazione non ha alcuna influenza. 

    :param targetVelocity: nuova velocità di destinazione [integer32]
    :tipo targetVelocity: int
    """
    pass

def SetTargetPos(targetPos : int):
    """Scorciatoia per scrivere l'oggetto "posizione target 607Ah.0h"

    :param targetPos: nuova posizione del target [integer32]
    :tipo targetPos: int
    """
    pass

def SetPosVel(profileVelocity : int):
    """Scorciatoia per scrivere l'oggetto "6081h.0h profile velocity""

    :param profileVelocity: nuova velocità del profilo [unsigned32]
    :tipo profileVelocity: int
    """
    pass

def SetAcc(profileAcceleration : int):
    """Scorciatoia per scrivere l'oggetto "6083h.0h accelerazione del profilo"

    :param profileAcceleration: nuova accelerazione del profilo [unsigned32]
    :tipo profileAcceleration: int
    """
    pass

def SetDec(profileDeceleration : int):
    """Scorciatoia per scrivere l'oggetto "6084h.0h profile deceleration"

    :param profileDeceleration: nuova decelerazione del profilo [unsigned32]
    :type profileDeceleration: int
    """
    pass

def GoHome(metodo : int, velocità : int, accelerazione : int, offset : int):
    """Avvia la corsa di referenziazione/homing del DS402.

    * Passa alla modalità operativa 6 - modalità velocità del profilo (SetOpMode(3))
    * Imposta gli oggetti 6098h.0h metodo di homing, 6099h.1h velocità di homing, 609Ah.0h accelerazione di homing e 607Ch.0h offset di homing.
    * Avvio del movimento 
    
    I valori del `metodo` di partenza per MovingCap sono: 
    * 37 o 35 = non muoversi. Imposta la posizione attuale come nuova posizione zero. 
    * -18 = blocco del riferimento in direzione positiva
    * -19 = riferimento di blocco eseguito in direzione negativa
    
    Utilizzare `ChkReady` e `ChkError` per attendere la fine della corsa di homing e rilevare gli errori durante la corsa. 

    param metodo: Metodo di homing DS402 [unsigned8]
    :tipo metodo: int
    :param velocity: Velocità di homing [unsigned32]
    :tipo velocity: int
    :param accelerazione: Accelerazione di destinazione [unsigned32]
    :tipo accelerazione: int
    :param offset: Posizione di offset dell'homing [intero32]. Dopo un'operazione di homing riuscita, questo valore di posizione 
        posizione come nuova posizione effettiva. 
    :tipo offset: int
    """
    pass

def SetOpMode(opMode: int):
    """Scorciatoia per scrivere l'oggetto "6060h.0h modalità di funzionamento""

    :param opMode: nuova modalità di funzionamento [unsigned8]: 0 - nessuna modalità. 1 - modalità posizione del profilo. 3 - modalità velocità del profilo. 6 - modalità homing.
    Tipo opMode: int
    """
    pass

def GetOpMode() -> int:
    """Scorciatoia per leggere l'oggetto "6060h.0h modalità di funzionamento""

    :return: modalità di funzionamento [unsigned8], vedi `SetOpMode`
    :rtype: int
    """
    opMode = 0
    return  opMode

def SetTorque(torque : int):
    """Scorciatoia per scrivere l'oggetto "6073h.0h corrente max."

    :param torque: nuovo valore di corrente massima [unsigned16], che è direttamente in relazione alla coppia massima durante il funzionamento. 
        L'unità di misura del valore è 0,1%, cioè coppia = 100 significa "10% di coppia" e coppia = 1000 significa "100% di coppia" (default).
    Tipo coppia: int
    """
    pass

def ChkIn(inNo : int) -> int:
    """Controlla l'ingresso digitale

    :param inNo: numero di ingresso da 1 a 8 (a seconda del modello MovingCap)
    :tipo inNo: int
    :return: 0 se basso. 1 se alto (attivo)
    :rtype: int
    """
    pass

def SetOut(outNo : int):
    """Imposta/Attiva l'uscita digitale

    :param outNo: numero di uscita da 1 a 4 (a seconda del modello MovingCap)
    :type outNo: int
    """
    pass

def ClearOut(outNo : int):
    """Azzeramento/disattivazione dell'uscita digitale

    :param outNo: numero di uscita da 1 a 4 (a seconda del modello MovingCap)
    :type outNo: int
    """
    pass

def GetActualPos() -> int:
    """Scorciatoia per leggere l'oggetto "6064h.0h valore effettivo della posizione""

    :return: posizione effettiva [integer32]
    :rtype: int
    """
    actualPos = 0
    return actualPos

def ReadStatusword() -> int:
    """Scorciatoia per leggere l'oggetto "6041h.0h statusword""

    :return: Valore statusword DS402 [unsigned16]
    :rtype: int
    """
    statusWord = 0
    return statusWord


def ChkReady() -> int:
    """Controlla se l'azionamento ha terminato il movimento corrente (è impostato il bit statusword "target reached"), 
    oppure si è verificato un errore (è impostato il bit "error").

    Utilizzare questa funzione dopo una nuova chiamata a `GoPosAbs`, `GoPosRel` o `GoHome`. 

    ritorno: 1 se è pronto. 0 se non è ancora pronto.
    :rtype: int
    """
    isReady = 0
    return isReady

def ChkError() -> int:
    """Controlla se il bit "error" della Statusword è impostato.

    :return: 1 se c'è un errore. 0 se non ci sono errori.
    :rtype: int
    """   
    isError = 0
    return isError

def ChkMfrStatus(bitIndex : int) -> int:
    """Controlla un bit specifico del registro di stato del produttore dell'oggetto 1002h.0h.

    Bit di errore Ethernet MovingCap disponibili:
    0 Errore sopra volt (Uzk)
    1 Errore sotto volt (Uzk)
    2 Errore Ack
    3 Errore over temp
    4 Errore I2T / Derating
    5 Interruzione connessione
    6 Errore corsa
    7 Errore comunicazione
    8 Errore sensore
    9 Errore Abilitazione hardware
    11 Errore Sovracorrente
    12 Errore Forza esterna / Coppia

    :param bitIndex: il numero di bit da 0..15
    :tipo bitIndex: int
    :return: 1 se errore. 0 se non c'è errore.
    :rtype: int
    """
    isError = 0
    return  isError
