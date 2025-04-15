"""
Utilidades combinadas para tema e interfaz de usuario de la aplicación ModCI
"""
import tkinter as tk
from tkinter import ttk, font

class UIManager:
    """Clase para gestionar la interfaz de usuario y los temas de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        
        # Definir tema único (claro)
        self.theme = {
            "bg": "#f5f5f5",
            "fg": "#333333",
            "text_bg": "white",
            "border": "#dddddd"
        }
        
        # Configurar el tema
        self.apply_theme()
    
    def apply_theme(self):
        """Aplica el tema a la aplicación"""
        theme = self.theme
        
        # Configurar fuentes
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        
        heading_font = font.Font(family="Segoe UI", size=12, weight="bold")
        
        # Configurar estilos
        style = ttk.Style()
        
        # Estilos generales
        style.configure(".", background=theme["bg"], foreground=theme["fg"])
        
        # Frame y LabelFrame
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabelframe", background=theme["bg"])
        style.configure("TLabelframe.Label", background=theme["bg"], foreground=theme["fg"], font=heading_font)
        
        # Label
        style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        
        # Botones simplificados
        style.configure("TButton", padding=(5, 2))
        
        # Mantener los estilos específicos pero con aspecto sencillo
        style.configure("Primario.TButton", padding=(5, 2))
        style.configure("Secundario.TButton", padding=(5, 2))
        style.configure("Acento.TButton", padding=(5, 2))
        
        # Configuración global
        self.root.configure(background=theme["bg"])
        
        # Configuración para ScrolledText y otros widgets de texto
        self.text_config = {
            "bg": theme["text_bg"],
            "fg": theme["fg"],
            "font": ("Consolas", 10),
            "selectbackground": "#a6a6a6",
            "selectforeground": "white",
            "borderwidth": 1,
            "relief": "solid",
            "insertbackground": theme["fg"]  # Color del cursor
        }
        
        return self.text_config
    
    # Método toggle_theme eliminado ya que no será necesario
    
    def get_text_config(self):
        """Devuelve la configuración para widgets de texto"""
        return self.text_config
    
    def get_current_theme(self):
        """Devuelve el nombre del tema actual"""
        return self.current_theme

def create_tooltip(widget, text):
    """Crea un tooltip para un widget"""
    tooltip = tk.Label(widget.master, text=text, background="#ffffe0", relief="solid", borderwidth=1)
    tooltip.config(font=("Segoe UI", 8))
    
    def enter(event):
        x = widget.winfo_rootx() + widget.winfo_width() // 2
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        tooltip.lift()
        tooltip.place(x=x, y=y, anchor="n")
    
    def leave(event):
        tooltip.place_forget()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    
    return tooltip

def create_button(parent, text, command, style="TButton", tooltip_text=None):
    """
    Crea un botón con estilo y opcionalmente un tooltip
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        style: Estilo del botón (TButton, Primario.TButton, etc.)
        tooltip_text: Texto del tooltip (opcional)
    
    Returns:
        El botón creado
    """
    btn = ttk.Button(parent, text=text, command=command, style=style)
    
    if tooltip_text:
        create_tooltip(btn, tooltip_text)
        
    return btn

def setup_scrolled_text(parent, height=10, **kwargs):
    """
    Crea y configura un widget ScrolledText
    
    Args:
        parent: Widget padre
        height: Altura del widget en líneas
        **kwargs: Argumentos adicionales para configurar el widget
    
    Returns:
        El widget ScrolledText creado
    """
    from tkinter import scrolledtext
    
    txt = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=height)
    txt.configure(**kwargs)
    
    return txt