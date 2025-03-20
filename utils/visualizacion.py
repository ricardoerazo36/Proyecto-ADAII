import matplotlib.pyplot as plt

def graficar_conflicto(resultados):
    """Grafica el nivel de conflicto final para cada método."""
    metodos = list(resultados.keys())
    conflictos = [res[2] for res in resultados.values()]
    
    plt.figure(figsize=(8, 5))
    plt.bar(metodos, conflictos, color=["blue", "orange", "green"])
    plt.xlabel("Método")
    plt.ylabel("Conflicto Interno")
    plt.title("Comparación del Conflicto Interno entre Métodos")
    plt.show()

def graficar_esfuerzo(resultados):
    """Grafica el esfuerzo utilizado por cada método."""
    metodos = list(resultados.keys())
    esfuerzos = [res[1] for res in resultados.values()]
    
    plt.figure(figsize=(8, 5))
    plt.bar(metodos, esfuerzos, color=["blue", "orange", "green"])
    plt.xlabel("Método")
    plt.ylabel("Esfuerzo Utilizado")
    plt.title("Comparación del Esfuerzo Utilizado entre Métodos")
    plt.show()