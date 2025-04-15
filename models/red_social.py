import numpy as np

class RedSocial:
    def __init__(self, grupos, r_max):
        self.grupos = grupos  # Lista de tuplas (n_agentes, opinion1, opinion2, rigidez)
        self.r_max = r_max
        self.n = len(grupos)
    
    def calcular_conflicto_interno(self, estrategia=None):
        """
        Calcula el conflicto interno de la red con la estrategia aplicada
        CI(RS) = sum(n_i * (o_i1 - o_i2)^2) / n, donde n es el total de agentes
        """
        if estrategia is None:
            # Si no hay estrategia, calcula el CI original
            suma_numerador = 0
            total_agentes = 0
            
            for n_agentes, op1, op2, _ in self.grupos:
                suma_numerador += n_agentes * ((op1 - op2) ** 2)
                total_agentes += n_agentes
                
            return suma_numerador / total_agentes
        else:
            # Aplicamos la estrategia y calculamos el nuevo CI
            nueva_red = self.aplicar_estrategia(estrategia)
            return nueva_red.calcular_conflicto_interno()
    
    def calcular_esfuerzo(self, estrategia):
        """
        Calcula el esfuerzo necesario para aplicar una estrategia de moderación
        Esfuerzo(RS, E) = sum(ceil(|o_i1 - o_i2| * r_i * e_i))
        """
        esfuerzo_total = 0
        
        for i in range(self.n):
            n_agentes, op1, op2, rigidez = self.grupos[i]
            mod_agentes = estrategia[i]
            
            if mod_agentes > 0:
                # Usamos ceil como indica la fórmula
                esfuerzo_grupo = int(np.ceil(abs(op1 - op2) * rigidez * mod_agentes))
                esfuerzo_total += esfuerzo_grupo
                
        return esfuerzo_total
    
    def estrategia_aplicable(self, estrategia):
        """Verifica si una estrategia es aplicable dada la restricción de R_max"""
        return self.calcular_esfuerzo(estrategia) <= self.r_max
    
    def aplicar_estrategia(self, estrategia):
        """
        Devuelve una nueva red social tras aplicar la estrategia de moderación
        Cuando se modera un agente, sus dos opiniones se igualan
        """
        nuevos_grupos = []
        
        for i in range(self.n):
            n_agentes, op1, op2, rigidez = self.grupos[i]
            mod_agentes = estrategia[i]
            
            if mod_agentes > n_agentes:
                mod_agentes = n_agentes  # No podemos moderar más agentes de los que hay
                
            # Agentes no modificados (mantienen sus opiniones originales)
            agentes_no_mod = n_agentes - mod_agentes
            if agentes_no_mod > 0:
                nuevos_grupos.append((agentes_no_mod, op1, op2, rigidez))
            
            # Agentes modificados (ahora tienen la misma opinión en ambas afirmaciones)
            # Según el enunciado, cuando se modera un agente, sus opiniones se vuelven iguales
            if mod_agentes > 0:
                # Opinión promedio como valor final (podría ser o_i1 o o_i2, el enunciado no especifica)
                op_promedio = (op1 + op2) / 2
                nuevos_grupos.append((mod_agentes, op_promedio, op_promedio, rigidez))
        
        return RedSocial(nuevos_grupos, self.r_max)
    
    def total_agentes(self):
        """Devuelve el número total de agentes en la red"""
        return sum(grupo[0] for grupo in self.grupos)
    
    def __str__(self):
        resultado = f"Red Social con {self.n} grupos de agentes y R_max = {self.r_max}\n"
        for i, (n_agentes, op1, op2, rigidez) in enumerate(self.grupos):
            resultado += f"Grupo {i}: {n_agentes} agentes, opinión1 = {op1}, opinión2 = {op2}, rigidez = {rigidez}\n"
        return resultado