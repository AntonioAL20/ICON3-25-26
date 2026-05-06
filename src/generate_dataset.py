import os
import random
import pandas as pd

def generate_large_dataset(num_samples=1000):
    """
    Genera un dataset CSV sintetico per addestrare il sistema diagnostico.
    Associa probabilità di comparsa di determinati sintomi a specifiche categorie di guasto.
    """
    guasti_rules = {
        "GuastoTermico": ["TempTroppoAlta", "TempInstabile", "PiattoFreddo", "VentolaRumorosa"],
        "GuastoMeccanico": ["LayerSpostati", "RumoreCinghia", "HomeFallito", "TicchettioEstrusore", "SottoEstrusione"],
        "ProblemaElettrico": ["OdoreBruciato", "SchermoNero", "HomeFallito", "TempInstabile"],
        "ProblemaAdesione": ["Warping", "PiattoFreddo", "FilamentoNonEsce"]
    }
    
    data = []
    
    for _ in range(num_samples):
        # Scegliamo un guasto a caso
        guasto_target = random.choice(list(guasti_rules.keys()))
        sintomi_possibili = guasti_rules[guasto_target]
        
        # Scegliamo da 1 a 3 sintomi per questo guasto
        num_sintomi = random.randint(1, min(3, len(sintomi_possibili)))
        sintomi_scelti = random.sample(sintomi_possibili, num_sintomi)
        
        # Aggiungiamo un leggero "rumore" (il 10% delle volte un sintomo fuori contesto)
        if random.random() < 0.10:
            sintomo_rumore = random.choice(["VentolaRumorosa", "SchermoNero", "TicchettioEstrusore"])
            if sintomo_rumore not in sintomi_scelti:
                sintomi_scelti.append(sintomo_rumore)
                
        # Uniamo i sintomi con il punto e virgola
        sintomi_str = ";".join(sintomi_scelti)
        data.append({"sintomi": sintomi_str, "guasto": guasto_target})
        
    df = pd.DataFrame(data)
    
    # Salvataggio
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", "data", "dataset_guasti.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Generato dataset di {num_samples} istanze in {csv_path}")

if __name__ == "__main__":
    generate_large_dataset()