from owlready2 import *
import os

#percorso base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ONTOLOGY_PATH = os.path.join(PROJECT_ROOT, "data", "ontology.owl")

# Creazione dell'ontologia
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
    
     # --- Display / Interfaccia utente ---
    class Display(Componente):
        pass
    class DisplayGuasto(Guasto):
        pass
    class TouchNonRisponde(Guasto):
        pass
    class SchermoNero(Sintomo):
        pass
    class IconeCongelate(Sintomo):
        pass
    class MessaggiIlleggibili(Sintomo):
        pass
    
    # --- Scheda SD / Supporto di memoria ---
    class SchedaSD(Componente):
        pass
    class SchedaNonRilevata(Guasto):
        pass
    class FileCorrotti(Guasto):
        pass
    class ErroreLetturaSD(Sintomo):
        pass
    class StampaNonAvvia(Sintomo):
        pass
    class LetturaLenta(Sintomo):
        pass
    
    # --- Cablaggio / Connessioni ---
    class Cablaggio(Componente):
        pass
    class ConnettoreAllentato(Guasto):
        pass
    class Cortocircuito(Guasto):
        pass
    class SpegnimentoImprovviso(Sintomo):
        pass
    class OdoreBruciato(Sintomo):
        pass
    class FunzionamentoIntermittente(Sintomo):
        pass
    
    # --- Telaio / Struttura meccanica ---
    class Telaio(Componente):
        pass
    class TelaioDeformato(Guasto):
        pass
    class VitiAllentate(Guasto):
        pass
    class VibrazioniEccessive(Sintomo):
        pass
    class OffsetAssi(Sintomo):
        pass
    class RumoreMeccanico(Sintomo):
        pass
    
    # --- Raffreddamento aggiuntivo (elettronica) ---
    class RaffreddamentoElettronica(Componente):
        pass
    class VentolaElettronicaGuasta(Guasto):
        pass
    class DissipatoreOstruito(Guasto):
        pass
    class SurriscaldamentoDriver(Sintomo):
        pass
    class SpegnimentoTermico(Sintomo):
        pass
    
    # --- Sensore di filamento ---
    class SensoreFilamento(Componente):
        pass
    class SensoreFilamentoGuasto(Guasto):
        pass
    class SensoreFilamentoFalsoAllarme(Guasto):
        pass
    class StampaFerma(Sintomo):
        pass
    class AllarmeContinuo(Sintomo):
        pass
    
    # --- Sensore di livello (BLTouch) ---
    class SensoreLivello(Componente):
        pass
    class SondaBloccata(Guasto):
        pass
    class SondaNonRileva(Guasto):
        pass
    class LivellamentoFallito(Sintomo):
        pass
    class PrimoStratoIrregolare(Sintomo):
        pass
    
    # --- Firmware / Software ---
    class Firmware(Componente):
        pass
    class FirmwareCorrotto(Guasto):
        pass
    class ParametriErrati(Guasto):
        pass
    class ComandiIgnorati(Sintomo):
        pass
    class MovimentiAnomali(Sintomo):
        pass
    class TemperaturaFissa(Sintomo):
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

# Creazione della directory se non esiste e salvataggio
os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)
onto.save(file = ONTOLOGY_PATH, format = "rdfxml")

print(f"Ontologia salvata in {ONTOLOGY_PATH}")
print("Classi di Sintomo:", [cls.name for cls in onto.Sintomo.subclasses()])
print("Classi di Guasto:", [cls.name for cls in onto.Guasto.subclasses()])
