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

def load_q_table():
    try:
        with open('q_table.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("Die Datei 'q_table.json' wurde nicht gefunden. Eine neue Tabelle wird erstellt.")
        return {}

# Funktion, um eine Aktion zu wählen
def choose_action(state):
    # Wenn der Zustand noch nicht in der Q-Tabelle ist, dann initialisieren wir ihn
    if str(state) not in q_table:
        q_table[str(state)] = {+1: 0, -1: 0, 0: 0}  # Init mit 0 für +1, -1 und neutral (0)
    
    # Exploration: Wähle zufällige Aktion
    if random.uniform(0, 1) < epsilon:
        return random.choice([+1, -1, 0])  # Zufällige Aktion: +1, -1 oder neutral (0)
    
    # Exploitation: Wähle mit einer Wahrscheinlichkeit basierend auf den Q-Werten
    # Die Wahrscheinlichkeit steigt mit der Stärke des Q-Wertes der besten Aktion
    if random.uniform(0, 1) < exploit_probability:
        # Wähle die beste bekannte Aktion
        return max(q_table[str(state)], key=q_table[str(state)].get)
    else:
        # Wähle zufällig eine der besten Aktionen mit den höchsten Q-Werten
        max_q_value = max(q_table[str(state)].values())
        best_actions = [action for action, value in q_table[str(state)].items() if value == max_q_value]
        return random.choice(best_actions)

# Funktion, um das Q-Learning durchzuführen
def update_q_table(state, action, reward):
    if str(state) not in q_table:
        q_table[str(state)] = {+1: 0, -1: 0, 0: 0}
    
    # Q-Wert aktualisieren: Q(s, a) = (1 - alpha) * Q(s, a) + alpha * (Belohnung + gamma * max(Q(s')))
    next_max_q_value = max(q_table[str(state)].values())  # Maximaler Q-Wert aus dem aktuellen Zustand (s')
    q_table[str(state)][action] = (1 - alpha) * q_table[str(state)][action] + alpha * (reward + gamma * next_max_q_value)

def get_reward(state, action):
    if state == 0:
        # Zustand 0
        if action == +1:
            return 0
        elif action == 0:
            return 1
        elif action == -1:
            return -5
    
    elif state % 2 == 0:  # Gerade Zahl
        # Bei geraden Zahlen:
        if action == +1:
            return 1
        elif action == 0:
            return -1
        elif action == -1:
            return -5
    
    else:  # Ungerade Zahl
        # Bei ungeraden Zahlen:
        if action == +1:
            return -5
        elif action == 0:
            return -1
        elif action == -1:
            return 1
        
def think(learning,state=None,userInput=False):
    if(learning):
        state = random.randint(0, 9)  # Zufälliger Startzustand
    action = choose_action(str(state))  # Die KI wählt eine Aktion
    reward = 0  # Belohnung (Feedback)

    if(learning):
        if(userInput):
            print(f"Input: {state}, AI-Output: {action}")
            reward = int(input("Belohnung (+1 = gut, -1 = schlecht, 0 = neutral): "))  # Feedback: +1, -1 oder 0
        else:
            reward = get_reward(state, action)  # Belohnung basierend auf dem Zustand und der Aktion
            print(f"Input: {state}, AI-Output: {action}, Reward: {reward}")

        update_q_table(str(state), action, reward)
    else:
        print(f"Input: {state}, AI-Output: {action}")

REPEAT_COUNT = 10000

learn = input("Möchtest du die KI trainieren (T) oder benutzen (B): ")

if learn.lower() == "t":
    userInput = input("Möchtest du die Belohnungen manuell eingeben (J/N): ")
    if userInput.lower() == "j":
        for episode in range(REPEAT_COUNT):
            think(learning=True,userInput=True)
    else:
        for episode in range(REPEAT_COUNT):
            think(learning=True,userInput=False)

    with open('q_table.json', 'w') as json_file:
        json.dump(q_table, json_file, indent=4)
    
    print("\nGelerntes Wissen wurde in die Datei 'q_table.json' gespeichert.")
elif learn.lower() == "b":
    q_table = load_q_table()
    
    for i in range(10):
        think(learning=False,state=i)
