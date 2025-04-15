"""
Utilidades para generar casos de prueba para la aplicación ModCI
"""
import numpy as np

def generar_caso_prueba(n, max_agentes=10, r_max_factor=5):
    """Genera un caso de prueba aleatorio"""
    grupos = []
    total_agentes = 0
    
    for _ in range(n):
        n_agentes = np.random.randint(1, max_agentes + 1)
        op1 = np.random.randint(-100, 101)
        op2 = np.random.randint(-100, 101)
        rigidez = round(np.random.random(), 2)  # Entre 0 y 1 con 2 decimales
        
        grupos.append((n_agentes, op1, op2, rigidez))
        total_agentes += n_agentes
    
    # R_max proporcional al número total de agentes y diferencias de opinión
    r_max = np.random.randint(1, total_agentes * r_max_factor + 1)
    
    from models.red_social import RedSocial
    return RedSocial(grupos, r_max)