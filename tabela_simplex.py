import copy
from math import isclose
from solver import resolver_ppl  # usa sua função existente (pulp)

TOL = 1e-8

class AnalisadorSimplex:
    def __init__(self, c, A, b, senses):
        """
        c: lista coef funç obj
        A: lista de listas (m x n)
        b: lista (m)
        senses: lista de strings ("<=", ">=", "=")
        """
        self.c = c
        self.A = [list(row) for row in A]
        self.b = list(b)
        self.senses = list(senses)
        self.m = len(self.b)
        self.n = len(self.c)

    def _augmented_values(self, ponto):
        """
        Retorna vetor com valores das variáveis originais (x) seguidos
        pelas folgas/surplus (na ordem das restrições).
        - Para "<=": folga = b - A x
        - Para ">=": surplus = A x - b
        - Para "=": valor residual = 0 (ou b - A x, mas tratamos como 0)
        """
        x = ponto
        residuals = []
        for i in range(self.m):
            lhs = sum(self.A[i][j] * x[j] for j in range(self.n))
            if self.senses[i] == "<=":
                residuals.append(self.b[i] - lhs)
            elif self.senses[i] == ">=":
                residuals.append(lhs - self.b[i])
            else:  # "="
                residuals.append(self.b[i] - lhs)
        return x + residuals  # comprimento n + m

    def analisar_alteracoes(self, delta_b, ponto_otimo, precos_sombra, lucro_original, folgas):
        """
        delta_b: lista de alterações propostas (comprimento m)
        ponto_otimo: lista de valores das variáveis originais x (comprimento n)
        precos_sombra: lista de preços-sombra (comprimento m)
        lucro_original: valor Z*
        folgas: lista de folgas retornadas pelo solver (comprimento m) -- não imprescindível aqui
        Retorna dicionário com:
          - viavel (bool)
          - condicoes_viabilidade: lista de strings com as expressões
          - resultados_viabilidade: lista "OK" / "NÃO VIÁVEL"
          - novo_lucro, variacao_lucro
        """
        m = self.m
        if len(delta_b) != m:
            raise ValueError("delta_b deve ter comprimento m (número de restrições)")

        # valores originais (variáveis + folgas/surplus)
        augmented_orig = self._augmented_values(ponto_otimo)
        total_aug = self.n + self.m  # tamanho do vetor augmentado

        # Vamos estimar numericamente as colunas de B^{-1} (m colunas) resolvendo m LPs
        # com b + e_j (unitário em cada restrição). Para cada j calculamos:
        # delta_aug_col_j = augmented(b + e_j) - augmented_orig
        # Assim, qualquer alteração generalizada Δb dá: Δaug = sum_j delta_aug_col_j * Δb_j
        cols = []  # lista de colunas (cada coluna é vetor comprimento total_aug)
        for j in range(m):
            # construir b' = b + e_j
            b_prime = copy.deepcopy(self.b)
            b_prime[j] = b_prime[j] + 1.0  # incremento unitário

            # resolver LP com novo b' (usamos resolver_ppl já existente)
            try:
                res_prime = resolver_ppl(self.c, self.A, b_prime, self.senses)
            except Exception as e:
                # se por algum motivo falhar, devolvemos erro controlado
                raise RuntimeError(f"Falha ao resolver LP de teste para coluna {j+1}: {e}")

            x_prime = res_prime["ponto"]
            # augmented prime
            augmented_prime = self._augmented_values(x_prime)
            # delta column: prime - orig
            col = [augmented_prime[k] - augmented_orig[k] for k in range(total_aug)]
            cols.append(col)

        # Agora montamos as expressões para cada linha básica que consideramos relevante.
        # Vamos considerar como "linhas a verificar" as m linhas correspondentes às restrições,
        # mas apresentar as expressões por variável básica detectada (preferimos mostrar as m linhas da tabela final).
        # Para exibição simples, geramos m expressões correspondentes às m restrições (linhas do tableau).
        condicoes = []
        resultados = []
        # Para apresentar coeficientes, usamos as linhas correspondentes às últimas m entradas do vetor augmentado
        # (i.e., as folgas/surplus) — são as que representam diretamente as linhas do tableau.
        # índice base das linhas na augmented vector: n .. n+m-1
        for row_idx in range(self.n, self.n + m):
            # coeficientes para Δ1..Δm são cols[col_j][row_idx]
            coefs = [cols[j][row_idx] for j in range(m)]
            const_term = augmented_orig[row_idx]  # valor independente (ex.: 41.67)
            # montar expressão string bonita: ex "Δ1 - 0,39·Δ2 - 0,21·Δ3 + 41,67 ≥ 0"
            parts = []
            for j, coef in enumerate(coefs):
                # pular coef aproximadamente zero
                if isclose(coef, 0.0, abs_tol=1e-9):
                    parts.append(f"{0:+.2f}·Δ{j+1}")  # mostra 0.00*Δj para consistência (ou poderíamos pular)
                else:
                    # formatar sinal e valor
                    sign = "+" if coef >= 0 else "-"
                    parts.append(f"{sign} {abs(coef):.2f}·Δ{j+1}")
            # juntar partes e o termo constante
            expr = " ".join(parts) + f" + {const_term:.2f} ≥ 0"
            # avaliar com delta_b fornecido
            val = const_term + sum(coefs[j] * delta_b[j] for j in range(m))
            condicoes.append(expr)
            resultados.append("OK" if val >= -1e-8 else "NÃO VIÁVEL")

        viavel = all(r == "OK" for r in resultados)

        # cálculo do novo lucro (se viável): variação linear usando preços-sombra
        if viavel:
            variacao_lucro = sum(precos_sombra[i] * delta_b[i] for i in range(m))
            novo_lucro = lucro_original + variacao_lucro
        else:
            variacao_lucro = 0.0
            novo_lucro = lucro_original

        # Para maior usabilidade também devolvemos as avaliações numéricas de cada condição
        avaliacoes = []
        for row_idx in range(self.n, self.n + m):
            const_term = augmented_orig[row_idx]
            coefs = [cols[j][row_idx] for j in range(m)]
            val = const_term + sum(coefs[j] * delta_b[j] for j in range(m))
            avaliacoes.append(val)

        return {
            "viavel": viavel,
            "condicoes_viabilidade": condicoes,
            "resultados_viabilidade": resultados,
            "avaliacoes": avaliacoes,
            "novo_lucro": novo_lucro,
            "variacao_lucro": variacao_lucro
        }
