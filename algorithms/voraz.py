import numpy as np

def modciV(red_social):
    # Ordenamos los grupos por |op1 - op2| * rigidez en orden descendente
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
