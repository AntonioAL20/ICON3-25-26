import os
from owlready2 import *

class OntologyManager:
    def __init__(self, path):
        # Se il percorso è relativo, costruiscilo assoluto rispetto alla posizione del file?
        # Per semplicità, assumiamo che path sia già il percorso corretto
        self.onto = get_ontology(path).load()
    
    def is_valid_class(self, class_name):
        """Verifica se esiste una classe con quel nome nell'ontologia."""
        return class_name in [cls.name for cls in self.onto.classes()]
    
    def get_all_symptoms(self):
        """Restituisce tutte le sottoclassi di Sintomo."""
        sintomo_class = self.onto.Sintomo
        return [cls.name for cls in sintomo_class.subclasses()]
    
    def get_all_faults(self):
        """Restituisce tutte le sottoclassi di Guasto."""
        guasto_class = self.onto.Guasto
        return [cls.name for cls in guasto_class.subclasses()]