"""Bibliothèque d'entraînement stub/interface pour les servo drives fullmo MovingCap

La bibliothèque d'entraînement permet l'accès au dictionnaire d'objets MovingCap DS402/CiA402 pour des
des scripts micropython qui peuvent être chargés et exécutés sur les lecteurs Ethernet MovingCap 
(MC349 ETH ou MCN23 ETH).

* WriteObject et ReadObject fournissent un accès général à tous les objets disponibles du 
dictionnaire des lecteurs de MovingCap. Si vous êtes familier avec les objets standard DS402/CiA402 
DS402/CiA402 et les objets spécifiques au fabricant comme documenté dans le manuel de l'utilisateur de MovingCap, c'est tout ce dont vous avez besoin pour écrire un dictionnaire complet.
est tout ce dont vous avez besoin pour écrire une application complète de drive master. 

* Les fonctions supplémentaires sont fournies comme un raccourci et un moyen plus rapide d'écrire vos applications.
Elles effectuent essentiellement plusieurs opérations d'écriture/lecture sur les objets DS402/CiA402 pour la fonctionnalité souhaitée.
la fonctionnalité souhaitée. Veuillez vous référer à nos exemples pour voir comment faire fonctionner votre lecteur avec quelques lignes de code seulement.
en mouvement avec quelques lignes de code seulement.
"""
__author__ = "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.05.xxx"
__date__ = "2023-03-09"

def WriteObject(index : int, subindex : int, value : int) -> int :
    """Ecriture de la valeur d'un objet CANopen (uniquement numérique)

    :param index : Index CANopen [unsigned16], par exemple 0x607A pour "target position".
    :type index : int
    :param subindex : Sous-index CANopen [unsigned8], par exemple 0
    :type subindex : int
    :param value : nouvelle valeur de l'objet [integer32].
    :type value : int
    :return : 0 en cas de succès, ou le code d'erreur interne de la pile CANopen.
        Vous pouvez généralement ignorer cette valeur. Vérifiez uniquement lorsque vous n'êtes pas sûr 
        si l'index/sous-index est un objet valide pour l'accès en écriture. 
    :rtype : int
    """
    ret = 0
    return ret

def ReadObject(index : int, subindex : int) -> int :
    """Lire la valeur d'un objet CANopen (uniquement numérique)

    :param index : Index CANopen [unsigned16], par exemple 0x6064 pour "position effective value".
    :type index : int
    :param subindex : Sous-index CANopen [unsigned8], par exemple 0
    :type subindex : int
    :return : valeur actuelle de l'objet [integer32]. Si l'objet n'est pas un objet valide pour l'accès en lecture,
        une valeur d'erreur interne à la pile CANopen est retournée. Notez que la valeur de retour est toujours integer32,
        même si l'entrée du dictionnaire d'objets a un type de données CANopen différent. 
    :rtype : int
    """
    valeur = 0
    retourne la valeur

def WriteControl(control : int) :
    """Ecriture du mot de contrôle de la DS402 (objet CANoypen 6040h.0h)

    :param control : nouvelle valeur [unsigned8] :type control : int.
    :type control : int
    """
    passe


def EnableDrive() :
    """Préparez le fonctionnement. 
    
    Cette fonction passe par les états requis de la machine d'état de la DS402,
    jusqu'à ce que "fonctionnement activé" soit atteint. 
    
    Ceci est équivalent à la vérification du mot d'état du lecteur
    via `ReadStatusword` et de commander les changements d'état requis en utilisant la fonction 
    `WriteControl`. La séquence est la suivante :

    * Si le variateur est en état d'erreur : WriteControl(0x80) réinitialisation de l'erreur -> nouvel état "interrupteur désactivé".
    * WriteControl(0x6) shutdown -> nouvel état "ready to switch on" (prêt à démarrer)
    * WriteControl(0x7) switch on -> nouvel état "switched on" (allumé)
    * WriteControl(0xf) enable operation -> nouvel état "operation enabled".
    
    Seules les transitions nécessaires sont effectuées. Si le variateur se trouve déjà dans l'état "operation enabled" (ReadStatusword est égal à 0x7).
    (ReadStatusword est 0x27), la fonction revient immédiatement.

    Voir aussi `PowerQuit`.

    Retour : 1 si le passage à l'état "operation enabled" est réussi. 0 si échec.
    :rtype : int
    """
    valeur = 0
    retourne la valeur

