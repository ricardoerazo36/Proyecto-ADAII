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
        
        # Definir temas
        self.themes = {
            "light": {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "primary": "#3366cc",
                "secondary": "#6699cc",
                "accent": "#ff6633",
                "success": "#66cc99",
                "warning": "#ffcc33",
                "error": "#ff3366",
                "text_bg": "white",
                "border": "#dddddd"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#f5f5f5",
                "primary": "#5588ee",
                "secondary": "#88aaee",
                "accent": "#ff8855",
                "success": "#77ddaa",
                "warning": "#ffdd55",
                "error": "#ff5577",
                "text_bg": "#383838",
                "border": "#555555"
            },
            "blue": {
                "bg": "#e6f0ff",
                "fg": "#333333",
                "primary": "#1a53ff",
                "secondary": "#4d79ff",
                "accent": "#ff6633",
                "success": "#33cc66",
                "warning": "#ffcc00",
                "error": "#ff3366",
                "text_bg": "white",
                "border": "#b3d1ff"
            }
        }
        
        # Configurar el tema inicial
        self.apply_theme("light")
    
    def apply_theme(self, theme_name):
        """Aplica un tema a la aplicación"""
        if theme_name not in self.themes:
            return
        
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
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
        
        # Button - Corrección de los botones para que se vean adecuadamente
        style.configure("TButton", 
                        background=theme["primary"], 
                        foreground="white", 
                        padding=(10, 5),
                        relief="raised")
                        
        # Importante: usar map para definir los estados del botón
        style.map("TButton",
                 background=[("active", theme["secondary"]), ("pressed", theme["primary"])],
                 foreground=[("active", "white"), ("pressed", "white")],
                 relief=[("pressed", "sunken"), ("active", "raised")])
        
        # Estilos específicos para botones
        style.configure("Primario.TButton", 
                        background=theme["primary"], 
                        foreground="white",
                        padding=(10, 5))
        style.map("Primario.TButton",
                  background=[("active", theme["secondary"]), ("pressed", theme["primary"])],
                  foreground=[("active", "white"), ("pressed", "white")],
                  relief=[("pressed", "sunken"), ("active", "raised")])
        
        style.configure("Secundario.TButton", 
                        background=theme["secondary"], 
                        foreground="white",
                        padding=(10, 5))
        style.map("Secundario.TButton",
                  background=[("active", theme["primary"]), ("pressed", theme["secondary"])],
                  foreground=[("active", "white"), ("pressed", "white")],
                  relief=[("pressed", "sunken"), ("active", "raised")])
        
        style.configure("Acento.TButton", 
                        background=theme["accent"], 
                        foreground="white",
                        padding=(10, 5))
        style.map("Acento.TButton",
                  background=[("active", "#ff8866"), ("pressed", theme["accent"])],
                  foreground=[("active", "white"), ("pressed", "white")],
                  relief=[("pressed", "sunken"), ("active", "raised")])
        
        # Configuración global
        self.root.configure(background=theme["bg"])
        
        # Configuración para ScrolledText y otros widgets de texto
        self.text_config = {
            "bg": theme["text_bg"],
            "fg": theme["fg"],
            "font": ("Consolas", 10),
            "selectbackground": theme["primary"],
            "selectforeground": "white",
            "borderwidth": 1,
            "relief": "solid",
            "insertbackground": theme["fg"]  # Color del cursor
        }
        
        return self.text_config
    
    def toggle_theme(self):
        """Cambia entre temas disponibles"""
        themes = list(self.themes.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        next_theme = themes[next_index]
        
        return self.apply_theme(next_theme)
    
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