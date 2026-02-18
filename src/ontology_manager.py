from owlready2 import *
import os

# Ottieni il percorso assoluto della directory che contiene questo script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Risali alla directory principale del progetto (supponendo che src/ sia dentro la root)
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# Costruisci il percorso completo per il file ontology.owl
ONTOLOGY_PATH = os.path.join(PROJECT_ROOT, "data", "ontology.owl")

# Crea una nuova ontologia
onto = get_ontology("http://www.example.org/stampante.owl")

with onto:
    # Definizione classi
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
    
    # Relazioni (proprietà)
    class ha_sintomo(Guasto >> Sintomo):
        pass
    class composto_da(Componente >> Componente):
        pass
    class affligge(Guasto >> Componente):
        pass

    # Individui (esempi concreti)
    estr1 = Estrusore("estrusore_principale")
    piatto1 = Piatto("piatto_principale")
    elettro1 = Elettronica("elettronica_principale")
    
    # Relazioni tra individui
    # (es. l'estrusore è un componente della stampante – non serve una classe stampante, possiamo usare una proprietà)
    # Aggiungiamo una proprietà 'parte_di' inversa? Per semplicità, lasciamo.
    
    # Associazioni guasti-sintomi
    g1 = EstrusoreOstruito("guasto_estrusore_ostruito")
    g1.ha_sintomo.append(FilamentoNonEsce("sintomo_filamento_non_esce"))
    g1.affligge.append(estr1)
    
    g2 = PiattoNonLivellato("guasto_piatto_non_livellato")
    g2.ha_sintomo.append(PrimoStratoNonAderisce("sintomo_primo_strato_non_aderisce"))
    g2.affligge.append(piatto1)
    
    # ... altri guasti e sintomi

# Salva l'ontologia in un file
onto.save(file = ONTOLOGY_PATH, format = "rdfxml")
