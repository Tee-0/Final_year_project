Overview
This project develops an agent-based simulation model that evaluates how staged and full-push software update rollout strategies affect the scale and impact of malware propagation
in compromised software supply chains — particularly under varying detection delays and device defence capabilities.
The simulation models a three-tier vendor → update server → device architecture using the Mesa agent-based modelling framework in Python. 
Device infection dynamics follow a SEIR (Susceptible–Exposed–Infected–Recovered) state machine, grounded in empirical evidence from the SolarWinds and Kaseya supply chain incidents.
