from owlready2 import sync_reasoner
import ontology_core

class DiagnosticReasoner:
    """
    Classe che gestisce il ragionamento automatico (Inference).
    Soddisfa il requisito "Ragionamento" di ICon usando la logica descrittiva (DL)
    invece di un semplice pattern matching (if/else).
    """
    def __init__(self, ontology):
        self.onto = ontology
        self.reasoner_run = False

    def run_inference(self):
        """Esegue il reasoner HermiT integrato per materializzare la conoscenza implicita."""
        print("[Reasoner] Avvio di HermiT DL Reasoner...")
        
        # sync_reasoner inferisce le superclassi in base agli assiomi 'equivalent_to'
        # e propaga le proprietà transitive.
        with self.onto:
            sync_reasoner(infer_property_values=True)
            
        self.reasoner_run = True
        print("[Reasoner] Inferenza completata. Conoscenza materializzata.")

    def get_inferred_classes_for_symptom(self, symptom_name):
        """
        Dato un sintomo raw (es. 'TempTroppoAlta'), restituisce tutte le classi
        astratti inferite (es. 'AllarmeTermico') per fare OntoBK.
        """
        if not self.reasoner_run:
            raise RuntimeError("Il reasoner non è stato ancora eseguito!")

        # Cerca l'individuo nell'ontologia
        istanza_sintomo = self.onto.search_one(iri=f"*{symptom_name}")
        
        if not istanza_sintomo:
            return []

        # INDIRECT_is_a contiene le classi inferite dal reasoner
        inferred_classes = [cls.name for cls in istanza_sintomo.INDIRECT_is_a 
                            if hasattr(cls, 'name') and cls.name != "Thing" and cls.name != "Sintomo"]
        
        return inferred_classes

if __name__ == "__main__":
    # Test del modulo standalone
    onto = ontology_core.build_advanced_ontology()
    reasoner = DiagnosticReasoner(onto)
    reasoner.run_inference()
    
    test_symptom = "TempTroppoAlta"
    inferred = reasoner.get_inferred_classes_for_symptom(test_symptom)
    print(f"Sintomo raw: '{test_symptom}' -> Classi inferite dal reasoner: {inferred}")
