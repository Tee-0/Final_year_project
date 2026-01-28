from mesa import Agent

class UpdateServerAgent(Agent):
    """
    Represents the software update server.

    This agent does not become infected in the SEIR sense.
    Instead, it can be compromised, after which all updates ut didtributes are mailcious until detection occurs

    """

    def __init__(
        self,
        unique_id: int,
        model,
        security_level: float
    ):
        """
        Docstring for __init__
        
        :param self: agent model

        :param unique_id:  Mesa required unique identifier
        :type unique_id: int

        :param model: simulation model.

        :param security_level:  How secure the update server is.
            Higher values mean harder to compromise.
        :type security_level: float
        """
        super().__init__(unique_id, model)

        self.security_level = security_level

        #checks if server been compromised by attacker
        self.is_compromised = False

        # Time step when compromise occurred (for reporting)
        self.compromise_step = None

        def compromise(self, current_step: int):
            """
            Marks the update server as compromised.
            """
        self.is_compromised = True
        self.compromise_step = current_step  

        def step(self):

            """
        Update server behaviour per simulation step.
        For now, the server does nothing actively.
        It simply exists as a stateful object.
        """
            pass