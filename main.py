import random
import json

# Q-Tabelle für das Lernen
q_table = {}  # Speichert Belohnungen für Aktionen

# Lernrate und Rabattfaktor
alpha = 0.1  # Wie stark neue Infos alte ersetzen
gamma = 0.9  # Wie stark zukünftige Belohnungen zählen

# Exploration vs Exploitation Parameter
epsilon = 0.1  # Wahrscheinlichkeit für Exploration
exploit_probability = 0.1  # Anfangswahrscheinlichkeit, mit der die beste Aktion gewählt wird

# Funktion, um eine Aktion zu wählen
def choose_action(state):
    # Wenn der Zustand noch nicht in der Q-Tabelle ist, dann initialisieren wir ihn
    if state not in q_table:
        q_table[state] = {+1: 0, -1: 0, 0: 0}  # Init mit 0 für +1, -1 und neutral (0)
    
    # Exploration: Wähle zufällige Aktion
    if random.uniform(0, 1) < epsilon:
        return random.choice([+1, -1, 0])  # Zufällige Aktion: +1, -1 oder neutral (0)
    
    # Exploitation: Wähle mit einer Wahrscheinlichkeit basierend auf den Q-Werten
    # Die Wahrscheinlichkeit steigt mit der Stärke des Q-Wertes der besten Aktion
    if random.uniform(0, 1) < exploit_probability:
        # Wähle die beste bekannte Aktion
        return max(q_table[state], key=q_table[state].get)
    else:
        # Wähle zufällig eine der besten Aktionen mit den höchsten Q-Werten
        max_q_value = max(q_table[state].values())
        best_actions = [action for action, value in q_table[state].items() if value == max_q_value]
        return random.choice(best_actions)

# Funktion, um das Q-Learning durchzuführen
def update_q_table(state, action, reward):
    if state not in q_table:
        q_table[state] = {+1: 0, -1: 0, 0: 0}
    
    # Q-Wert aktualisieren: Q(s, a) = (1 - alpha) * Q(s, a) + alpha * (Belohnung + gamma * max(Q(s')))
    q_table[state][action] = (1 - alpha) * q_table[state][action] + alpha * (reward + gamma * max(q_table[state].values()))

# Simulationsschleife
for episode in range(20):
    state = random.randint(0, 9)  # Zufälliger Zustand (Input)
    action = choose_action(state)  # Die KI wählt eine Aktion
    
    print(f"Input: {state}, AI-Output: {action}")
    
    # Du gibst das Feedback manuell
    reward = int(input("Belohnung (+1 = gut, -1 = schlecht, 0 = neutral): "))  # Feedback: +1, -1 oder 0
    
    # Q-Tabelle mit der erhaltenen Belohnung und dem aktuellen Zustand/Aktion-Update anpassen
    update_q_table(state, action, reward)
    
    # Erhöhe die Exploitation-Wahrscheinlichkeit nach jedem Schritt (optional)
    exploit_probability = min(1.0, exploit_probability + 0.05)  # Erhöhe die Wahrscheinlichkeit auf maximal 1.0

# Gelerntes Wissen in eine JSON-Datei speichern
with open('q_table.json', 'w') as json_file:
    json.dump(q_table, json_file, indent=4)

print("\nGelerntes Wissen wurde in die Datei 'q_table.json' gespeichert.")
