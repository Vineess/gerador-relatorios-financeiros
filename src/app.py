import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt

# Caminho para a pasta 'data', que está uma pasta acima de 'src'
caminho_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# Garantir que a pasta 'data' exista
os.makedirs(caminho_data, exist_ok=True)

# Caminho completo para a planilha
caminho_planilha = os.path.join(caminho_data, 'planilha_financeira.csv')

# Verificar se o arquivo CSV já existe, se não criar
if not os.path.exists(caminho_planilha):
    colunas = ['Descrição', 'Valor', 'Tipo de Pagamento', 'Tipo', 'Data']
    modelo_df = pd.DataFrame(columns=colunas)
    modelo_df.to_csv(caminho_planilha, index=False)
    print(f"Planilha criada: {caminho_planilha}")
else:
    print(f"Planilha já existe: {caminho_planilha}")

# Função para processar a planilha
def processar_planilha(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    receitas = df[df['Tipo'] == 'Receita']
    despesas = df[df['Tipo'] == 'Despesa']
    total_receitas = receitas['Valor'].sum()
    total_despesas = despesas['Valor'].sum()
    lucro_liquido = total_receitas - total_despesas
    return total_receitas, total_despesas, lucro_liquido, receitas, despesas

# Função para gerar o gráfico
def gerar_grafico(receitas, despesas, caminho_saida, nome_base):
    labels = ['Receitas', 'Despesas']
    sizes = [receitas['Valor'].sum(), despesas['Valor'].sum()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    caminho_imagem = os.path.join(caminho_saida, f'{nome_base}_grafico.png')
    plt.savefig(caminho_imagem)
    plt.close()
    return caminho_imagem

# Função para gerar o relatório PDF
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

# Função para salvar dados da planilha
def salvar_dados(descricao, valor, tipo_pagamento, tipo, data):
    df = pd.read_csv(caminho_planilha)
    novo_registro = {'Descrição': descricao, 'Valor': valor, 'Tipo de Pagamento': tipo_pagamento, 'Tipo': tipo, 'Data': data}
    df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
    df.to_csv(caminho_planilha, index=False)
    print(f"Dados salvos: {novo_registro}")


# Função para gerar o relatório
def gerar_relatorio():
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    hora_agora = datetime.now().strftime('%H-%M-%S')
    nome_base = f'relatorio_{hora_agora}'

    # Caminho para a pasta de relatórios, uma pasta acima de 'src'
    pasta_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'relatorios', data_hoje)
    os.makedirs(pasta_saida, exist_ok=True)

    total_receitas, total_despesas, lucro_liquido, receitas, despesas = processar_planilha(caminho_planilha)
    caminho_grafico = gerar_grafico(receitas, despesas, pasta_saida, nome_base)
    caminho_pdf = gerar_relatorio_pdf(total_receitas, total_despesas, lucro_liquido, pasta_saida, caminho_grafico, nome_base)

    print(f"Relatório gerado com sucesso em: {caminho_pdf}")
    messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso!\n\n{caminho_pdf}")


# Interface gráfica com Tkinter
def abrir_interface():
    root = tk.Tk()
    root.title("Gerador de Relatórios Financeiros")

    # Campos de entrada
    tk.Label(root, text="Descrição").grid(row=0, column=0)
    descricao_entry = tk.Entry(root)
    descricao_entry.grid(row=0, column=1)

    tk.Label(root, text="Valor").grid(row=1, column=0)
    valor_entry = tk.Entry(root)
    valor_entry.grid(row=1, column=1)

    tk.Label(root, text="Tipo de Pagamento").grid(row=2, column=0)
    tipo_pagamento_entry = tk.Entry(root)
    tipo_pagamento_entry.grid(row=2, column=1)

    tk.Label(root, text="Tipo (Receita/Despesa)").grid(row=3, column=0)
    tipo_entry = tk.Entry(root)
    tipo_entry.grid(row=3, column=1)

    tk.Label(root, text="Data (YYYY-MM-DD)").grid(row=4, column=0)
    data_entry = tk.Entry(root)
    data_entry.grid(row=4, column=1)

    # Função de salvar e limpar os campos
    def on_salvar():
        descricao = descricao_entry.get()
        valor = float(valor_entry.get())
        tipo_pagamento = tipo_pagamento_entry.get()
        tipo = tipo_entry.get()
        data = data_entry.get()
        
        if descricao and valor and tipo_pagamento and tipo and data:
            salvar_dados(descricao, valor, tipo_pagamento, tipo, data)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            
            # Limpar os campos após salvar
            descricao_entry.delete(0, tk.END)
            valor_entry.delete(0, tk.END)
            tipo_pagamento_entry.delete(0, tk.END)
            tipo_entry.delete(0, tk.END)
            data_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")

    # Função de gerar relatório
    def on_gerar_relatorio():
        gerar_relatorio()

    # Botões
    tk.Button(root, text="Salvar", command=on_salvar).grid(row=5, column=0)
    tk.Button(root, text="Gerar Relatório", command=on_gerar_relatorio).grid(row=5, column=1)

    # Iniciar a interface gráfica
    root.mainloop()

# Iniciar a interface
if __name__ == "__main__":
    abrir_interface()
