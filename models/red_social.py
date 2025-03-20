import numpy as np

class RedSocial:
    def __init__(self, agentes, r_max):
        self.agentes = agentes  # Lista de tuplas (n, op1, op2, rigidez)
        self.r_max = r_max  # Recursos disponibles

    def calcular_conflicto(self):
        total_conflicto = sum(n * (op1 - op2) ** 2 for n, op1, op2, _ in self.agentes)
        total_agentes = sum(n for n, _, _, _ in self.agentes)
        return total_conflicto / total_agentes if total_agentes > 0 else 0

    def esfuerzo_necesario(self, estrategia):
        return sum(np.ceil(abs(op1 - op2) * rig * e) for (n, op1, op2, rig), e in zip(self.agentes, estrategia))

    def aplicar_estrategia(self, estrategia):
        nueva_red = [(n - e, op1, op1, rig) if e > 0 else (n, op1, op2, rig) for (n, op1, op2, rig), e in zip(self.agentes, estrategia)]
        return RedSocial(nueva_red, self.r_max)

    def __str__(self):
        return f"Red Social (Conflicto: {self.calcular_conflicto()}, Recursos: {self.r_max})"


# algorithms/fuerza_bruta.py
def modciFB(red_social):
    # Generar todas las estrategias posibles y elegir la mejor
    from itertools import product
    mejor_estrategia = None
    mejor_conflicto = float('inf')
    
    for estrategia in product(*(range(n + 1) for n, _, _, _ in red_social.agentes)):
        if red_social.esfuerzo_necesario(estrategia) <= red_social.r_max:
            nueva_red = red_social.aplicar_estrategia(estrategia)
            conflicto = nueva_red.calcular_conflicto()
            if conflicto < mejor_conflicto:
                mejor_conflicto = conflicto
                mejor_estrategia = estrategia
    
    return mejor_estrategia, red_social.esfuerzo_necesario(mejor_estrategia), mejor_conflicto


# algorithms/voraz.py
def modciV(red_social):
    # Ordenamos los grupos por la diferencia de opiniones multiplicada por la rigidez
    agentes_ordenados = sorted(enumerate(red_social.agentes), key=lambda x: abs(x[1][1] - x[1][2]) * x[1][3], reverse=True)
    estrategia = [0] * len(red_social.agentes)
    recursos_disponibles = red_social.r_max
    
    for i, (n, op1, op2, rig) in agentes_ordenados:
        if recursos_disponibles > 0:
            max_cambio = min(n, recursos_disponibles // np.ceil(abs(op1 - op2) * rig))
            estrategia[i] = max_cambio
            recursos_disponibles -= np.ceil(abs(op1 - op2) * rig * max_cambio)
    
    nueva_red = red_social.aplicar_estrategia(estrategia)
    return estrategia, red_social.esfuerzo_necesario(estrategia), nueva_red.calcular_conflicto()


# algorithms/programacion_dinamica.py
def modciPD(red_social):
    n = len(red_social.agentes)
    r_max = red_social.r_max
    dp = [[float('inf')] * (r_max + 1) for _ in range(n + 1)]
    estrategia = [[0] * n for _ in range(r_max + 1)]
    
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        n_agentes, op1, op2, rig = red_social.agentes[i - 1]
        for r in range(r_max + 1):
            dp[i][r] = dp[i - 1][r]
            for e in range(n_agentes + 1):
                esfuerzo = np.ceil(abs(op1 - op2) * rig * e)
                if r >= esfuerzo and dp[i - 1][r - int(esfuerzo)] + e < dp[i][r]:
                    dp[i][r] = dp[i - 1][r - int(esfuerzo)] + e
                    estrategia[r][i - 1] = e
    
    mejor_estrategia = [0] * n
    r = r_max
    for i in range(n, 0, -1):
        mejor_estrategia[i - 1] = estrategia[r][i - 1]
        r -= int(np.ceil(abs(red_social.agentes[i - 1][1] - red_social.agentes[i - 1][2]) * red_social.agentes[i - 1][3] * mejor_estrategia[i - 1]))
    
    nueva_red = red_social.aplicar_estrategia(mejor_estrategia)
    return mejor_estrategia, red_social.esfuerzo_necesario(mejor_estrategia), nueva_red.calcular_conflicto()