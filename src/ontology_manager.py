import os
from owlready2 import *

class OntologyManager:
    def __init__(self, relative_path):
        # Costruisce il percorso assoluto basato sulla posizione di questo file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)  # risale di un livello (da src a root)
        full_path = os.path.join(project_root, relative_path)
        self.onto = get_ontology(full_path).load()
    
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