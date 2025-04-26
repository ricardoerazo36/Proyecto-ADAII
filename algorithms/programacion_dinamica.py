import numpy as np
from functools import lru_cache

def modciPD(red_social):
    n = red_social.n
    r_max = red_social.r_max
    grupos = red_social.grupos

    decision_cache = {}  # (i, r) -> k chosen

    @lru_cache(maxsize=None)
    def dp(i, r):
        if i == 0:
            return 0

        n_agentes, op1, op2, rigidez = grupos[i - 1]
        diferencia_op = abs(op1 - op2)

        min_conflicto = dp(i - 1, r) + n_agentes * (diferencia_op ** 2)
        mejor_k = 0

        for k in range(1, n_agentes + 1):
            esfuerzo = int(np.ceil(diferencia_op * rigidez * k))
            if r >= esfuerzo:
                conflicto = dp(i - 1, r - esfuerzo) + (n_agentes - k) * (diferencia_op ** 2)
                if conflicto < min_conflicto:
                    min_conflicto = conflicto
                    mejor_k = k

        # Store decision for reconstruction
        decision_cache[(i, r)] = mejor_k
        return min_conflicto

    # Call the top-level problem
    total_conflicto = dp(n, r_max)

    # Reconstruct strategy using the decision cache
    estrategia = [0] * n
    r = r_max
    for i in range(n, 0, -1):
        k = decision_cache.get((i, r), 0)
        estrategia[i - 1] = k
        if k > 0:
            n_agentes, op1, op2, rigidez = grupos[i - 1]
            diferencia_op = abs(op1 - op2)
            esfuerzo = int(np.ceil(diferencia_op * rigidez * k))
            r -= esfuerzo

    total_agentes = sum(grupo[0] for grupo in grupos)
    conflicto_ajustado = total_conflicto / total_agentes

    return (estrategia, red_social.calcular_esfuerzo(estrategia), conflicto_ajustado)

