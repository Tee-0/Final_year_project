from enum import Enum

class DeviceState(Enum):
    """
    Enumeration representing the malware infection states of an end user device
    Directly implements the S-E-I-R model
    """

    SUSCEPTIBLE = "S"  #Device has not received a compromised update
    EXPOSED = "E" #Device installed compromised update, malware not executed
    INFECTED = "I" #Malware executed, device compromised
    RECOVERED = "R" #Malware detected and removed