"""drive library stub/interface para servoaccionamientos MovingCap fullmo

La biblioteca de accionamientos permite acceder al diccionario de objetos MovingCap DS402/CiA402 para
scripts de micropython que se pueden cargar y ejecutar en los servoaccionamientos MovingCap Ethernet 
(MC349 ETH o MCN23 ETH).

* WriteObject y ReadObject proporcionan acceso general a todos los objetos disponibles del 
diccionario de unidades de MovingCap. Si está familiarizado con los objetos estándar DS402/CiA402 
estándar DS402/CiA402 y los objetos específicos del fabricante tal y como se documentan en el manual de usuario de MovingCap, esto
es todo lo que necesita para escribir una aplicación maestra de accionamiento completa. 

* Las funciones adicionales se proporcionan como un atajo y una forma más rápida de escribir sus aplicaciones.
Básicamente realizan varias operaciones de escritura/lectura en los objetos DS402/CiA402 para la funcionalidad deseada.
la funcionalidad deseada. Por favor, consulte nuestros ejemplos para ver cómo conseguir que su unidad
en movimiento con sólo unas pocas líneas de código.
"""
__author__ = "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.05.xxx"
__date__ = "2023-03-09"

def WriteObject(index : int, subindex : int, value : int) -> int:
    """Escribir valor de objeto CANopen (sólo numérico)

    :param índice: Índice CANopen [unsigned16], por ejemplo 0x607A para "posición de destino"
    :type índice: int
    :param subíndice: CANopen subíndice [unsigned8], por ejemplo 0
    :type subindex: int
    :param valor: nuevo valor para este objeto [integer32]
    :type valor: int
    :return: 0 si tiene éxito, o el código de error interno de la pila CANopen.
        Normalmente puede ignorar este valor. Compruébelo sólo cuando no esté seguro de 
        si el índice/subíndice es un objeto válido para el acceso de escritura. 
    :rtype: int
    """
    ret = 0
    devolver ret

def LeerObjeto(índice : int, subíndice : int) -> int:
    """Leer valor de objeto CANopen (sólo numérico)

    :param índice: Índice CANopen [unsigned16], por ejemplo 0x6064 para "valor real de posición"
    :type índice: int
    :param subíndice: CANopen subíndice [unsigned8], por ejemplo 0
    :type subindex: int
    :return: valor actual del objeto [integer32]. Si el objeto no es un objeto válido para el acceso de lectura
        se devuelve un valor de error interno de la pila CANopen. Tenga en cuenta que el valor de retorno es siempre integer32,
        incluso si la entrada del diccionario de objetos tiene un tipo de datos CANopen diferente. 
    :rtype: int
    """
    valor = 0
    devolver valor

def EscribirControl(control : int):
    """Escribir palabra de control DS402 (objeto CANoypen 6040h.0h)

    :param control: nuevo valor [unsigned8]
    :type control: int
    """
    pass


def EnableDrive():
    """Preparar para funcionar. 
    
    Esta función cambia a través de los estados requeridos de la máquina de estado DS402
    hasta que se alcanza "operación habilitada". 
    
    Esto es equivalente a comprobar la palabra de estado
    mediante `ReadStatusword` y ordenar los cambios de estado necesarios mediante 
    `WriteControl`. La secuencia es la siguiente

    * Si el accionamiento está en estado de error: WriteControl(0x80) fallo reset -> nuevo estado "encender deshabilitado"
    * WriteControl(0x6) apagado -> nuevo estado "listo para encender".
    * WriteControl(0x7) encendido -> nuevo estado "encendido".
    * WriteControl(0xf) habilitar operación -> nuevo estado "operación habilitada"
    
    Sólo se realizan las transiciones necesarias. Si el accionamiento ya se encuentra en estado "funcionamiento habilitado"
    (ReadStatusword es 0x27), la función vuelve inmediatamente.

    Véase también `PowerQuit`.

    :return: 1 si el cambio a "funcionamiento habilitado" se realiza correctamente. 0 si falla.
    :rtype: int
    """
    valor = 0
    devolver valor

def StopMotion():
    """Ordena un quickstop ("desaceleración en rampa de opción de parada rápida""). 
    Utiliza el objeto 6085h.0h valor de desaceleración quickstop. 
    """
    pass

