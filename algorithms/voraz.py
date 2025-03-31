import numpy as np

def modciV(red_social):
    """
    Algoritmo voraz para el problema ModCI.
    Estrategia: Priorizar grupos con mayor diferencia de opiniones y menor rigidez
    Retorna: (estrategia_optima, esfuerzo, conflicto_interno)
    """
    n = red_social.n
    estrategia = [0] * n
    r_max_restante = red_social.r_max
    
    # Calculamos el beneficio por unidad de esfuerzo para cada grupo
    beneficios = []
    for i in range(n):
        n_agentes, op1, op2, rigidez = red_social.grupos[i]
        
        if rigidez == 0:  # Evitar división por cero
            beneficio = float('inf')
        else:
            # Beneficio = reducción en conflicto por unidad de esfuerzo
            diferencia_op = abs(op1 - op2)
            beneficio = (diferencia_op ** 2) / (diferencia_op * rigidez)
        
        beneficios.append((i, beneficio, n_agentes))
    
    # Ordenamos por beneficio descendente
    beneficios.sort(key=lambda x: x[1], reverse=True)
    
    # Asignamos recursos de forma voraz
    for i, beneficio, max_agentes in beneficios:
        n_agentes, op1, op2, rigidez = red_social.grupos[i]
        diferencia_op = abs(op1 - op2)
        
        # Calculamos cuántos agentes podemos moderar con el r_max restante
        esfuerzo_por_agente = np.ceil(diferencia_op * rigidez)
        max_modificables = min(max_agentes, r_max_restante // max(1, esfuerzo_por_agente))
        
        # Actualizamos la estrategia y el r_max restante
        estrategia[i] = max_modificables
        r_max_restante -= int(max_modificables * esfuerzo_por_agente)
    
    # Calculamos el conflicto interno resultante
    nueva_red = red_social.aplicar_estrategia(estrategia)
    conflicto = nueva_red.calcular_conflicto_interno()
    
    return (estrategia, red_social.calcular_esfuerzo(estrategia), conflicto)