import numpy as np

def modciPD(red_social):
    """
    Algoritmo de programación dinámica para el problema ModCI
    Retorna: (estrategia_optima, esfuerzo, conflicto_interno)
    """
    n = red_social.n
    r_max = red_social.r_max
    
    # Inicializamos la tabla de PD
    # dp[i][r] representa el mínimo conflicto posible considerando los primeros i grupos
    # con un presupuesto máximo de r
    dp = [[float('inf')] * (r_max + 1) for _ in range(n + 1)]
    
    # Caso base: sin grupos, conflicto es 0
    for r in range(r_max + 1):
        dp[0][r] = 0
    
    # Matriz para reconstruir la solución
    decisiones = [[-1] * (r_max + 1) for _ in range(n + 1)]
    
    # Llenamos la tabla DP
    for i in range(1, n + 1):
        grupo_idx = i - 1
        n_agentes, op1, op2, rigidez = red_social.grupos[grupo_idx]
        diferencia_op = abs(op1 - op2)
        
        for r in range(r_max + 1):
            # Opción 1: No moderar ningún agente de este grupo
            dp[i][r] = dp[i-1][r] + n_agentes * (diferencia_op ** 2)
            decisiones[i][r] = 0
            
            # Opción 2: Moderar k agentes (1 <= k <= n_agentes)
            for k in range(1, n_agentes + 1):
                esfuerzo = int(np.ceil(diferencia_op * rigidez * k))
                
                if r >= esfuerzo:
                    # Calculamos el conflicto si moderamos k agentes
                    nuevo_conflicto = dp[i-1][r - esfuerzo] + (n_agentes - k) * (diferencia_op ** 2)
                    
                    if nuevo_conflicto < dp[i][r]:
                        dp[i][r] = nuevo_conflicto
                        decisiones[i][r] = k
    
    # Reconstruimos la estrategia óptima
    estrategia = [0] * n
    r_restante = r_max
    
    for i in range(n, 0, -1):
        estrategia[i-1] = decisiones[i][r_restante]
        if estrategia[i-1] > 0:
            n_agentes, op1, op2, rigidez = red_social.grupos[i-1]
            esfuerzo = int(np.ceil(abs(op1 - op2) * rigidez * estrategia[i-1]))
            r_restante -= esfuerzo
    
    # Ajustamos el conflicto para reflejar la división por el número total de agentes
    total_agentes = sum(grupo[0] for grupo in red_social.grupos)
    conflicto_ajustado = dp[n][r_max] / total_agentes
    
    return (estrategia, red_social.calcular_esfuerzo(estrategia), conflicto_ajustado)