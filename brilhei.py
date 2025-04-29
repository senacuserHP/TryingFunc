def calcular_estatisticas(numeros):


    if not isinstance(numeros, list):
        raise TypeError("O argumento deve ser uma lista")

    if not numeros:
        raise ValueError("A lista nao pode estar vazia")

    for num in numeros:
        if not isinstance(num, (int, float)):
            raise ValueError(f"elemento invalido encontrado: {num}")

    try:
        # Média
        media = sum(numeros) / len(numeros)
        
        # Ordena a lista para mediana
        lista_ordenada = sorted(numeros)
        n = len(lista_ordenada)
        
        # Mediana
        if n % 2 == 0:
            mediana = (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2
        else:
            mediana = lista_ordenada[n//2]
        
        # Mínimo e máximo
        minimo = min(numeros)
        maximo = max(numeros)
        
        # Retorna resultados em um dicionário
        return {
            "media": round(media, 2),
            "mediana": round(mediana, 2),
            "minimo": minimo,
            "maximo": maximo
        }
    
    except Exception as e:
        raise ValueError(f"Erro ao calcular estatísticas: {str(e)}")

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Teste com uma lista válida
        dados = [10, 20, 15, 25, 30, 22]
        resultado = calcular_estatisticas(dados)
        print("Estatísticas:", resultado)
        
        # Teste com erro (lista com string)
        dados_invalidos = [10, 20, "30", 40]
        resultado = calcular_estatisticas(dados_invalidos)
        
    except ValueError as ve:
        print("Erro:", ve)
    except TypeError as te:
        print("Erro:", te)