def StopMotion() :
    """Commande un arrêt rapide ("ralentir sur la rampe d'option d'arrêt rapide"). 
    Utilise l'objet 6085h.0h valeur de décélération du quickstop. 
    """
    passe

def PowerQuit() :
    """Remet le mode de fonctionnement à zéro (voir `SetOpMode`), 
    puis fait basculer la machine d'état de la DS402 sur "switch on disabled". 

    Voir aussi `EnableDrive`.
    """
    pass

def GoPosAbs(targetPos : int) :
    """Commence un nouveau mouvement vers une position absolue.

    * Si nécessaire, passer en mode d'opération 1 - mode de positionnement du profil (SetOpMode(1))
    * Définissez la nouvelle cible (voir `SetTargetPos`)
    * Démarrez le positionnement en utilisant le mode DS402 "point de consigne unique" : la nouvelle position cible est traitée immédiatement.

    La commande de positionnement utilise "6083h.0h accélération de profil" (`SetAcc`) et 
    "6084h.0h profil décélération" (`SetDec`) pour le mouvement. 

    Utilisez `ChkReady` et `ChkError` pour attendre la fin du positionnement et détecter les erreurs pendant l'exécution. 

    Voir aussi 'GoPosRel'.

    :param targetPos : nouvelle position absolue [integer32]
    :type targetPos : int
    """
    pass

def GoPosRel(relativePos : int) :
    """Commence un nouveau mouvement vers une position relative.

    Identique à `GoPosAbs`, mais spécifie une position relative. 

    Par défaut, "relative" signifie "relative à la position cible précédente utilisée", 
    mais l'objet "60F2h.0h code d'option de positionnement" peut spécifier une autre 
    signification différente, par exemple "relative à la position réelle actuelle".

    :param relativePos : nouvelle position cible relative [integer32]
    :type relativePos : int
    """
    passe

def GoVel(targetVelocity : int) :
    """Lance une nouvelle opération à vitesse constante.

    * Si nécessaire, basculez vers le mode d'opération 3 - mode vitesse du profil (SetOpMode(3)).
    * Définir la nouvelle vitesse cible et 
    
    Les changements de vitesse sont appliqués en utilisant l'objet "6083h.0h profile acceleration" (voir `SetAcc`). 
    Si la direction est modifiée (par exemple, d'une vitesse positive à une vitesse négative), l'objet 
    "6085h.0h décélération rapide" est utilisé jusqu'à ce que la vitesse soit nulle, 
    puis 6083h.0h est appliqué pour accélérer dans la direction opposée. 
    
    Le paramètre de décélération n'a aucune influence. 

    :param targetVelocity : nouvelle vitesse cible [integer32]
    :type targetVelocity : int
    """
    passe

def SetTargetPos(targetPos : int) :
    """Raccourci pour l'écriture de l'objet "607Ah.0h target position".

    :param targetPos : nouvelle position cible [integer32]
    :type targetPos : int
    """
    passe

def SetPosVel(profileVelocity : int) :
    """Raccourci pour écrire l'objet "6081h.0h profile velocity"".

    :param profileVelocity : nouvelle vélocité du profil [unsigned32]
    :type profileVelocity : int
    """
    passe

def SetAcc(profileAcceleration : int) :
    """Raccourci pour écrire l'objet "6083h.0h profil accélération"".

    :param profileAcceleration : nouveau profil d'accélération [unsigned32].
    :type profileAcceleration : int
    """
    passe

def SetDec(profileDeceleration : int) :
    """Raccourci pour écrire l'objet "6084h.0h profil décélération"".

    :param profileDeceleration : nouveau profil de décélération [unsigned32].
    :type profileDeceleration : int
    """
    passe

def GoHome(method : int, velocity : int, acceleration : int, offset : int) :
    """Lance la course de référencement/hébergement du DS402

    * Passage au mode de fonctionnement 6 - mode vitesse du profil (SetOpMode(3))
    * Définir les objets 6098h.0h méthode de référencement, 6099h.1h vitesse de référencement, 609Ah.0h accélération de référencement et 607Ch.0h offset de référencement.
    * Démarrer le mouvement 
    
    Les valeurs de `méthode` pour MovingCap sont : 
    * 37 ou 35 = ne pas bouger. Définir la position réelle actuelle comme nouvelle position zéro. 
    -18 = Blocage de la référence dans le sens positif.
    -19 = bloc de référence exécuté dans le sens négatif.
    
    Utilisez `ChkReady` et `ChkError` pour attendre la fin de la course de recherche et détecter les erreurs pendant la course. 

    :param method : DS402 homing method [unsigned8] (méthode de recherche d'origine DS402)
    :type method : int
    :param velocity : Homing velocity [unsigned32] :type velocity : int
    :type velocity : int
    :param acceleration : Homing acceleration [unsigned32] :type acceleration : int
    :type acceleration : int
    :param offset : Position d'origine de l'orientation [integer32]. Après une opération de retour à la position initiale réussie, cette 
        cette valeur de position comme la nouvelle position réelle. 
    :type offset : int
    """
    passe

