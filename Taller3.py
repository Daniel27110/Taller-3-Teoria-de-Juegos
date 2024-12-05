import random

def simulate_round(player1, player2, C, T, p):
    """Simula una ronda entre dos jugadores con posibilidad de error p."""
    choice1 = player1['strategy']()
    choice2 = player2['strategy']()

    # Simular error de la máquina
    if random.random() < p:
        choice1 = not choice1
    if random.random() < p:
        choice2 = not choice2

    # Asignar puntajes según las elecciones
    if choice1 and choice2:
        return C, C
    elif choice1 and not choice2:
        return 0, T
    elif not choice1 and choice2:
        return T, 0
    else:
        return 0, 0

def simulate_match(player1, player2, rounds, C, T, p):
    """Simula un partido de varias rondas entre dos jugadores."""
    score1, score2 = 0, 0

    for _ in range(rounds):
        s1, s2 = simulate_round(player1, player2, C, T, p)
        score1 += s1
        score2 += s2

        # Actualizar estrategias basadas en la ronda
        player1['update'](player2['last_choice'])
        player2['update'](player1['last_choice'])

    return score1, score2

def main():
    # Configurar parámetros
    C = int(input("Ingrese el valor de C (ganancia por cooperación mutua): "))
    T = int(input("Ingrese el valor de T (ganancia por traición): "))
    p = float(input("Ingrese la probabilidad de error de la máquina (0 <= p <= 1): "))
    rounds = 20

    # Definir jugadores
    players = {
        "Angel": {
            "strategy": lambda: True,
            "update": lambda _: None,
            "last_choice": True,
            "score": 0
        },
        "Diablo": {
            "strategy": lambda: False,
            "update": lambda _: None,
            "last_choice": False,
            "score": 0
        },
        "Tito": {
            "strategy": lambda: players["Tito"]["last_choice"],
            "update": lambda choice: players["Tito"].update({"last_choice": choice}),
            "last_choice": True,
            "score": 0
        },
        "Loco": {
            "strategy": lambda: random.choice([True, False]),
            "update": lambda _: None,
            "last_choice": True,
            "score": 0
        },
        "Resentido": {
            "strategy": lambda: players["Resentido"]["last_choice"],
            "update": lambda choice: players["Resentido"].update({"last_choice": False if not choice else players["Resentido"]["last_choice"]}),
            "last_choice": True,
            "score": 0
        }
    }

    # Simular el torneo
    player_names = list(players.keys())
    for i in range(len(player_names)):
        for j in range(i + 1, len(player_names)):
            player1 = players[player_names[i]]
            player2 = players[player_names[j]]

            score1, score2 = simulate_match(player1, player2, rounds, C, T, p)
            player1["score"] += score1
            player2["score"] += score2

    # Mostrar resultados
    print("\nResultados del torneo:")
    for name, player in players.items():
        print(f"{name}: {player['score']} monedas")

    # Determinar ganador
    winner = max(players.items(), key=lambda x: x[1]['score'])[0]
    print(f"\nEl ganador es: {winner}")

if __name__ == "__main__":
    main()
