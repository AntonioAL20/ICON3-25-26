from owlready2 import *
import os

# Ottieni il percorso base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ONTOLOGY_PATH = os.path.join(PROJECT_ROOT, "data", "ontology.owl")

# Crea l'ontologia
onto = get_ontology("http://www.example.org/stampante.owl")

with onto:
    # ========== CLASSI BASE ==========
    class Componente(Thing):
        pass
    class Guasto(Thing):
        pass
    class Sintomo(Thing):
        pass
    
    # ========== COMPONENTI ==========
    
    # --- Estrusore ---
    class Estrusore(Componente):
        pass
    class IngranaggioConsumato(Guasto):
        pass
    class TuboIntasato(Guasto):
        pass
    class FilamentoSalta(Sintomo):
        pass
    class EstrusioneIntermittente(Sintomo):
        pass
    
    # --- Piatto ---
    class Piatto(Componente):
        pass
    class PiattoNonRiscalda(Guasto):
        pass
    class PiattoSurriscalda(Guasto):
        pass
    class Warping(Sintomo):
        pass
    class TempoRiscaldamentoLungo(Sintomo):
        pass
    
    # --- Elettronica ---
    class Elettronica(Componente):
        pass
    class Surriscaldamento(Guasto):
        pass
    class CavoInterrotto(Guasto):
        pass
    
    # --- Alimentatore ---
    class Alimentatore(Componente):
        pass
    class AlimentatoreGuasto(Guasto):
        pass
    class AlimentatoreInstabile(Guasto):
        pass
    class StampanteNonAccende(Sintomo):
        pass
    class RiavviiCasuali(Sintomo):
        pass
    class LuciIntermittenti(Sintomo):
        pass
    
    # --- Sensore di temperatura ---
    class SensoreTemperatura(Componente):
        pass
    class SensoreRotto(Guasto):
        pass
    class SensoreDeragliato(Guasto):
        pass
    class ErroreTemperatura(Sintomo):
        pass
    class TemperaturaNonStabile(Sintomo):
        pass
    
    # --- Motori passo-passo ---
    class MotorePasso(Componente):
        pass
    class MotoreBloccato(Guasto):
        pass
    class PerditaPassi(Guasto):
        pass
    class StratiSpostati(Sintomo):
        pass
    class RumorePasso(Sintomo):
        pass
    class MovimentoIrregolare(Sintomo):
        pass
    
    # --- Finecorsa  ---
    class Finecorsa(Componente):
        pass
    class FinecorsaGuasto(Guasto):
        pass
    class FinecorsaFalsoContatto(Guasto):
        pass
    class HomeFallito(Sintomo):
        pass
    class Collisione(Sintomo):
        pass
    
    # --- Ventola ---
    class Ventola(Componente):
        pass
    class VentolaBloccata(Guasto):
        pass
    class VentolaRumorosa(Guasto):
        pass
    class SovratemperaturaEstrusore(Sintomo):
        pass
    class StratiDeformati(Sintomo):
        pass
    
    # ========== SINTOMI ==========
    class FilamentoNonEsce(Sintomo):
        pass
    class PrimoStratoNonAderisce(Sintomo):
        pass
    class TemperaturaInstabile(Sintomo):
        pass
    class RumoreStrano(Sintomo):
        pass
    
    # ========== PROPRIETÀ (opzionali, per future estensioni) ==========
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
print("Classi di Sintomo:", [cls.name for cls in onto.Sintomo.subclasses()])
print("Classi di Guasto:", [cls.name for cls in onto.Guasto.subclasses()])