def PowerQuit():
    """Pone a cero el modo de operación (ver `SetOpMode`), 
    luego cambia la maquina de estado del DS402 a "encendido deshabilitado". 

    Ver también `EnableDrive`.
    """
    pass

def GoPosAbs(targetPos : int):
    """Inicia un nuevo movimiento a una posición absoluta.

    * Si es necesario, cambia al modo de operación 1 - modo de posicionamiento de perfil (SetOpMode(1))
    * Establecer el nuevo objetivo (ver `SetTargetPos`)
    * Inicie el posicionamiento utilizando el modo "consigna única" del DS402: la nueva posición objetivo se procesa inmediatamente.

    El control de posicionamiento utiliza "6083h.0h aceleración de perfil" (`SetAcc`) y 
    "6084h.0h perfil deceleración" (`SetDec`) para el movimiento. 

    Utilice `ChkReady` y `ChkError` para esperar el final del posicionamiento y detectar errores durante la ejecución. 

    Véase también `GoPosRel`.

    :param targetPos: nueva posición objetivo absoluta [integer32]
    :type targetPos: int
    """
    pass

def GoPosRel(relativePos : int):
    """Inicia un nuevo movimiento a la posición relativa.

    Igual que `GoPosAbs`, pero especifica una posición relativa. 

    Por defecto "relative" significa "relativo a la anterior posición objetivo utilizada", 
    pero el objeto "60F2h.0h código de opción de posicionamiento" puede especificar un significado diferente. 
    diferente, por ejemplo, "relativa a la posición real actual".

    :param relativePos: nueva posición objetivo relativa [integer32]
    :type relativePos: int
    """
    pass

def GoVel(objetivoVelocidad : int):
    """Inicia una nueva operación de velocidad constante.

    * Si es necesario, cambia al modo de operación 3 - modo de velocidad de perfil (SetOpMode(3))
    * Establecer nueva velocidad objetivo y 
    
    Los cambios de velocidad se aplican utilizando el objeto "6083h.0h aceleración de perfil" (ver `SetAcc`). 
    Si se cambia la dirección (por ejemplo, de velocidad positiva a negativa), el objeto 
    "6085h.0h desaceleración rápida" hasta que la velocidad sea cero, 
    entonces se aplica 6083h.0h para acelerar en la dirección opuesta. 
    
    El parámetro de deceleración no influye. 

    :paramVelocidadObjetivo: nueva velocidad objetivo [integer32]
    :type velocidadobjetivo: int
    """
    pass

def SetTargetPos(targetPos : int):
    """Atajo para escribir el objeto "607Ah.0h posición objetivo""

    :param targetPos: nueva posición objetivo [integer32]
    :type targetPos: int
    """
    pass

def SetPosVel(perfilVelocidad : int):
    """Atajo para escribir el objeto "6081h.0h velocidad del perfil""

    :param perfilVelocidad: nueva velocidad del perfil [unsigned32]
    :type velocidadPerfil: int
    """
    pass

def SetAcc(perfilAceleración : int):
    """Atajo para escribir el objeto "6083h.0h aceleración del perfil""

    :param perfilAceleración: nueva aceleración del perfil [unsigned32]
    :type aceleracionperfil: int
    """
    pass

def SetDec(perfilDesaceleración : int):
    """Atajo para escribir el objeto "6084h.0h perfil desaceleracion""

    :param perfilDesaceleración: nueva desaceleración del perfil [unsigned32]
    :type perfilDesaceleración: int
    """
    pass

