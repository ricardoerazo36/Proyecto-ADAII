def modciFB(red_social):
    """
    Algoritmo de fuerza bruta para el problema ModCI
    Retorna: (estrategia_optima, esfuerzo, conflicto_interno)
    """
    n = red_social.n
    mejor_estrategia = None
    mejor_conflicto = float('inf')
    
    # Función recursiva para generar todas las posibles estrategias
    def generar_estrategias(estrategia_actual, indice):
        nonlocal mejor_estrategia, mejor_conflicto
        
        # Caso base: si ya hemos asignado todos los grupos
        if indice == n:
            if red_social.estrategia_aplicable(estrategia_actual):
                nueva_red = red_social.aplicar_estrategia(estrategia_actual)
                conflicto = nueva_red.calcular_conflicto_interno()
                
                if conflicto < mejor_conflicto:
                    mejor_conflicto = conflicto
                    mejor_estrategia = estrategia_actual.copy()
            return
        
        # Generar todas las posibilidades para este grupo
        n_agentes = red_social.grupos[indice][0]
        for k in range(n_agentes + 1):  # Desde 0 hasta n_agentes
            estrategia_actual[indice] = k
            generar_estrategias(estrategia_actual, indice + 1)
    
    # Iniciar la generación de estrategias
    estrategia_inicial = [0] * n
    generar_estrategias(estrategia_inicial, 0)
    
    # Si no encontramos ninguna estrategia aplicable
    if mejor_estrategia is None:
        mejor_estrategia = [0] * n
    
    esfuerzo = red_social.calcular_esfuerzo(mejor_estrategia)
    return (mejor_estrategia, esfuerzo, mejor_conflicto)