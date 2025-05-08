import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Função para ler a planilha e processar os dados
def processar_planilha(caminho_arquivo):
    # Carregar os dados da planilha (assumindo um arquivo CSV para simplificação)
    df = pd.read_csv(caminho_arquivo)

    # Separar Receitas e Despesas
    receitas = df[df['Tipo'] == 'Receita']
    despesas = df[df['Tipo'] == 'Despesa']

    # Calcular totais
    total_receitas = receitas['Valor'].sum()
    total_despesas = despesas['Valor'].sum()
    lucro_liquido = total_receitas - total_despesas

    return total_receitas, total_despesas, lucro_liquido, receitas, despesas

# Função para gerar o gráfico
def gerar_grafico(receitas, despesas):
    # Gráfico de pizza
    labels = ['Receitas', 'Despesas']
    sizes = [receitas['Valor'].sum(), despesas['Valor'].sum()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('grafico.png')  # Salva o gráfico

# Função para gerar o relatório PDF
def gerar_relatorio_pdf(total_receitas, total_despesas, lucro_liquido, receitas, despesas):
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Relatório Financeiro", ln=True, align='C')

    # Relatório de Totais
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f"Total de Receitas: R${total_receitas:.2f}", ln=True)
    pdf.cell(200, 10, f"Total de Despesas: R${total_despesas:.2f}", ln=True)
    pdf.cell(200, 10, f"Lucro Líquido: R${lucro_liquido:.2f}", ln=True)

    # Gerar gráfico
    pdf.ln(10)
    pdf.image('grafico.png', x=10, y=pdf.get_y(), w=100)

    # Salvar o PDF
    pdf.output('relatorio_financeiro.pdf')

# Função principal
def main():
    caminho_arquivo = 'data/planilha_financeira.csv'  # Caminho da planilha
    total_receitas, total_despesas, lucro_liquido, receitas, despesas = processar_planilha(caminho_arquivo)
    gerar_grafico(receitas, despesas)
    gerar_relatorio_pdf(total_receitas, total_despesas, lucro_liquido, receitas, despesas)
    print("Relatório gerado com sucesso!")

if __name__ == '__main__':
    main()
