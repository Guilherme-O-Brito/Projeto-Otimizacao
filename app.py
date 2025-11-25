import streamlit as st
from solver import resolver_ppl
from tabela_simplex import AnalisadorSimplex

st.set_page_config(page_title="Calculadora de Simplex", layout="centered")

st.title("#CALCULADORA SIMPLEX#")
st.write("Método Simplex Tableu em Python MADE WITH Streamlit")

# ENTRADA DA FUNÇÃO OBJETIVO
st.header("1 -> Função Objetivo (Maximizar)")
c_str = st.text_input("Coeficientes da função objetivo (ex: 12 60)")
c = list(map(float, c_str.split())) if c_str else []

# RESTRIÇÕES
st.header("2 -> Restrições")
n = st.number_input("Número de restrições", min_value=1, max_value=5, step=1)

A, b, senses = [], [], []

for i in range(n):
    st.subheader(f"Restrição {i+1}")

    coef = st.text_input(f"Coeficientes da restrição {i+1} (ex: 2 1)", key=f"A{i}")
    op = st.selectbox("Operador", ["<=", ">=", "="], key=f"op{i}")
    rhs = st.number_input("Lado direito (b)", key=f"b{i}")

    if coef:
        A.append(list(map(float, coef.split())))
        b.append(rhs)
        senses.append(op)

# ALTERAÇÕES EM b
st.header("3 -> Alterações nas restrições")
st.write("Digite as variações Δb para cada restrição (ex: 250 0 0)")

alteracoes_str = st.text_input("Variações Δb (separadas por espaço):")
if alteracoes_str:
    delta_b = list(map(float, alteracoes_str.split()))
else:
    delta_b = [0] * n

# BOTÃO PARA RESOLVER
if st.button(" Resolver Simplex"):
    if not c or not A:
        st.error("Preencha a função objetivo e as restrições corretamente.")
    else:
        resultado = resolver_ppl(c, A, b, senses)

        st.success("Simplex resolvido com sucesso!")

        st.subheader("Solução Ótima")
        for i, ponto in enumerate(resultado["ponto"]):
            st.write(f"x{i+1} = {ponto:.2f}")

        st.subheader("Lucro ótimo (Z*)")
        st.write(f"R$ {resultado['lucro']:.2f}")

        st.subheader("Preços-sombra")
        for i, sombra in enumerate(resultado["sombra"]):
            st.write(f"Restrição {i+1}: R$ {sombra:.2f}")

        # ANÁLISE DAS ALTERAÇÕES - APENAS 4 LINHAS
        if alteracoes_str:
            st.header("4 -> Análise das variações")
            
            analisador = AnalisadorSimplex(c, A, b, senses)
            analise = analisador.analisar_alteracoes(
                delta_b=delta_b,
                ponto_otimo=resultado["ponto"],
                precos_sombra=resultado["sombra"],
                lucro_original=resultado["lucro"],
                folgas=resultado["folga"]
            )
            
            # LINHA 1: Condições de viabilidade
            st.subheader("Condições de viabilidade:")
            for condicao, resultado_cond in zip(analise["condicoes_viabilidade"], analise["resultados_viabilidade"]):
                if "OK" in resultado_cond:
                    st.success(f"✓ {condicao}")
                else:
                    st.error(f"✗ {condicao}")
            
            # LINHA 2: Resultado geral
            st.subheader("Resultado:")
            if analise["viavel"]:
                st.success("✓ SOLUÇÃO VIÁVEL")
            else:
                st.error("✗ SOLUÇÃO INVIÁVEL")
            
            # LINHA 3: Cálculo do novo lucro (apenas se viável)
            if analise["viavel"]:
                st.subheader("Novo lucro:")
                st.write(f"Z_novo = {resultado['lucro']:.0f} + {analise['variacao_lucro']:.0f} = R$ {analise['novo_lucro']:.0f}")