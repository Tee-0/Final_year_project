import random
from mesa import Agent

class AttackerAgent(Agent) :
    """
    Represents an eternal attacker attempting 
    to compormise the update server
    """
    def __init__(
        self,
        unique_id: int,
        model,
        skill_level: float

    ):
        """
        :param self: Description
        :param unique_id:  Mesa-required ID 
        :type unique_id: int
        :param model: Referencing the model
        :param skill_level: Attacker capability.
            Higher means higher chance of success.
        :type skill_level: float(0-1)
        """

        super().__init__(unique_id, model)

        self.skill_level = skill_level

        #whether the attacker has already succeeeded
        self.attack_successful = False

    def attempt_compromise(self, update_server):
        """
        Attempt to compromise the update server.

        Success probability depends on:
        - attacker skill
        - server security
        """
        
        #if already compromisedd, no need to try again
        if update_server.is_compromised:
            return
        
        #probability model(simple and explainable)
        probability_of_success = (
            self.skill_level * (1 - update_server.security_level)
        )

        #Draw a random number to decide success
        if random.random() < probability_of_success:
            update_server.compromise(self.model.current_step)
            self.attack_successful = True

        def step(self):
            """
            Attacker behaviour per simulation step
            """

            #Only attempt attack if not already successful
            if not self.attack_successful:
                self.attempt_compromise(self.model.update_server)
        