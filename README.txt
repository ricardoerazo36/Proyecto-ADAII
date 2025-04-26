Proyecto Moderación de Conflicto Interno (ModCI)

Estudiantes:
Bayron Jojoa-2242917
Alejandro Muñoz-2242951
Ricardo Erazo-2242117
David Urrego-2240407

Descripción General
ModCI es una aplicación para modelar y resolver problemas de moderación en redes sociales. La aplicación permite cargar o generar redes sociales compuestas por grupos de agentes con opiniones diferentes, y aplicar diversos algoritmos para encontrar estrategias óptimas de moderación que minimicen el conflicto interno.

Estructura de Archivos
El proyecto está organizado en los siguientes directorios y archivos:

Directorio Principal
main.py: Punto de entrada de la aplicación. Contiene la interfaz gráfica y la lógica principal.

Directorio models/
red_social.py: Define la clase RedSocial que modela una red social con grupos de agentes.

Directorio algorithms/
fuerza_bruta.py: Implementa el algoritmo de fuerza bruta.
voraz.py: Implementa el algoritmo voraz.
programacion_dinamica.py: Implementa el algoritmo de programación dinámica.

Directorio utils/
file_manager.py: Contiene funciones para cargar y guardar redes sociales y resultados.
test_generator.py: Proporciona funciones para generar casos de prueba aleatorios.
ui_theme_utils.py: Contiene utilidades para gestionar la interfaz de usuario y los temas.

Requisitos
Para ejecutar la aplicación necesitarás:
Python 3.6 o superior
Bibliotecas: tkinter, numpy , functools

Ejecución de la Aplicación
Para ejecutar la aplicación, simplemente ejecuta el archivo main.py

Luego, se debe cargar una Red Social.

Haz clic en "Seleccionar archivo" y escoge un archivo de BateriaPruebas.

O se puede generar un Caso Aleatorio.
Haz clic en "Generar caso aleatorio"
Introduce el número de grupos y el número máximo de agentes por grupo
Opcionalmente, guarda el caso generado

Ejecutar Algoritmos
Puedes ejecutar cualquiera de los tres algoritmos disponibles:

Fuerza Bruta: Garantiza encontrar la solución óptima, pero puede ser lento para redes grandes
Voraz: Rápido pero puede no encontrar la solución óptima
Programación Dinámica: Balance entre eficiencia y optimalidad

Comparar Algoritmos
Haz clic en "Comparar algoritmos" para ejecutar los tres algoritmos y comparar sus resultados y tiempos de ejecución.
Guardar Resultados
Después de ejecutar un algoritmo, puedes guardar los resultados haciendo clic en "Guardar resultado".

Algoritmos Implementados

Fuerza Bruta:
Prueba todas las combinaciones posibles de estrategias y selecciona la que minimiza el conflicto interno respetando la restricción de esfuerzo máximo.

Voraz:
Prioriza los grupos con mayor diferencia de opiniones y menor rigidez, asignando recursos de manera incremental hasta agotar el esfuerzo máximo disponible.

Programación Dinámica:
Utiliza una matriz para almacenar soluciones parciales y construir la solución óptima de manera recursiva, balanceando el tiempo de ejecución y la calidad de la solución.
