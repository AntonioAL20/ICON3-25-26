from owlready2 import *
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)

def build_advanced_ontology():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    onto_path = os.path.join(base_dir, "..", "data", "stampante3d_inferred.owl")
    
    onto = get_ontology("http://www.di.uniba.it/icon/stampante3d.owl")

    with onto:
        # --- CLASSI BASE ---
        class EntitaDiagnostica(Thing): pass
        class Componente(EntitaDiagnostica): pass
        class Sintomo(EntitaDiagnostica): pass

        # --- OBJECT PROPERTIES ---
        class ha_sottocomponente(ObjectProperty, TransitiveProperty):
            domain = [Componente]; range = [Componente]
        
        class parte_di(ObjectProperty):
            domain = [Componente]; range = [Componente]
            inverse_property = ha_sottocomponente

        class coinvolge_componente(ObjectProperty):
            domain = [Sintomo]; range = [Componente]

        # --- TASSONOMIA COMPONENTI ---
        class ComponenteElettrico(Componente): pass
        class ComponenteMeccanico(Componente): pass
        class ComponenteTermico(Componente): pass
        class StrutturaMeccanica(ComponenteMeccanico): pass

        class MotoreStepper(ComponenteMeccanico, ComponenteElettrico): pass
        class Termistore(ComponenteTermico, ComponenteElettrico): pass
        class Ugello(ComponenteMeccanico, ComponenteTermico): pass
        class PiattoRiscaldato(ComponenteTermico, ComponenteElettrico): pass
        class SchedaMadre(ComponenteElettrico): pass
        class Finecorsa(ComponenteElettrico, ComponenteMeccanico): pass
        class Ventola(ComponenteElettrico, ComponenteMeccanico): pass
        class Cinghia(ComponenteMeccanico): pass

        # --- INDIVIDUI (Topologia della Stampante) ---
        extruder_asm = ComponenteMeccanico("GruppoEstrusore")
        asse_x = StrutturaMeccanica("AsseX")
        asse_y = StrutturaMeccanica("AsseY")
        
        motore_e = MotoreStepper("MotoreEstrusore", parte_di=[extruder_asm])
        motore_x = MotoreStepper("MotoreX", parte_di=[asse_x])
        cinghia_x = Cinghia("CinghiaX", parte_di=[asse_x])
        endstop_x = Finecorsa("FinecorsaX", parte_di=[asse_x])
        
        ugello_1 = Ugello("UgelloPrincipale", parte_di=[extruder_asm])
        termistore_hotend = Termistore("TermistoreHotend", parte_di=[extruder_asm])
        ventola_hotend = Ventola("VentolaHotend", parte_di=[extruder_asm])
        
        piatto = PiattoRiscaldato("PiattoDiStampa")
        mainboard = SchedaMadre("SchedaMadrePrincipale")

        # --- RESTRIZIONI LOGICHE (Description Logic) ---
        class AllarmeTermico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteTermico)]
        
        class AllarmeMeccanico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteMeccanico)]
            
        class AllarmeElettrico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteElettrico)]

        # --- SINTOMI ESTESI ---
        Sintomo("TempTroppoAlta", coinvolge_componente=[termistore_hotend])
        Sintomo("TempInstabile", coinvolge_componente=[termistore_hotend])
        Sintomo("PiattoFreddo", coinvolge_componente=[piatto])
        
        Sintomo("TicchettioEstrusore", coinvolge_componente=[motore_e])
        Sintomo("FilamentoNonEsce", coinvolge_componente=[ugello_1])
        Sintomo("SottoEstrusione", coinvolge_componente=[extruder_asm])
        
        Sintomo("LayerSpostati", coinvolge_componente=[motore_x, cinghia_x])
        Sintomo("RumoreCinghia", coinvolge_componente=[cinghia_x])
        Sintomo("HomeFallito", coinvolge_componente=[endstop_x, motore_x])
        
        Sintomo("OdoreBruciato", coinvolge_componente=[mainboard])
        Sintomo("SchermoNero", coinvolge_componente=[mainboard])
        Sintomo("VentolaRumorosa", coinvolge_componente=[ventola_hotend])
        
        Sintomo("Warping", coinvolge_componente=[piatto])

    return onto, onto_path