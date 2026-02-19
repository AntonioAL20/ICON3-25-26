import sys
from ontology_manager import OntologyManager
from knowledge_base import load_rules, save_rules
from inference import diagnose
from learning import update_probabilities
from induction import RuleInducer

def main():
    # Inizializza
    onto_mgr = OntologyManager("data/ontology.owl")
    rules = load_rules("data/rules_initial.csv")
    inducer = RuleInducer(threshold=2)  # basso per test

    print("=== Sistema Esperto Diagnostico con Ontologia ===")

    # --- Stampa sintomi in 4 colonne ---
    sintomi = onto_mgr.get_all_symptoms()
    sintomi.sort()
    colonne = 4
    larghezza_max = max(len(s) for s in sintomi) + 2  # padding
    righe = (len(sintomi) + colonne - 1) // colonne
    print("Sintomi disponibili:")
    for r in range(righe):
        linea = ""
        for c in range(colonne):
            idx = r + c * righe  # ordine per colonna
            if idx < len(sintomi):
                linea += f"{sintomi[idx]:<{larghezza_max}}"
        print(linea)
    print()  # riga vuota per separazione

    while True:
        sintomi_input = input("\nInserisci i sintomi osservati (separati da virgola): ").strip()
        if not sintomi_input:
            break
        observed = set(s.strip() for s in sintomi_input.split(','))

        # Validazione: i sintomi devono esistere nell'ontologia
        invalid = [s for s in observed if not onto_mgr.is_valid_class(s)]
        if invalid:
            print(f"Sintomi non validi: {invalid}. Riprova.")
            continue

            results, used_rules = diagnose(observed, rules, onto_mgr)
            if not results:
                print("Nessuna diagnosi possibile.")
            else:
                print("\nPossibili guasti:")
                for guasto, prob in sorted(results.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {guasto}: {prob:.2f}")
            
            # Richiedi feedback sempre (anche se non ci sono diagnosi)
            feedback = input("\nQual era il guasto effettivo? (inserisci nome o 'nessuno'): ").strip()
            if feedback == 'nessuno':
                correct = None
            else:
                if not onto_mgr.is_valid_class(feedback):
                    print("Guasto non valido, ignorato.")
                    correct = None
                else:
                    correct = feedback
            
            # Aggiornamento probabilità (solo se ci sono regole usate e il guasto è valido)
            if correct is not None and used_rules:
                rules = update_probabilities(rules, used_rules, correct, observed)
            
            # Induzione: passa l'osservazione (anche se non ci sono regole usate)
            if correct is not None:
                inducer.add_observation(observed, correct, rules)

            # Controlla candidati
            candidates = inducer.get_candidates()
            for sym_set, fault, count in candidates:
                print(f"\nNotata combinazione ricorrente: {sym_set} -> {fault} (occorrenze: {count})")
                ans = input("Aggiungere come nuova regola? (s/n): ").lower()
                if ans == 's':
                    inducer.add_rule_from_candidate(sym_set, fault, rules)
                    print("Regola aggiunta.")

        cont = input("\nContinua? (s/n): ").lower()
        if cont != 's':
            break

    # Salva regole aggiornate
    save_rules("data/rules_updated.csv", rules)
    print("Regole salvate. Arrivederci.")

if __name__ == '__main__':
    main()
