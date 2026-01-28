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

      super().__init__(unique_id, model) 
      
      #SEIR States
      self.state = "S"

      self.trust_score = trust_score      #0-1
      self.defence_level = defence.level  #0-1

      #timestamps 
      self.exposed_step = None
      self.infected_step = None

      #STEP 1, RECEIVES UPDATE
      def receive_update(self):
         """
         Device checks the update server.
         If compromised, device may download a malicious update
         """
         
      server = self.model.update_server  

      if self.state == "S" and server.is_compromised:
         if random.random() < self.trust_score: 
            self.state = "E"
            self.exposed_step = self.model.current_step

        #Step 2, execute malware
      def execute_malware(self):
          """
          Exposed devices may execute the malware
          """
          if self.state == "E":
            execution_probability = 0.7
          
            if random.random() < execution_probability:
              self.state = "I"
              self.infected_step = self.model.current_step
              
        #step 3- detect and recover
      def detect_and_recover(self):
          """
          Infected devices may detect and remove malware.
          Detection probability:
          defence_level × (1 − trust_score)
          """
          
          if self.state == "I":
               detection_probability = (
                    self.defence_level * (1 - self.trust_score)
               )
                
               if random.random() < detection_probability:
                   self.state = "R"
                   
      def step(self):
        """
        Device behaviour per update cycle.
        """

        self.receive_update()
        self.execute_malware()
        self.detect_and_recover()


                 
           
