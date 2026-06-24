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
        class StatoOperativo(Thing): pass
        class CategoriaDegrado(Thing): pass
        class TipoCalibrazione(Thing): pass

        # --- TASSONOMIA CONTESTO E DEGRADO ---
        class AmbienteUmido(StatoOperativo): pass
        class AltaVelocita(StatoOperativo): pass
        class UsuraAvanzata(StatoOperativo): pass

        class DegradoMeccanico(CategoriaDegrado): pass
        class DegradoTermico(CategoriaDegrado): pass

        class CalibrazionePID(TipoCalibrazione): pass
        class CalibrazioneStep(TipoCalibrazione): pass

        # --- TASSONOMIA COMPONENTI HARDWARE ---
        class ComponenteElettrico(Componente): pass
        class ComponenteMeccanico(Componente): pass
        class ComponenteTermico(Componente): pass
        class StrutturaMeccanica(ComponenteMeccanico): pass
        class Sensore(ComponenteElettrico): pass

        class MotoreStepper(ComponenteMeccanico, ComponenteElettrico): pass
        class Termistore(ComponenteTermico, Sensore): pass
        class Ugello(ComponenteMeccanico, ComponenteTermico): pass
        class PiattoRiscaldato(ComponenteTermico, ComponenteElettrico): pass
        class SchedaMadre(ComponenteElettrico): pass
        class Finecorsa(ComponenteElettrico, ComponenteMeccanico): pass
        class Ventola(ComponenteElettrico, ComponenteMeccanico): pass
        class Cinghia(ComponenteMeccanico): pass
        class Accelerometro(Sensore): pass

        # --- OBJECT PROPERTIES ---
        class ha_sottocomponente(ObjectProperty, TransitiveProperty):
            domain = [Componente]; range = [Componente]
        
        class parte_di(ObjectProperty):
            domain = [Componente]; range = [Componente]
            inverse_property = ha_sottocomponente

        class coinvolge_componente(ObjectProperty):
            domain = [Sintomo]; range = [Componente]

        class sensibile_a(ObjectProperty):
            domain = [EntitaDiagnostica]; range = [StatoOperativo]

        class aggravato_da(ObjectProperty):
            domain = [Sintomo]; range = [StatoOperativo]

        class alimentato_da(ObjectProperty):
            domain = [Componente]; range = [Componente]

        class conseguenza_di(ObjectProperty, TransitiveProperty):
            domain = [Sintomo]; range = [Sintomo]

        class soggetto_a_degrado(ObjectProperty):
            domain = [Componente]; range = [CategoriaDegrado]

        class misurato_da(ObjectProperty):
            domain = [Sintomo]; range = [Sensore]

        class richiede_calibrazione(ObjectProperty):
            domain = [Componente]; range = [TipoCalibrazione]

        # --- ISTANZE DI CONTESTO (ABox) ---
        config_umido = AmbienteUmido("ContestoAmbienteUmido")
        config_veloce = AltaVelocita("ContestoAltaVelocita")
        config_usura = UsuraAvanzata("ContestoUsuraAvanzata")

        degrado_mecc = DegradoMeccanico("ProfiloDegradoMeccanico")
        degrado_term = DegradoTermico("ProfiloDegradoTermico")
        
        cal_pid = CalibrazionePID("RoutinePID_Termica")
        cal_step = CalibrazioneStep("RoutineStep_Meccanica")

        # --- ISTANZE HARDWARE E TOPOLOGIA (ABox) ---
        extruder_asm = ComponenteMeccanico("GruppoEstrusore")
        asse_x = StrutturaMeccanica("AsseX")
        
        mainboard = SchedaMadre("SchedaMadrePrincipale")
        piatto = PiattoRiscaldato("PiattoDiStampa")
        
        motore_e = MotoreStepper("MotoreEstrusore", parte_di=[extruder_asm])
        motore_x = MotoreStepper("MotoreX", parte_di=[asse_x])
        cinghia_x = Cinghia("CinghiaX", parte_di=[asse_x])
        endstop_x = Finecorsa("FinecorsaX", parte_di=[asse_x])
        sensore_vib = Accelerometro("AccelerometroAsseX", parte_di=[asse_x])
        
        ugello_1 = Ugello("UgelloPrincipale", parte_di=[extruder_asm])
        termistore_hotend = Termistore("TermistoreHotend", parte_di=[extruder_asm])
        ventola_hotend = Ventola("VentolaHotend", parte_di=[extruder_asm])

        # --- ASSERZIONI LOGICHE (RETE ELETTRICA, DEGRADO E CALIBRAZIONI) ---
        motore_e.alimentato_da = [mainboard]
        motore_x.alimentato_da = [mainboard]
        piatto.alimentato_da = [mainboard]
        termistore_hotend.alimentato_da = [mainboard]
        ventola_hotend.alimentato_da = [mainboard]
        endstop_x.alimentato_da = [mainboard]
        sensore_vib.alimentato_da = [mainboard]

        cinghia_x.soggetto_a_degrado = [degrado_mecc]
        motore_x.soggetto_a_degrado = [degrado_mecc]
        motore_e.soggetto_a_degrado = [degrado_mecc]
        termistore_hotend.soggetto_a_degrado = [degrado_term]
        ugello_1.soggetto_a_degrado = [degrado_term]

        termistore_hotend.richiede_calibrazione = [cal_pid]
        piatto.richiede_calibrazione = [cal_pid]
        motore_x.richiede_calibrazione = [cal_step]
        motore_e.richiede_calibrazione = [cal_step]

        # --- RESTRIZIONI LOGICHE AVANZATE ---
        class AllarmeTermico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteTermico)]
        
        class AllarmeMeccanico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteMeccanico)]
            
        class AllarmeElettrico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteElettrico)]

        class AllarmeAdesioneIgroscopica(Sintomo):
            equivalent_to = [Sintomo & aggravato_da.some(AmbienteUmido)]

        class AllarmeCriticoUsura(Sintomo):
            equivalent_to = [Sintomo & aggravato_da.some(UsuraAvanzata)]

        # --- POPOLAMENTO SINTOMI ---
        s_alta_temp = Sintomo("TempTroppoAlta", coinvolge_componente=[termistore_hotend], misurato_da=[termistore_hotend])
        s_inst_temp = Sintomo("TempInstabile", coinvolge_componente=[termistore_hotend], aggravato_da=[config_usura])
        s_piatto_fr = Sintomo("PiattoFreddo", coinvolge_componente=[piatto])
        
        s_ticchettio = Sintomo("TicchettioEstrusore", coinvolge_componente=[motore_e])
        s_no_filam = Sintomo("FilamentoNonEsce", coinvolge_componente=[ugello_1])
        s_sotto_est = Sintomo("SottoEstrusione", coinvolge_componente=[extruder_asm])
        
        s_layer_sp = Sintomo("LayerSpostati", coinvolge_componente=[motore_x, cinghia_x], aggravato_da=[config_veloce, config_usura], misurato_da=[sensore_vib])
        s_rum_cingh = Sintomo("RumoreCinghia", coinvolge_componente=[cinghia_x], aggravato_da=[config_usura], misurato_da=[sensore_vib])
        s_home_fall = Sintomo("HomeFallito", coinvolge_componente=[endstop_x, motore_x])
        
        s_bruciato = Sintomo("OdoreBruciato", coinvolge_componente=[mainboard])
        s_scr_nero = Sintomo("SchermoNero", coinvolge_componente=[mainboard])
        s_vent_rum = Sintomo("VentolaRumorosa", coinvolge_componente=[ventola_hotend])
        
        s_warping = Sintomo("Warping", coinvolge_componente=[piatto], aggravato_da=[config_umido])

        # Catena Causale
        s_ticchettio.conseguenza_di = [s_no_filam] 
        s_sotto_est.conseguenza_di = [s_ticchettio] 

    return onto, onto_path