def GoHome(method : int, velocity : int, acceleration : int, offset : int):
    """Inicia la ejecución de referenciación/homing del DS402.

    * Cambiar a modo de operación 6 - modo de velocidad de perfil (SetOpMode(3))
    * Establece los objetos 6098h.0h método de referenciación, 6099h.1h velocidad de referenciación, 609Ah.0h aceleración de referenciación y 607Ch.0h offset de referenciación
    * Inicio del movimiento 
    
    Los valores de `method` para MovingCap son: 
    * 37 o 35 = no mover. Establece la posición real actual como nueva posición cero. 
    -18 = bloque de referencia en dirección positiva.
    -19 = bloque de referencia en dirección negativa
    
    Utiliza `ChkReady` y `ChkError` para esperar a que finalice el recorrido y detectar errores durante el mismo. 

    :param método: DS402 método de homing [unsigned8]
    :type método: int
    :param velocidad: Velocidad de homing [unsigned32]
    :type velocidad: int
    :param aceleración: Aceleración de retorno [unsigned32] :type aceleración: int
    :type aceleración: int
    :param desplazamiento: Posición de retorno [integer32]. Tras una operación de referenciación satisfactoria 
        la nueva posición real. 
    :type offset: int
    """
    pass

def SetOpMode(opMode: int):
    """Atajo para escribir el objeto "6060h.0h modos de operación""

    :param opMode: nuevo modo de operación [unsigned8]: 0 - ningún modo. 1 - modo posición del perfil. 3 - modo velocidad del perfil. 6 - modo homing.
    :type opMode: int
    """
    pass

def GetOpMode() -> int:
    """Acceso directo para leer el objeto "6060h.0h modos de operación""

    :return: modo de operación [unsigned8], ver `SetOpMode`
    :rtype: int
    """
    opMode = 0
    return opMode

def SetTorque(torque : int):
    """Atajo para escribir el objeto "6073h.0h max actual""

    :param par: nuevo valor de corriente máx. [unsigned16], que está directamente en relación con el par máximo durante el funcionamiento. 
        La unidad de valor es 0,1%, es decir, par = 100 significa "10% de par" y par = 1000 significa "100% de par" (por defecto).
    :tipo par: int
    """
    pass

def ChkIn(inNo : int) -> int:
    """Comprobar entrada digital

    :param inNo: Nº entrada de 1..8 (según modelo MovingCap)
    :type inNo: int
    :return: 0 si bajo 1 si es alta (activa)
    :rtype: int
    """
    pass

def SetOut(outNo : int):
    """Establecer/Activar salida digital

    :param outNo: Nº de salida de 1..4 (según modelo MovingCap)
    :type outNo: int
    """
    pass

def ClearOut(outNo : int):
    """Reinicia/desactiva la salida digital

    :param outNo: Nº de salida de 1..4 (según modelo MovingCap)
    :type outNo: int
    """
    pass

def GetActualPos() -> int:
    """Acceso directo para leer el objeto "6064h.0h posición valor real"

    :return: posición real [integer32]
    :rtype: int
    """
    actualPos = 0
    return actualPos

def LeerPalabraEstado() -> int:
    """Acceso directo para leer el objeto "6041h.0h statusword""

    :return: DS402 valor de la palabra de estado [unsigned16]
    :rtype: int
    """
    statusWord = 0
    return palabraEstado


def ChkReady() -> int:
    """"Comprueba si la unidad ha finalizado el movimiento actual (se activa el bit "target reached" de statusword), 
    o se ha producido un error (el bit "error" está activado).

    Úsalo después de una nueva llamada a `GoPosAbs`, `GoPosRel` o `GoHome`. 

    :devolver: 1 si está listo. 0 si no está listo (todavía).
    :rtype: int
    """
    isReady = 0
    return isReady

def ChkError() -> int:
    """"Comprueba si el bit "error" de Statusword está activado.

    :return: 1 si hay error. 0 si no hay error.
    :rtype: int
    """   
    isError = 0
    return isError

def ChkMfrStatus(bitIndex : int) -> int:
    """Comprueba un bit específico del objeto 1002h.0h registro de estado del fabricante.

    MovingCap Bits de error Ethernet disponibles:
    0 Error sobre voltios (Uzk)
    1 Error bajo voltios (Uzk)
    2 Error Ack
    3 Error sobre temp
    4 Error I2T / Derating
    5 Abortar conexión
    6 Error carrera
    7 Error comunicación
    8 Error Sensor
    9 Error Hardware Enable
    11 Error Sobrecorriente
    12 Error Fuerza externa / Par

    :param bitIndex: el número de bit de 0..15
    :type bitIndex: int
    :return: 1 si error. 0 si no hay error.
    :rtype: int
    """
    isError = 0
    return isError
