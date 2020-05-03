"""Data shared among all writers"""

checked_attributes = set()  # attributes that have been validated
model_resource = None       # not used for now
sim_atts = None             # attribute resource defining the simulation
warning_messages = list()
xml_doc = None              # xml document to be generated
