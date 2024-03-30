import re

def cambiar_signo(elemento: str) -> str:
    '''cambiar el signo del predicado dado'''
    return elemento[1:] if elemento.startswith('¬') else '¬' + elemento

def obtener_predicados(clausula: list[str]) -> dict[str, str|bool]:
    '''Obtener el '''
    return [{'completo': parte, 'negado': parte.startswith("¬")} for parte in clausula if '(' in parte or parte.startswith("¬")]

def reducir_clausulas(clausula1: list[str], clausula2: list[str]) -> list[str]:
    '''reduce dos clausulas dadas si tienen predicados contrarios'''
    # Combina dos cláusulas si tienen predicados contrarios, eliminando los predicados que se cancelan entre sí.
    # Si las cláusulas son reducibles, devuelve una nueva cláusula reducida, de lo contrario, devuelve None.
    nueva_clausula = clausula1.copy() + clausula2.copy()
    for parte1 in clausula1:
        for parte2 in clausula2:
            pred1 = obtener_predicados([parte1])[0]
            pred2 = obtener_predicados([parte2])[0]
            if (pred1['completo'].startswith("¬") and pred1['completo'][1:] == pred2['completo']) or \
               (pred2['completo'].startswith("¬") and pred1['completo'] == pred2['completo'][1:]):
                nueva_clausula = clausula1.copy()
                nueva_clausula.remove(parte1)
                nueva_clausula += clausula2.copy()
                nueva_clausula.remove(parte2)
    
    if nueva_clausula != clausula1 + clausula2:
        # Eliminar elementos duplicados y vacíos
        nueva_clausula = list(filter(lambda x: x.strip() != "" and nueva_clausula.count(x) == 1, nueva_clausula))
        return nueva_clausula
    else:
        return None


def resolucion(clausulas_actuales: list[str], estado: str) -> bool:
    '''Resuelve por inferencia de resolucion'''
    # Itera sobre las cláusulas actuales y las reduce hasta que se alcanza un estado de resolución o se detecta un bucle infinito.
    # Devuelve True si la pregunta se resuelve, False si hay un bucle infinito.
    estado_actual = [cambiar_signo(estado)]
    estados_previos = set()
    while True:
        
        for clausula in clausulas_actuales:
            estado_siguiente = reducir_clausulas(clausula, estado_actual)
            
            if estado_siguiente == []:
                print(f'inicio:{clausula} \nactual:{estado_actual} \nresultado:{estado_siguiente}\n\n')
                return True
            elif estado_siguiente not in clausulas_actuales:
                if estado_siguiente is not None:  # Agregamos la condición para imprimir solo cuando estado_siguiente no es None
                    print(f'inicio:{clausula} \nactual:{estado_actual} \nresultado:{estado_siguiente}\n\n')
                else:
                    continue
                
            estado_actual = estado_siguiente 

        if tuple(estado_actual) not in estados_previos:
            estados_previos.add(tuple(estado_actual))
        else:
            # Si no se agregan nuevos estados, asumimos un bucle infinito y retornamos False
            return False

        

def separar_clausulas(clausulas: list[str]) -> list[list[str]]:
    '''Dividir la base de conocimiento en arreglos de arreglos'''
    return [re.split(r'\s+v\s+', line.strip()) for line in clausulas]

def main() -> None:
    
    base_conocimiento_inicial = [
        "Hombre(Marco)",
        "Pompeyano(Marco)",
        "¬Pompeyano(Marco) v Romano(Marco)",
        "Gobernante(Cesar)",
        "¬Romano(Marco) v Leal(Marco, Cesar) v Odia(Marco, Cesar)",
        "¬Hombre(Marco) v ¬Gobernante(Cesar) v ¬IntentaAsesinar(Marco, Cesar) v ¬Leal(Marco, Cesar)",
        "IntentaAsesinar(Marco, Cesar)"
    ]

    pregunta = "Odia(Marco, Cesar)"
    clausulas_actuales = separar_clausulas(base_conocimiento_inicial)
    if resolucion(clausulas_actuales, pregunta):
        print("siuu") 
    else:
        print("jueputa")
    

if __name__ == '__main__':
    main()