def SetOpMode(opMode : int) :
    """Raccourci pour l'écriture de l'objet "6060h.0h modes de fonctionnement"".

    :param opMode : nouveau mode de fonctionnement [unsigned8] : 0 - aucun mode. 1 - mode position du profil. 3 - mode vitesse du profil. 6 - mode de retour à la base.
    :type opMode : int
    """
    passe

def GetOpMode() -> int :
    """Raccourci pour lire l'objet "6060h.0h modes d'opération"".

    :return : mode de fonctionnement [unsigned8], voir `SetOpMode`.
    :rtype : int
    """
    opMode = 0
    return opMode

def SetTorque(torque : int) :
    """Raccourci pour écrire l'objet "6073h.0h max current"".

    :param torque : nouvelle valeur de courant maximum [unsigned16], qui est directement en relation avec le couple maximum pendant le fonctionnement. 
        L'unité de valeur est de 0,1%, c'est-à-dire que couple = 100 signifie "10% de couple" et couple = 1000 signifie "100% de couple" (par défaut).
    :type couple : int
    """
    passe

def ChkIn(inNo : int) -> int :
    """Vérifier l'entrée numérique

    :param inNo : N° d'entrée de 1..8 (selon le modèle MovingCap)
    :type inNo : int
    :return : 0 si faible. 1 si haut (actif)
    :rtype : int
    """
    passe

def SetOut(outNo : int) :
    """Configurer/Activer la sortie numérique

    :param outNo : Numéro de sortie de 1..4 (selon le modèle MovingCap)
    :type outNo : int
    """
    passe

def ClearOut(outNo : int) :
    """Réinitialiser/désactiver la sortie numérique

    :param outNo : N° de sortie de 1..4 (selon le modèle MovingCap)
    :type outNo : int
    """
    passe

def GetActualPos() -> int :
    """Raccourci pour lire la valeur réelle de la position de l'objet "6064h.0h".

    :return : position réelle [integer32]
    :rtype : int
    """
    actualPos = 0
    return actualPos

def ReadStatusword() -> int :
    """Raccourci pour lire l'objet "6041h.0h statusword"".

    :return : Valeur du mot d'état de la DS402 [unsigned16].
    :rtype : int
    """
    statusWord = 0
    return statusWord


def ChkReady() -> int :
    """Vérifier si l'entraînement a terminé le mouvement en cours (le bit statusword "target reached" est activé), 
    ou si une erreur s'est produite (le bit "error" est activé).

    Utilisez ceci après un nouvel appel `GoPosAbs`, `GoPosRel` ou `GoHome`. 

    :return : 1 si prêt. 0 si pas (encore) prêt.
    :rtype : int
    """
    isReady = 0
    return isReady

def ChkError() -> int :
    """Vérifier si le bit "error" du Statusword est activé.

    :return : 1 si erreur. 0 si aucune erreur.
    :rtype : int
    """   
    isError = 0
    return isError

def ChkMfrStatus(bitIndex : int) -> int :
    """Vérifier un bit spécifique du registre d'état du fabricant de l'objet 1002h.0h.

    Bits d'erreur Ethernet MovingCap disponibles :
    0 Erreur sur volt (Uzk)
    1 Erreur sous-volt (Uzk)
    2 Erreur Ack
    3 Erreur sur la température
    4 Erreur I2T / Déclassement
    5 Abandon de la connexion
    6 Erreur de course
    7 Erreur de communication
    8 Erreur Capteur
    9 Erreur Hardware Enable
    11 Erreur de surintensité
    12 Erreur Force externe / Couple

    :param bitIndex : le numéro de bit de 0 à 15
    :type bitIndex : int
    :return : 1 si erreur. 0 si aucune erreur.
    :rtype : int
    """
    isError = 0
    return isError
