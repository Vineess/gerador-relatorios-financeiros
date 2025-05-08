import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from fpdf import FPDF

def processar_planilha(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    receitas = df[df['Tipo'] == 'Receita']
    despesas = df[df['Tipo'] == 'Despesa']
    total_receitas = receitas['Valor'].sum()
    total_despesas = despesas['Valor'].sum()
    lucro_liquido = total_receitas - total_despesas
    return total_receitas, total_despesas, lucro_liquido, receitas, despesas

def gerar_grafico(receitas, despesas, caminho_saida, nome_base):
    labels = ['Receitas', 'Despesas']
    sizes = [receitas['Valor'].sum(), despesas['Valor'].sum()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    caminho_imagem = os.path.join(caminho_saida, f'{nome_base}_grafico.png')
    plt.savefig(caminho_imagem)
    plt.close()
    return caminho_imagem

def gerar_relatorio_pdf(total_receitas, total_despesas, lucro_liquido, caminho_saida, caminho_grafico, nome_base):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Relatório Financeiro", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f"Total de Receitas: R${total_receitas:.2f}", ln=True)
    pdf.cell(200, 10, f"Total de Despesas: R${total_despesas:.2f}", ln=True)
    pdf.cell(200, 10, f"Lucro Líquido: R${lucro_liquido:.2f}", ln=True)

    pdf.ln(10)
    pdf.image(caminho_grafico, x=10, y=pdf.get_y(), w=100)

    caminho_pdf = os.path.join(caminho_saida, f'{nome_base}_relatorio.pdf')
    pdf.output(caminho_pdf)
    return caminho_pdf

def main():
    caminho_arquivo = 'data/planilha_financeira.csv'

    data_hoje = datetime.now().strftime('%Y-%m-%d')
    hora_agora = datetime.now().strftime('%H-%M-%S')
    nome_base = f'relatorio_{hora_agora}'

    pasta_saida = os.path.join('relatorios', data_hoje)
    os.makedirs(pasta_saida, exist_ok=True)

    total_receitas, total_despesas, lucro_liquido, receitas, despesas = processar_planilha(caminho_arquivo)
    caminho_grafico = gerar_grafico(receitas, despesas, pasta_saida, nome_base)
    caminho_pdf = gerar_relatorio_pdf(total_receitas, total_despesas, lucro_liquido, pasta_saida, caminho_grafico, nome_base)

    print(f"Relatório gerado com sucesso em: {caminho_pdf}")

if __name__ == '__main__':
    main()
