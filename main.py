import os
from models.red_social import RedSocial
from algorithms.fuerza_bruta import modciFB
from algorithms.voraz import modciV
from algorithms.programacion_dinamica import modciPD
from utils.file_io import leer_red_social, escribir_resultado

def main():
    # Leer datos de entrada
    input_path = "data/input.txt"
    output_path = "data/output.txt"
    
    if not os.path.exists(input_path):
        print("Error: No se encontró el archivo de entrada.")
        return
    
    red_social = leer_red_social(input_path)
    
    # Aplicar los tres métodos
    resultados = {
        "Fuerza Bruta": modciFB(red_social),
        "Voraz": modciV(red_social),
        "Programación Dinámica": modciPD(red_social)
    }
    
    # Guardar resultados en archivo
    escribir_resultado(output_path, resultados)
    
    print("Resultados guardados en", output_path)

if __name__ == "__main__":
    main()
