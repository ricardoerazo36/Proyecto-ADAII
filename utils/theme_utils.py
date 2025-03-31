"""
Gestor de temas para la aplicación ModCI
"""
import tkinter as tk
from tkinter import ttk, font

class ThemeManager:
    """Clase para gestionar los temas de la aplicación"""
    
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
        
        # Button
        style.configure("TButton", background=theme["primary"], foreground="white")
        style.map("TButton",
                 background=[("active", theme["secondary"]), ("pressed", theme["primary"])],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Estilos específicos para botones
        style.configure("Primario.TButton", background=theme["primary"], foreground="white")
        style.map("Primario.TButton",
                  background=[("active", theme["secondary"]), ("pressed", theme["primary"])])
        
        style.configure("Secundario.TButton", background=theme["secondary"], foreground="white")
        style.map("Secundario.TButton",
                  background=[("active", theme["primary"]), ("pressed", theme["secondary"])])
        
        style.configure("Acento.TButton", background=theme["accent"], foreground="white")
        style.map("Acento.TButton",
                  background=[("active", "#ff8866"), ("pressed", theme["accent"])])
        
        # Configuración global
        self.root.configure(background=theme["bg"])
        
        # Configuración para ScrolledText
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

def create_tooltip(widget, text):
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