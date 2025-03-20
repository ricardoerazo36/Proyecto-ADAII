import numpy as np

def modciPD(red_social):
    n = len(red_social.agentes)
    r_max = red_social.r_max
    
    # Matriz DP para minimizar el conflicto interno con un presupuesto r_max
    dp = [[float('inf')] * (r_max + 1) for _ in range(n + 1)]
    estrategia = [[0] * n for _ in range(r_max + 1)]
    
    dp[0][0] = 0  # Sin recursos, sin agentes cambiados

    for i in range(1, n + 1):
        n_agentes, op1, op2, rig = red_social.agentes[i - 1]
        for r in range(r_max + 1):
            dp[i][r] = dp[i - 1][r]  # No cambiar ningún agente en este grupo
            
            for e in range(n_agentes + 1):  # Evaluamos cambiar desde 0 hasta n_agentes
                esfuerzo = np.ceil(abs(op1 - op2) * rig * e)
                if r >= esfuerzo and dp[i - 1][r - int(esfuerzo)] + e < dp[i][r]:
                    dp[i][r] = dp[i - 1][r - int(esfuerzo)] + e
                    estrategia[r][i - 1] = e

    # Reconstrucción de la mejor estrategia
    mejor_estrategia = [0] * n
    r = r_max
    for i in range(n, 0, -1):
        mejor_estrategia[i - 1] = estrategia[r][i - 1]
        r -= int(np.ceil(abs(red_social.agentes[i - 1][1] - red_social.agentes[i - 1][2]) * red_social.agentes[i - 1][3] * mejor_estrategia[i - 1]))
    
    nueva_red = red_social.aplicar_estrategia(mejor_estrategia)
    return mejor_estrategia, red_social.esfuerzo_necesario(mejor_estrategia), nueva_red.calcular_conflicto()
