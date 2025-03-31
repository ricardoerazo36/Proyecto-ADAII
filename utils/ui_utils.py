"""
Utilidades para la interfaz de usuario de la aplicación ModCI
"""
import tkinter as tk
from tkinter import ttk, font

def configurar_estilo():
    """Configura el estilo visual de la aplicación"""
    # Colores
    colores = {
        'fondo': '#f5f5f5',
        'texto': '#333333',
        'primario': '#3366cc',
        'secundario': '#6699cc',
        'acento': '#ff6633',
        'exito': '#66cc99',
        'advertencia': '#ffcc33',
        'error': '#ff3366'
    }
    
    # Configurar estilo ttk
    style = ttk.Style()
    
    # Crear fuente personalizada
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)
    
    heading_font = font.Font(family="Segoe UI", size=12, weight="bold")
    
    # Configurar estilos
    style.configure('TFrame', background=colores['fondo'])
    style.configure('TLabelframe', background=colores['fondo'])
    style.configure('TLabelframe.Label', background=colores['fondo'], foreground=colores['texto'], font=heading_font)
    
    style.configure('TLabel', background=colores['fondo'], foreground=colores['texto'])
    style.configure('TButton', background=colores['primario'], foreground='white', font=default_font)
    style.map('TButton',
              background=[('active', colores['secundario']), ('pressed', colores['primario'])],
              foreground=[('active', 'white'), ('pressed', 'white')])
    
    # Estilo para botones por categoría
    style.configure('Primario.TButton', background=colores['primario'], foreground='white')
    style.map('Primario.TButton',
              background=[('active', colores['secundario']), ('pressed', colores['primario'])])
    
    style.configure('Secundario.TButton', background=colores['secundario'], foreground='white')
    style.map('Secundario.TButton',
              background=[('active', colores['primario']), ('pressed', colores['secundario'])])
    
    style.configure('Acento.TButton', background=colores['acento'], foreground='white')
    style.map('Acento.TButton',
              background=[('active', '#ff8866'), ('pressed', colores['acento'])])
    
    # Configurar ScrolledText
    texto_config = {
        'bg': 'white',
        'fg': colores['texto'],
        'font': ('Consolas', 10),
        'selectbackground': colores['primario'],
        'selectforeground': 'white',
        'borderwidth': 1,
        'relief': 'solid'
    }
    
    return style, colores, texto_config

def crear_tooltip(widget, text):
    """Crea un tooltip para un widget"""
    tooltip = tk.Label(widget.master, text=text, background="#ffffe0", relief="solid", borderwidth=1)
    tooltip.config(font=("Segoe UI", 8))
    
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.lift()
        tooltip.place(x=x, y=y)
    
    def leave(event):
        tooltip.place_forget()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    
    return tooltip