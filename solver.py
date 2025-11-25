import pulp

def resolver_ppl(c, A, b, senses):
    """
    Resolve um problema de programação linear usando o método Simplex
    """
    m = len(A)
    n = len(c)

    model = pulp.LpProblem("Simplex", pulp.LpMaximize)

    # Variáveis
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n)]

    # Função objetivo
    model += pulp.lpSum(c[j] * x[j] for j in range(n)), "Funcao_Objetivo"

    # Restrições
    for i in range(m):
        expr = pulp.lpSum(A[i][j] * x[j] for j in range(n))
        if senses[i] == "<=":
            model += expr <= b[i], f"R{i+1}"
        elif senses[i] == ">=":
            model += expr >= b[i], f"R{i+1}"
        else:
            model += expr == b[i], f"R{i+1}"

    model.solve()

    # Resultados
    ponto = [v.value() for v in x]
    lucro = pulp.value(model.objective)

    # Preços-sombra
    sombra = [model.constraints[f"R{i+1}"].pi for i in range(m)]
    
    # Folga ainda calculada internamente para uso na análise
    folga = [model.constraints[f"R{i+1}"].slack for i in range(m)]

    return {
        "ponto": ponto,
        "lucro": lucro,
        "sombra": sombra,
        "folga": folga
    }