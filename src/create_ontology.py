from owlready2 import *
import os

# Ottieni il percorso base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ONTOLOGY_PATH = os.path.join(PROJECT_ROOT, "data", "ontology.owl")

# Crea l'ontologia
onto = get_ontology("http://www.example.org/stampante.owl")

with onto:
    class Componente(Thing):
        pass
    class Estrusore(Componente):
        pass
    class Piatto(Componente):
        pass
    class Elettronica(Componente):
        pass
    
    class Guasto(Thing):
        pass
    class EstrusoreOstruito(Guasto):
        pass
    class PiattoNonLivellato(Guasto):
        pass
    class Surriscaldamento(Guasto):
        pass
    class CavoInterrotto(Guasto):
        pass
    
    class Sintomo(Thing):
        pass
    class FilamentoNonEsce(Sintomo):
        pass
    class PrimoStratoNonAderisce(Sintomo):
        pass
    class TemperaturaInstabile(Sintomo):
        pass
    class RumoreStrano(Sintomo):
        pass
    
    # Proprietà
    class ha_sintomo(Guasto >> Sintomo):
        pass
    class composto_da(Componente >> Componente):
        pass
    class affligge(Guasto >> Componente):
        pass

# Crea la directory se non esiste e salva
os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)
onto.save(file = ONTOLOGY_PATH, format = "rdfxml")

print(f"Ontologia salvata in {ONTOLOGY_PATH}")