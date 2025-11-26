# Calculadora Simplex

Aplicação web interativa para resolução de problemas de programação linear usando o Método Simplex com interface gráfica em Streamlit.

## 👥 Participantes do Projeto

- **Guilherme Brito** 
- **Rodrigo Armengol**

## 📋 Descrição

Este projeto implementa uma calculadora para o Método Simplex Tableau, permitindo:

- Definir função objetivo (maximização)
- Adicionar múltiplas restrições (≤, ≥, =)
- Resolver problemas de programação linear
- Analisar alterações nas restrições (análise de sensibilidade)
- Visualizar preços-sombra e folgas
- Gerar tabelas do método Simplex passo a passo

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação
- **Streamlit**: Framework para interface web
- **PuLP**: Biblioteca para resolução de problemas de otimização linear
- **NumPy**: Operações numéricas

## 📂 Estrutura do Projeto

```
Tableu/
├── app.py              # Interface principal Streamlit
├── solver.py           # Solver de programação linear usando PuLP
├── tabela_simplex.py   # Analisador Simplex 
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 🚀 Como Usar

### 1. Instalação das Dependências

Primeiro, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Executar o Programa

Para rodar a aplicação, execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

### 3. Usando a Interface

1. **Função Objetivo**: Digite os coeficientes da função objetivo separados por espaço (ex: `12 60`)

2. **Número de Restrições**: Selecione quantas restrições seu problema possui (1 a 5)

3. **Definir Restrições**: Para cada restrição, forneça:
   - Coeficientes separados por espaço (ex: `2 1`)
   - Operador (≤, ≥, ou =)
   - Valor do lado direito (b)

4. **Alterações em b (opcional)**: Digite as variações Δb para análise de sensibilidade (ex: `250 0 0`)

5. **Resolver**: Clique no botão "Resolver Simplex" para obter:
   - Solução ótima
   - Valor da função objetivo
   - Preços-sombra
   - Análise de sensibilidade
   - Tableau Simplex detalhado

## 📊 Exemplo de Uso

**Problema:**
- Maximizar: Z = 12x₁ + 60x₂
- Sujeito a:
  - 2x₁ + x₂ ≤ 100
  - x₁ + 2x₂ ≤ 150
  - x₁, x₂ ≥ 0

**Entrada na Interface:**
- Função objetivo: `12 60`
- Número de restrições: `2`
- Restrição 1: coeficientes `2 1`, operador `≤`, lado direito `100`
- Restrição 2: coeficientes `1 2`, operador `≤`, lado direito `150`

## 📝 Funcionalidades

### Módulo `solver.py`
Resolve problemas de programação linear usando a biblioteca PuLP, retornando:
- Ponto ótimo
- Valor da função objetivo
- Preços-sombra das restrições
- Folgas

### Módulo `tabela_simplex.py`
Realiza análise detalhada do Simplex:
- Análise de sensibilidade
- Verificação de viabilidade após alterações
- Geração de tabelas Simplex iterativas
- Identificação de variáveis básicas e não-básicas

### Interface `app.py`
Fornece interface amigável com:
- Entrada intuitiva de dados
- Visualização de resultados
- Tabelas formatadas
- Análise de alterações em tempo real

## 📄 Requisitos

- Python 3.7 ou superior
- Sistema operacional: Windows, Linux ou macOS

## 📖 Disciplina

Projeto desenvolvido para a disciplina **M210 - Otimização** do Inatel.

---