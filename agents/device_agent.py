import random
from mesa import Agent

class DeviceAgent(Agent):
    """
    Represents an end-user device that installs
    software updates and may become infected
    """

    def __init__(
        self,
        unique_id: int,
        model,
        trust_score: float,
        defence_level: float
    ):
        """Initialize a device agent."""
        super().__init__(unique_id, model) 
        
        # SEIR States
        self.state = "S"

        self.trust_score = trust_score      # 0-1
        self.defence_level = defence_level  # 0-1

        # Timestamps 
        self.exposed_step = None
        self.infected_step = None
        
        # For rollout control
        self.can_check_updates_this_step = False

    def receive_update(self):
        """
        Device checks the update server.
        If compromised, device may download a malicious update.
        """
        # Only check for updates if eligible this step
        if not self.can_check_updates_this_step:
            return 
        
        server = self.model.update_server  

        if self.state == "S" and server.is_compromised:
            if random.random() < self.trust_score: 
                self.state = "E"
                self.exposed_step = self.model.current_step

    def execute_malware(self):
        """
        Exposed devices may execute the malware.
        """
        if self.state == "E":
            # Use model's execution probability parameter
            if random.random() < self.model.execution_probability:
                self.state = "I"
                self.infected_step = self.model.current_step
              
    def detect_and_recover(self):
        """
        Infected devices may detect and remove malware after detection delay.
        """
        if self.state == "I":
            # Check if enough time has passed since infection
            if self.infected_step is not None:
                steps_since_infection = self.model.current_step - self.infected_step
                
                # Only try to detect after the detection delay
                if steps_since_infection >= self.model.detection_delay:
                    # Detection probability based on defence level
                    if random.random() < self.defence_level:
                        self.state = "R"
                   
    def step(self):
        """
        Device behaviour per update cycle.
        
        CRITICAL: State transitions are mutually exclusive per step.
        A device can only change state ONCE per step to maintain
        temporal realism and prevent instantaneous S→E→I→R progression.
        """
        
        # Priority 1: Check for recovery (if infected and enough time passed)
        if self.state == "I":
            self.detect_and_recover()
            return  # Done for this step
        
        # Priority 2: Try to execute malware (if exposed)
        if self.state == "E":
            self.execute_malware()
            return  # Done for this step
        
        # Priority 3: Check for updates (if susceptible)
        if self.state == "S":
            self.receive_update()
            return  # Done for this step
        
        # If state is R, device does nothing (already recovered)