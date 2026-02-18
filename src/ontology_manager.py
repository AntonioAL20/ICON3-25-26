from owlready2 import *
import os

# Ottieni il percorso assoluto della directory che contiene questo script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Risali alla directory principale del progetto (supponendo che src/ sia dentro la root)
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# Costruisci il percorso completo per il file ontology.owl
ONTOLOGY_PATH = os.path.join(PROJECT_ROOT, "data", "ontology.owl")
# Crea la directory se non esiste
os.makedirs(os.path.dirname(ONTOLOGY_PATH), exist_ok=True)


# ---------- DEFINIZIONE DELLA CLASSE PER L'USO NEL PROGRAMMA ----------
class OntologyManager:
    def __init__(self, path):
        self.onto = get_ontology(path).load()

    def is_valid_class(self, class_name):
        """Verifica se esiste una classe con quel nome nell'ontologia."""
        return class_name in self.onto.classes()

    def get_all_symptoms(self):
        """Restituisce tutte le sottoclassi di Sintomo."""
        sintomo_class = self.onto.Sintomo
        return [cls.name for cls in sintomo_class.subclasses()]

    def get_all_faults(self):
        """Restituisce tutte le sottoclassi di Guasto."""
        guasto_class = self.onto.Guasto
        return [cls.name for cls in guasto_class.subclasses()]

# ---------- GENERAZIONE DELL'ONTOLOGIA (eseguita solo se lo script è lanciato direttamente) ----------
if __name__ == "__main__":
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
        
        # Associazioni guasti-sintomi
        g1 = EstrusoreOstruito("guasto_estrusore_ostruito")
        # Nota: devi usare i nomi delle classi sintomo, ma qui stai creando individui? 
        # In realtà ha_sintomo è una proprietà tra Guasto e Sintomo, quindi gli oggetti devono essere individui di Sintomo.
        # Dobbiamo creare individui per i sintomi.
        s1 = FilamentoNonEsce("sintomo_filamento_non_esce")
        s2 = RumoreStrano("sintomo_rumore_strano")
        g1.ha_sintomo.append(s1)
        g1.ha_sintomo.append(s2)
        g1.affligge.append(estr1)
        
        g2 = PiattoNonLivellato("guasto_piatto_non_livellato")
        s3 = PrimoStratoNonAderisce("sintomo_primo_strato_non_aderisce")
        g2.ha_sintomo.append(s3)
        g2.affligge.append(piatto1)
        
        g3 = Surriscaldamento("guasto_surriscaldamento")
        s4 = TemperaturaInstabile("sintomo_temperatura_instabile")
        g3.ha_sintomo.append(s4)
        g3.affligge.append(elettro1)
        
        g4 = CavoInterrotto("guasto_cavo_interrotto")
        s5 = RumoreStrano("sintomo_rumore_strano")  # potrebbe essere lo stesso individuo? Meglio crearne uno nuovo
        g4.ha_sintomo.append(s5)
        g4.affligge.append(elettro1)

# Salva l'ontologia in un file
onto.save(file = ONTOLOGY_PATH, format = "rdfxml")
