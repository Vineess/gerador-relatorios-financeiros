# Gerador de Relatórios Financeiros Automáticos

Este projeto oferece uma solução simples para gerar relatórios financeiros a partir de planilhas de despesas e receitas. Ele calcula o total de receitas, total de despesas, lucro líquido, e gera um gráfico em formato PDF.

## Como Usar

### Pré-requisitos
- Python 3.x
- Pandas
- Matplotlib
- FPDF

### Passos:
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gerador-relatorios-financeiros.git
   cd gerador-relatorios-financeiros

2. Crie um ambiente virtual:

    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Instale as dependências:

    pip install -r requirements.txt

4. Coloque sua planilha CSV de despesas e receitas na pasta data/ com o formato:

    Descrição, Valor, Tipo (Receita/Despesa), Data (opcional)

5.  Execute o script:

    python src/gerar_relatorio.py

