import numpy as np

def modciV(red_social):
    """
    Algoritmo voraz para el problema ModCI.
    Estrategia: Priorizar grupos por (o_i1 - o_i2)^2 * n_i / r_i
    Retorna: (estrategia_optima, esfuerzo, conflicto_interno)
    """
    n = red_social.n
    estrategia = [0] * n
    r_max_restante = red_social.r_max
    
    # Calculamos la prioridad de cada grupo según la teoría
    # prioridad = (o_i1 - o_i2)^2 * n_i / r_i
    prioridades = []
    for i in range(n):
        n_agentes, op1, op2, rigidez = red_social.grupos[i]
        diferencia_op = abs(op1 - op2)
        
        # Evitamos división por cero
        if rigidez == 0:
            prioridad = float('inf')
        else:
            prioridad = (diferencia_op ** 2) * n_agentes / rigidez
            
        # Guardamos (índice, prioridad, n_agentes)
        prioridades.append((i, prioridad, n_agentes))
    
    # Ordenamos por prioridad descendente
    prioridades.sort(key=lambda x: x[1], reverse=True)
    
    # Asignamos recursos de forma voraz
    for i, _, n_agentes in prioridades:
        _, op1, op2, rigidez = red_social.grupos[i]
        diferencia_op = abs(op1 - op2)
        
        # Iteramos hasta agotar el esfuerzo o moderar todos los agentes
        for e in range(1, n_agentes + 1):
            esfuerzo_e = int(np.ceil(diferencia_op * rigidez * e))
            if esfuerzo_e > r_max_restante:
                break
            estrategia[i] = e
            
        r_max_restante -= int(np.ceil(diferencia_op * rigidez * estrategia[i]))
    
    # Calculamos el conflicto interno resultante
    nueva_red = red_social.aplicar_estrategia(estrategia)
    conflicto = nueva_red.calcular_conflicto_interno()
    
    return (estrategia, red_social.calcular_esfuerzo(estrategia), conflicto)