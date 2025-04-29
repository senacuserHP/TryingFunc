import numpy as np
from typing import Dict, List, Tuple
import math

def sistema_recomendacao(avaliacoes: Dict[str, Dict[str, float]], usuario_alvo: str, n_recomendacoes: int = 3) -> List[Tuple[str, float]]:
    """
    Implementa um sistema de recomendação baseado em filtragem colaborativa usando similaridade de cosseno.
    Recomenda itens para um usuário com base nas avaliações de outros usuários.

    Args:
        avaliacoes (Dict[str, Dict[str, float]]): Dicionário onde as chaves são IDs de usuários e os valores são
            dicionários com IDs de itens e suas respectivas avaliações (float).
        usuario_alvo (str): ID do usuário para o qual as recomendações serão geradas.
        n_recomendacoes (int): Número de itens a serem recomendados (padrão: 3).

    Returns:
        List[Tuple[str, float]]: Lista de tuplas contendo o ID do item recomendado e a pontuação prevista.

    Raises:
        ValueError: Se as entradas forem inválidas (ex.: usuário não existe, avaliações vazias).
        TypeError: Se os tipos dos argumentos forem incorretos.
    """
    # Validação de entrada
    if not isinstance(avaliacoes, dict) or not avaliacoes:
        raise TypeError("O argumento 'avaliacoes' deve ser um dicionário não vazio.")
    if not isinstance(usuario_alvo, str):
        raise TypeError("O argumento 'usuario_alvo' deve ser uma string.")
    if not isinstance(n_recomendacoes, int) or n_recomendacoes < 1:
        raise ValueError("O argumento 'n_recomendacoes' deve ser um inteiro positivo.")
    if usuario_alvo not in avaliacoes:
        raise ValueError(f"Usuário '{usuario_alvo}' não encontrado nas avaliações.")

    # Função auxiliar para calcular similaridade de cosseno entre dois usuários
    def similaridade_cosseno(user1: Dict[str, float], user2: Dict[str, float]) -> float:
        """
        Calcula a similaridade de cosseno entre dois usuários com base em suas avaliações.

        Args:
            user1, user2: Dicionários com itens como chaves e avaliações como valores.

        Returns:
            float: Similaridade de cosseno (entre -1 e 1).
        """
        # Encontra itens comuns avaliados por ambos os usuários
        itens_comuns = set(user1.keys()) & set(user2.keys())
        if not itens_comuns:
            return 0.0

        # Calcula vetores para os itens comuns
        vetor1 = np.array([user1[item] for item in itens_comuns])
        vetor2 = np.array([user2[item] for item in itens_comuns])

        # Calcula similaridade de cosseno
        norma1 = np.linalg.norm(vetor1)
        norma2 = np.linalg.norm(vetor2)
        if norma1 == 0 or norma2 == 0:
            return 0.0

        return np.dot(vetor1, vetor2) / (norma1 * norma2)

    try:
        # Calcula similaridades entre o usuário alvo e todos os outros usuários
        similaridades = {}
        for outro_usuario in avaliacoes:
            if outro_usuario != usuario_alvo:
                sim = similaridade_cosseno(avaliacoes[usuario_alvo], avaliacoes[outro_usuario])
                if sim > 0:  # Considera apenas similaridades positivas
                    similaridades[outro_usuario] = sim

        if not similaridades:
            raise ValueError("Nenhum usuário similar encontrado para gerar recomendações.")

        # Identifica itens não avaliados pelo usuário alvo
        itens_avaliados = set(avaliacoes[usuario_alvo].keys())
        todos_itens = set()
        for usuario in avaliacoes:
            todos_itens.update(avaliacoes[usuario].keys())
        itens_nao_avaliados = todos_itens - itens_avaliados

        if not itens_nao_avaliados:
            raise ValueError("Nenhum item disponível para recomendação.")

        # Calcula pontuações previstas para itens não avaliados
        pontuacoes = {}
        for item in itens_nao_avaliados:
            soma_pontuacao = 0.0
            soma_similaridade = 0.0
            for usuario, similaridade in similaridades.items():
                if item in avaliacoes[usuario]:
                    soma_pontuacao += similaridade * avaliacoes[usuario][item]
                    soma_similaridade += similaridade
            if soma_similaridade > 0:
                pontuacoes[item] = soma_pontuacao / soma_similaridade
            else:
                pontuacoes[item] = 0.0

        # Ordena itens por pontuação e retorna as top N recomendações
        recomendacoes = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        return recomendacoes[:min(n_recomendacoes, len(recomendacoes))]

    except Exception as e:
        raise ValueError(f"Erro ao gerar recomendações: {str(e)}")

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Exemplo de matriz de avaliações (usuários -> itens -> notas)
        avaliacoes = {
            "Alice": {"Filme1": 5.0, "Filme2": 3.0, "Filme3": 4.0},
            "Bob": {"Filme1": 4.0, "Filme2": 2.0, "Filme4": 5.0},
            "Charlie": {"Filme2": 4.0, "Filme3": 3.0, "Filme4": 4.0},
            "Diana": {"Filme1": 3.0, "Filme3": 5.0, "Filme4": 2.0}
        }

        # Gera recomendações para Alice
        recomendacoes = sistema_recomendacao(avaliacoes, "Alice", 2)
        print("Recomendações para Alice:")
        for item, pontuacao in recomendacoes:
            print(f"Item: {item}, Pontuação prevista: {pontuacao:.2f}")

    except (ValueError, TypeError) as e:
        print("Erro:", e)