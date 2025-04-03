"""
ModCI - Moderación de Conflicto Interno
Módulo principal de la aplicación
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, simpledialog
import os
import time
import numpy as np

from models.red_social import RedSocial
from algorithms.fuerza_bruta import modciFB
from algorithms.voraz import modciV
from algorithms.programacion_dinamica import modciPD

# Importamos las utilidades que hemos unificado
from utils.ui_theme_utils import UIManager, create_tooltip, create_button, setup_scrolled_text
from utils.file_manager import cargar_red_social, guardar_resultado, guardar_caso_prueba
from utils.test_generator import generar_caso_prueba

class ModCIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ModCI - Moderación de Conflicto Interno")
        self.root.geometry("900x700")
        
        # Inicializamos el gestor de interfaz unificado
        self.ui_manager = UIManager(root)
        self.text_config = self.ui_manager.get_text_config()
        
        self.red_social = None
        self.ruta_archivo_entrada = None
        self.resultado_actual = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de menú
        self.crear_menu()
        
        # Frame para carga de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Archivo de entrada", padding="10")
        file_frame.pack(fill=tk.X, expand=False, pady=5)
        
        # Botones con la nueva función auxiliar
        create_button(
            file_frame, 
            "Seleccionar archivo", 
            self.seleccionar_archivo, 
            "Primario.TButton", 
            "Seleccionar un archivo de entrada para cargar una red social"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            file_frame, 
            "Generar caso aleatorio", 
            self.generar_caso_aleatorio, 
            "Secundario.TButton",
            "Genera un caso de prueba aleatorio con los parámetros especificados"
        ).pack(side=tk.LEFT, padx=5)
        
        self.lbl_archivo = ttk.Label(file_frame, text="No se ha seleccionado ningún archivo")
        self.lbl_archivo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Frame para visualización de la red social
        red_frame = ttk.LabelFrame(main_frame, text="Red Social", padding="10")
        red_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Usando la función auxiliar para crear el ScrolledText
        self.txt_red = setup_scrolled_text(red_frame, 10, **self.text_config)
        self.txt_red.pack(fill=tk.BOTH, expand=True)
        
        # Frame para algoritmos
        alg_frame = ttk.LabelFrame(main_frame, text="Algoritmos", padding="10")
        alg_frame.pack(fill=tk.X, expand=False, pady=5)
        
        # Grid para los botones de algoritmos
        for i in range(3):
            alg_frame.columnconfigure(i, weight=1)
        
        # Botones de algoritmos con la nueva función auxiliar
        btn_fb = create_button(
            alg_frame, 
            "Fuerza Bruta", 
            self.ejecutar_fuerza_bruta, 
            "Primario.TButton", 
            "Ejecuta el algoritmo de fuerza bruta (puede ser lento para redes grandes)"
        )
        btn_fb.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_voraz = create_button(
            alg_frame, 
            "Voraz", 
            self.ejecutar_voraz, 
            "Primario.TButton", 
            "Ejecuta el algoritmo voraz (rápido pero puede no ser óptimo)"
        )
        btn_voraz.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        btn_pd = create_button(
            alg_frame, 
            "Programación Dinámica", 
            self.ejecutar_pd, 
            "Primario.TButton", 
            "Ejecuta el algoritmo de programación dinámica (balance entre eficiencia y optimalidad)"
        )
        btn_pd.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Frame para resultados
        res_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        res_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Usando la función auxiliar para crear el ScrolledText
        self.txt_resultados = setup_scrolled_text(res_frame, 10, **self.text_config)
        self.txt_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Frame para guardar resultados
        save_frame = ttk.LabelFrame(main_frame, text="Guardar resultados", padding="10")
        save_frame.pack(fill=tk.X, expand=False, pady=5)
        
        create_button(
            save_frame, 
            "Guardar resultado", 
            self.guardar_resultado, 
            "Acento.TButton",
            "Guarda el resultado del último algoritmo ejecutado"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            save_frame, 
            "Comparar algoritmos", 
            self.comparar_algoritmos, 
            "Secundario.TButton",
            "Compara el rendimiento de todos los algoritmos disponibles"
        ).pack(side=tk.LEFT, padx=5)
        
        # Statusbar
        self.statusbar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.seleccionar_archivo)
        file_menu.add_command(label="Generar caso aleatorio", command=self.generar_caso_aleatorio)
        file_menu.add_separator()
        file_menu.add_command(label="Guardar resultado", command=self.guardar_resultado)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Algoritmos
        alg_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Algoritmos", menu=alg_menu)
        alg_menu.add_command(label="Fuerza Bruta", command=self.ejecutar_fuerza_bruta)
        alg_menu.add_command(label="Voraz", command=self.ejecutar_voraz)
        alg_menu.add_command(label="Programación Dinámica", command=self.ejecutar_pd)
        alg_menu.add_separator()
        alg_menu.add_command(label="Comparar algoritmos", command=self.comparar_algoritmos)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Cambiar tema", command=self.cambiar_tema)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        help_menu.add_command(label="Documentación", command=self.mostrar_documentacion)
    
    def cambiar_tema(self):
        """Cambia el tema de la aplicación"""
        self.text_config = self.ui_manager.toggle_theme()
        self.txt_red.configure(**self.text_config)
        self.txt_resultados.configure(**self.text_config)
        self.statusbar.config(text=f"Tema cambiado a: {self.ui_manager.get_current_theme()}")
    
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de ModCI",
            "ModCI - Moderación de Conflicto Interno\n\n"
            "Una aplicación para modelar y resolver problemas de moderación en redes sociales\n\n"
            "© 2025"
        )
    
    def mostrar_documentacion(self):
        """Muestra la documentación de la aplicación"""
        # Aquí podría abrirse un archivo HTML o PDF con la documentación
        messagebox.showinfo(
            "Documentación",
            "La documentación está disponible en el archivo README.md\n"
            "del proyecto y en la carpeta docs/."
        )
    
    def generar_caso_aleatorio(self):
        """Genera un caso de prueba aleatorio"""
        try:
            n = simpledialog.askinteger("Generar caso", "Número de grupos:", 
                                        minvalue=1, maxvalue=100, initialvalue=5)
            if n is None:
                return
            
            max_agentes = simpledialog.askinteger("Generar caso", "Máximo número de agentes por grupo:", 
                                                  minvalue=1, maxvalue=100, initialvalue=10)
            if max_agentes is None:
                return
            
            # Mostrar un mensaje mientras se genera el caso (puede tardar)
            self.statusbar.config(text="Generando caso aleatorio...")
            self.root.update_idletasks()
            
            self.red_social = generar_caso_prueba(n, max_agentes)
            self.txt_red.delete(1.0, tk.END)
            self.txt_red.insert(tk.END, str(self.red_social))
            
            self.ruta_archivo_entrada = None
            self.lbl_archivo.config(text="Caso generado aleatoriamente (no guardado)")
            self.statusbar.config(text=f"Red social generada aleatoriamente con {n} grupos")
            
            # Preguntar si desea guardar el caso generado
            if messagebox.askyesno("Guardar caso", "¿Desea guardar el caso generado?"):
                self.guardar_caso_generado()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el caso: {str(e)}")
            self.statusbar.config(text="Error al generar el caso")
    
    def guardar_caso_generado(self):
        """Guarda un caso generado aleatoriamente"""
        if not self.red_social:
            return
        
        filetypes = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        ruta = filedialog.asksaveasfilename(title="Guardar caso", filetypes=filetypes, defaultextension=".txt")
        
        if ruta:
            try:
                guardar_caso_prueba(self.red_social, ruta)
                self.ruta_archivo_entrada = ruta
                self.lbl_archivo.config(text=os.path.basename(ruta))
                self.statusbar.config(text=f"Caso guardado en {os.path.basename(ruta)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el caso: {str(e)}")
                self.statusbar.config(text="Error al guardar el caso")
    
    def comparar_algoritmos(self):
        """Compara los tiempos de ejecución y resultados de los diferentes algoritmos"""
        if not self.red_social:
            messagebox.showwarning("Advertencia", "Primero debe cargar una red social")
            return
        
        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, "Comparando algoritmos...\n\n")
        self.root.update_idletasks()
        
        resultados = []
        
        # Ejecutar algoritmo de Fuerza Bruta
        try:
            self.statusbar.config(text="Ejecutando algoritmo Fuerza Bruta...")
            self.root.update_idletasks()
            
            inicio = time.time()
            estrategia_fb, esfuerzo_fb, conflicto_fb = modciFB(self.red_social)
            fin = time.time()
            tiempo_fb = fin - inicio
            
            resultados.append(("Fuerza Bruta", estrategia_fb, esfuerzo_fb, conflicto_fb, tiempo_fb))
        except Exception as e:
            self.txt_resultados.insert(tk.END, f"Error en Fuerza Bruta: {str(e)}\n\n")
        
        # Ejecutar algoritmo Voraz
        try:
            self.statusbar.config(text="Ejecutando algoritmo Voraz...")
            self.root.update_idletasks()
            
            inicio = time.time()
            estrategia_v, esfuerzo_v, conflicto_v = modciV(self.red_social)
            fin = time.time()
            tiempo_v = fin - inicio
            
            resultados.append(("Voraz", estrategia_v, esfuerzo_v, conflicto_v, tiempo_v))
        except Exception as e:
            self.txt_resultados.insert(tk.END, f"Error en algoritmo Voraz: {str(e)}\n\n")
        
        # Ejecutar algoritmo de Programación Dinámica
        try:
            self.statusbar.config(text="Ejecutando algoritmo Programación Dinámica...")
            self.root.update_idletasks()
            
            inicio = time.time()
            estrategia_pd, esfuerzo_pd, conflicto_pd = modciPD(self.red_social)
            fin = time.time()
            tiempo_pd = fin - inicio
            
            resultados.append(("Programación Dinámica", estrategia_pd, esfuerzo_pd, conflicto_pd, tiempo_pd))
        except Exception as e:
            self.txt_resultados.insert(tk.END, f"Error en Programación Dinámica: {str(e)}\n\n")
        
        # Mostrar resultados
        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, "Resultados de la comparación:\n\n")
        
        for nombre, estrategia, esfuerzo, conflicto, tiempo in resultados:
            self.txt_resultados.insert(tk.END, f"Algoritmo: {nombre}\n")
            self.txt_resultados.insert(tk.END, f"  - Tiempo: {tiempo:.6f} segundos\n")
            self.txt_resultados.insert(tk.END, f"  - Conflicto: {conflicto:.2f}\n")
            self.txt_resultados.insert(tk.END, f"  - Esfuerzo: {esfuerzo}\n")
            self.txt_resultados.insert(tk.END, "\n")
        
        # Calcular el mejor
        if resultados:
            mejor = min(resultados, key=lambda x: x[3])  # Menor conflicto
            self.txt_resultados.insert(tk.END, f"Mejor resultado (menor conflicto): {mejor[0]}\n")
            
            mas_rapido = min(resultados, key=lambda x: x[4])  # Menor tiempo
            self.txt_resultados.insert(tk.END, f"Algoritmo más rápido: {mas_rapido[0]} ({mas_rapido[4]:.6f} s)\n")
        
        self.statusbar.config(text="Comparación de algoritmos completada")
    
    def seleccionar_archivo(self):
        """Selecciona un archivo de entrada para cargar una red social"""
        filetypes = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=filetypes)
        
        if ruta:
            self.ruta_archivo_entrada = ruta
            self.lbl_archivo.config(text=os.path.basename(ruta))
            
            try:
                self.statusbar.config(text=f"Cargando red social desde {os.path.basename(ruta)}...")
                self.root.update_idletasks()
                
                self.red_social = cargar_red_social(ruta)
                self.txt_red.delete(1.0, tk.END)
                self.txt_red.insert(tk.END, str(self.red_social))
                
                self.statusbar.config(text=f"Red social cargada desde {os.path.basename(ruta)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
                self.statusbar.config(text="Error al cargar el archivo")
    
    def ejecutar_algoritmo(self, algoritmo, nombre_algoritmo):
        """Método genérico para ejecutar cualquier algoritmo"""
        if not self.red_social:
            messagebox.showwarning("Advertencia", "Primero debe cargar una red social")
            return
        
        self.statusbar.config(text=f"Ejecutando algoritmo {nombre_algoritmo}...")
        self.root.update_idletasks()
        
        try:
            inicio = time.time()
            estrategia, esfuerzo, conflicto = algoritmo(self.red_social)
            fin = time.time()
            
            # Mostramos los resultados
            self.mostrar_resultados(estrategia, esfuerzo, conflicto, nombre_algoritmo, fin - inicio)
            
            self.resultado_actual = (estrategia, esfuerzo, conflicto)
            self.statusbar.config(text=f"Algoritmo {nombre_algoritmo} completado en {fin - inicio:.4f} segundos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar el algoritmo {nombre_algoritmo}: {str(e)}")
            self.statusbar.config(text=f"Error en algoritmo {nombre_algoritmo}")
    
    def ejecutar_fuerza_bruta(self):
        """Ejecuta el algoritmo de fuerza bruta"""
        self.ejecutar_algoritmo(modciFB, "Fuerza Bruta")
    
    def ejecutar_voraz(self):
        """Ejecuta el algoritmo voraz"""
        self.ejecutar_algoritmo(modciV, "Voraz")
    
    def ejecutar_pd(self):
        """Ejecuta el algoritmo de programación dinámica"""
        self.ejecutar_algoritmo(modciPD, "Programación Dinámica")
    
    def mostrar_resultados(self, estrategia, esfuerzo, conflicto, nombre_algoritmo, tiempo):
        """Muestra los resultados de un algoritmo en el área de texto"""
        self.txt_resultados.delete(1.0, tk.END)
        
        resultado = f"Resultados del algoritmo {nombre_algoritmo} (tiempo: {tiempo:.4f} segundos)\n"
        resultado += f"Conflicto interno: {conflicto:.2f}\n"
        resultado += f"Esfuerzo: {esfuerzo}\n"
        resultado += f"Estrategia:\n"
        
        # Mostrar la estrategia para cada grupo
        for i, mod in enumerate(estrategia):
            n_agentes = self.red_social.grupos[i][0]
            resultado += f"  Grupo {i+1}: moderar {mod} de {n_agentes} agentes\n"
        
        self.txt_resultados.insert(tk.END, resultado)
    
    def guardar_resultado(self):
        """Guarda el resultado del último algoritmo ejecutado"""
        if not hasattr(self, 'resultado_actual') or self.resultado_actual is None:
            messagebox.showwarning("Advertencia", "Primero debe ejecutar un algoritmo")
            return
        
        estrategia, esfuerzo, conflicto = self.resultado_actual
        
        filetypes = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        ruta = filedialog.asksaveasfilename(title="Guardar resultado", filetypes=filetypes, defaultextension=".txt")
        
        if ruta:
            try:
                self.statusbar.config(text=f"Guardando resultado...")
                self.root.update_idletasks()
                
                guardar_resultado(ruta, estrategia, conflicto, esfuerzo)
                self.statusbar.config(text=f"Resultado guardado en {os.path.basename(ruta)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el resultado: {str(e)}")
                self.statusbar.config(text="Error al guardar el resultado")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModCIApp(root)
    root.mainloop()