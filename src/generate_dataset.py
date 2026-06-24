import os
import random
import pandas as pd

def generate_large_dataset(num_samples=1500):
    guasti_rules = {
        "GuastoTermico": ["TempTroppoAlta", "TempInstabile", "PiattoFreddo", "VentolaRumorosa"],
        "GuastoMeccanico": ["LayerSpostati", "RumoreCinghia", "HomeFallito", "TicchettioEstrusore", "SottoEstrusione"],
        "ProblemaElettrico": ["OdoreBruciato", "SchermoNero", "HomeFallito", "TempInstabile"],
        "ProblemaAdesione": ["Warping", "PiattoFreddo", "FilamentoNonEsce"]
    }
    
    materiali = ["PLA", "ABS", "PETG", "TPU", "NYLON", "ASA", "PC"]
    data = []
    
    for _ in range(num_samples):
        guasto_target = random.choice(list(guasti_rules.keys()))
        sintomi_possibili = guasti_rules[guasto_target]
        
        num_sintomi = random.randint(1, min(3, len(sintomi_possibili)))
        sintomi_scelti = random.sample(sintomi_possibili, num_sintomi)
        
        if random.random() < 0.25: 
            sintomi_scelti.append(random.choice(["VentolaRumorosa", "SchermoNero", "TicchettioEstrusore", "HomeFallito"]))
                
        sintomi_str = ";".join(list(set(sintomi_scelti)))
        materiale = random.choice(materiali)
        
        velocita = random.randint(40, 150)
        umidita = random.randint(30, 80)
        usura = random.randint(100, 4000)
        temp_estrusore = random.randint(190, 240)
        temp_piatto = random.randint(40, 80)
        vibrazioni = random.randint(5, 25)
        
        if guasto_target == "GuastoTermico" and random.random() > 0.3:
            temp_estrusore = random.choice([random.randint(250, 290), random.randint(150, 170)])
            usura = random.randint(1000, 5000)
            
        elif guasto_target == "GuastoMeccanico" and random.random() > 0.4:
            velocita = random.randint(100, 200)
            usura = random.randint(3000, 7000)
            vibrazioni = random.randint(40, 90)
            
        elif guasto_target == "ProblemaAdesione" and random.random() > 0.3:
            temp_piatto = random.randint(20, 55)
            if materiale in ["NYLON", "PETG", "TPU"]:
                umidita = random.randint(55, 95)
                
        elif guasto_target == "ProblemaElettrico" and random.random() > 0.5:
            umidita = random.randint(60, 95)
            
        if velocita > 120 and usura > 3000:
            vibrazioni = random.randint(30, 60)
            
        tempo_stampa_ore = round(random.uniform(0.5, 96.0), 1)
        
        data.append({
            "materiale": materiale,
            "temperatura_estrusore": temp_estrusore,
            "temperatura_piatto": temp_piatto,
            "velocita_stampa": velocita,
            "umidita_ambientale": umidita,
            "usura_motore": usura,
            "livello_vibrazioni": vibrazioni,
            "tempo_stampa_ore": tempo_stampa_ore,
            "sintomi": sintomi_str, 
            "guasto": guasto_target
        })
        
    df = pd.DataFrame(data)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", "data", "dataset_guasti.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Generato dataset multi-variato (Sensori Avanzati) di {num_samples} istanze in {csv_path}")

if __name__ == "__main__":
    generate_large_dataset()