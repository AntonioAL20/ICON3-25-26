from owlready2 import *
import warnings

# Disabilitiamo i warning minori di sqlite per output pulito
warnings.filterwarnings("ignore", category=UserWarning)

def build_advanced_ontology():
    """
    Costruisce un'ontologia OWL 2.0 complessa per la diagnostica di stampanti 3D.
    Soddisfa il requisito di "Rappresentazione" del corso ICon introducendo:
    - Gerarchie profonde
    - Object Properties (Transitive e Inverse)
    - Restrizioni logiche (Equivalent To) per l'inferenza automatica
    """
    onto = get_ontology("http://www.di.uniba.it/icon/stampante3d.owl")

    with onto:
        # ==========================================
        # 1. CLASSI BASE E GERARCHIE PROFONDE
        # ==========================================
        class EntitaDiagnostica(Thing): pass
        
        class Componente(EntitaDiagnostica): pass
        class Sintomo(EntitaDiagnostica): pass
        class CategoriaGuasto(EntitaDiagnostica): pass

        # ==========================================
        # 2. PROPRIETÀ COMPLESSE (Object Properties)
        # ==========================================
        class ha_sottocomponente(ObjectProperty, TransitiveProperty):
            """Proprietà transitiva: se A ha sottocomp B, e B ha sottocomp C, A ha sottocomp C"""
            domain = [Componente]
            range = [Componente]
        
        class parte_di(ObjectProperty):
            """Proprietà inversa di ha_sottocomponente"""
            domain = [Componente]
            range = [Componente]
            inverse_property = ha_sottocomponente

        class coinvolge_componente(ObjectProperty):
            domain = [Sintomo]
            range = [Componente]

        # ==========================================
        # 3. TASSONOMIA DEI COMPONENTI
        # ==========================================
        class ComponenteElettrico(Componente): pass
        class ComponenteMeccanico(Componente): pass
        class ComponenteTermico(Componente): pass

        # Ereditarietà multipla
        class MotoreStepper(ComponenteMeccanico, ComponenteElettrico): pass
        class Termistore(ComponenteTermico, ComponenteElettrico): pass
        class Ugello(ComponenteMeccanico, ComponenteTermico): pass

        # Creazione della topologia (Individui)
        extruder_asm = ComponenteMeccanico("GruppoEstrusore")
        motore_e = MotoreStepper("MotoreEstrusore", parte_di=[extruder_asm])
        ugello_1 = Ugello("UgelloPrincipale", parte_di=[extruder_asm])
        termistore_hotend = Termistore("TermistoreHotend", parte_di=[extruder_asm])

        # ==========================================
        # 4. RESTRIZIONI LOGICHE (Per il Reasoner)
        # ==========================================
        # Definizione basata sulle proprietà: Un AllarmeTermico è definito
        # come un qualsiasi sintomo che coinvolge un ComponenteTermico.
        # Questo permette ad HermiT di classificare le istanze automaticamente!
        class AllarmeTermico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteTermico)]
        
        class AllarmeMeccanico(Sintomo):
            equivalent_to = [Sintomo & coinvolge_componente.some(ComponenteMeccanico)]

        # Individui Sintomi Base (RAW) - Senza classificazione esplicita
        s_temp_alta = Sintomo("TempTroppoAlta", coinvolge_componente=[termistore_hotend])
        s_ticchettio = Sintomo("TicchettioEstrusore", coinvolge_componente=[motore_e])
        s_no_filamento = Sintomo("FilamentoNonEsce", coinvolge_componente=[ugello_1])

    return onto

if __name__ == "__main__":
    print("Costruzione dell'ontologia in corso...")
    ontologia = build_advanced_ontology()
    print(f"Ontologia costruita con successo: {len(list(ontologia.classes()))} classi definite.")
