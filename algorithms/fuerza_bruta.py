from itertools import product
import numpy as np

def modciFB(red_social):
    mejor_estrategia = None
    mejor_conflicto = float('inf')
    
    # Generar todas las combinaciones posibles de estrategias
    for estrategia in product(*(range(n + 1) for n, _, _, _ in red_social.agentes)):
        if red_social.esfuerzo_necesario(estrategia) <= red_social.r_max:
            nueva_red = red_social.aplicar_estrategia(estrategia)
            conflicto = nueva_red.calcular_conflicto()
            if conflicto < mejor_conflicto:
                mejor_conflicto = conflicto
                mejor_estrategia = estrategia
    
    return mejor_estrategia, red_social.esfuerzo_necesario(mejor_estrategia), mejor_conflicto
