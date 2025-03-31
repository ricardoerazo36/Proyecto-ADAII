import numpy as np

class RedSocial:
    def __init__(self, grupos, r_max):
        self.grupos = grupos  # Lista de tuplas (n_agentes, opinion1, opinion2, rigidez)
        self.r_max = r_max
        self.n = len(grupos)
    
    def calcular_conflicto_interno(self, estrategia=None):
        """Calcula el conflicto interno de la red con la estrategia aplicada o sin estrategia"""
        if estrategia is None:
            estrategia = [0] * self.n
        
        suma_numerador = 0
        suma_agentes = 0
        
        for i in range(self.n):
            n_agentes, op1, op2, rigidez = self.grupos[i]
            mod_agentes = estrategia[i]
            
            # Agentes no modificados mantienen sus opiniones originales
            if n_agentes > mod_agentes and mod_agentes >= 0:
                suma_numerador += (n_agentes - mod_agentes) * ((op1 - op2) ** 2)
                suma_agentes += (n_agentes - mod_agentes)
            
        return suma_numerador / max(1, suma_agentes)
    
    def calcular_esfuerzo(self, estrategia):
        """Calcula el esfuerzo necesario para aplicar una estrategia de moderación"""
        esfuerzo_total = 0
        
        for i in range(self.n):
            n_agentes, op1, op2, rigidez = self.grupos[i]
            mod_agentes = estrategia[i]
            
            if mod_agentes > 0:
                esfuerzo_grupo = np.ceil(abs(op1 - op2) * rigidez * mod_agentes)
                esfuerzo_total += esfuerzo_grupo
                
        return esfuerzo_total
    
    def estrategia_aplicable(self, estrategia):
        """Verifica si una estrategia es aplicable dada la restricción de R_max"""
        return self.calcular_esfuerzo(estrategia) <= self.r_max
    
    def aplicar_estrategia(self, estrategia):
        """Devuelve una nueva red social tras aplicar la estrategia de moderación"""
        nuevos_grupos = []
        
        for i in range(self.n):
            n_agentes, op1, op2, rigidez = self.grupos[i]
            mod_agentes = estrategia[i]
            
            if mod_agentes > 0 and mod_agentes <= n_agentes:
                # Los agentes moderados ahora tienen el mismo valor para ambas opiniones
                # Promedio de opiniones como valor final 
                op_promedio = (op1 + op2) / 2
                
                # Agentes no modificados
                if n_agentes - mod_agentes > 0:
                    nuevos_grupos.append((n_agentes - mod_agentes, op1, op2, rigidez))
                
                # Agentes modificados (si hay)
                if mod_agentes > 0:
                    nuevos_grupos.append((mod_agentes, op_promedio, op_promedio, rigidez))
            else:
                # Grupo que no se modifica
                nuevos_grupos.append((n_agentes, op1, op2, rigidez))
        
        return RedSocial(nuevos_grupos, self.r_max)
    
    def __str__(self):
        resultado = f"Red Social con {self.n} grupos de agentes y R_max = {self.r_max}\n"
        for i, (n_agentes, op1, op2, rigidez) in enumerate(self.grupos):
            resultado += f"Grupo {i}: {n_agentes} agentes, opinión1 = {op1}, opinión2 = {op2}, rigidez = {rigidez}\n"
        return resultado