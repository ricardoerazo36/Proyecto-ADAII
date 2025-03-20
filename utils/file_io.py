import os
from models.red_social import RedSocial

def leer_red_social(filepath):
    """Lee la red social desde un archivo de texto y devuelve un objeto RedSocial."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe.")
    
    with open(filepath, "r") as f:
        lineas = f.readlines()
    
    n = int(lineas[0].strip())  # Número de grupos de agentes
    agentes = []
    
    for i in range(1, n + 1):
        datos = list(map(float, lineas[i].strip().split(",")))
        agentes.append((int(datos[0]), int(datos[1]), int(datos[2]), datos[3]))  # (n, op1, op2, rigidez)
    
    r_max = int(lineas[n + 1].strip())  # Recursos disponibles
    
    return RedSocial(agentes, r_max)

def escribir_resultado(filepath, resultados):
    """Guarda los resultados de los algoritmos en un archivo de texto."""
    with open(filepath, "w") as f:
        for metodo, (estrategia, esfuerzo, conflicto) in resultados.items():
            f.write(f"{metodo}\n")
            f.write(f"Conflicto final: {conflicto}\n")
            f.write(f"Esfuerzo utilizado: {esfuerzo}\n")
            f.write(f"Estrategia aplicada: {estrategia}\n")
            f.write("\n")
