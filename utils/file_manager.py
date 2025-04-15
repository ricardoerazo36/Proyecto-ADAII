"""
Utilidades para manejo de archivos en la aplicación ModCI
"""

def cargar_red_social(ruta_archivo):
    """Carga una red social desde un archivo de texto"""
    with open(ruta_archivo, 'r') as f:
        lineas = f.readlines()
    
    n = int(lineas[0].strip())
    grupos = []
    
    for i in range(1, n+1):
        datos = lineas[i].strip().split(',')
        n_agentes = int(datos[0])
        op1 = int(datos[1])
        op2 = int(datos[2])
        rigidez = float(datos[3])
        grupos.append((n_agentes, op1, op2, rigidez))
    
    r_max = int(lineas[n+1].strip())
    
    from models.red_social import RedSocial
    return RedSocial(grupos, r_max)

def guardar_resultado(ruta_archivo, estrategia, conflicto, esfuerzo):
    """Guarda el resultado en un archivo de texto según el formato especificado"""
    with open(ruta_archivo, 'w') as f:
        f.write(f"{conflicto}\n")
        f.write(f"{esfuerzo}\n")
        for mod in estrategia:
            f.write(f"{mod}\n")

def guardar_caso_prueba(red_social, ruta_archivo):
    """Guarda un caso de prueba generado en formato de archivo de entrada"""
    with open(ruta_archivo, 'w') as f:
        f.write(f"{red_social.n}\n")
        
        for n_agentes, op1, op2, rigidez in red_social.grupos:
            f.write(f"{n_agentes}, {op1}, {op2}, {rigidez}\n")
        
        f.write(f"{red_social.r_max}\n")