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
    import pandas as pd
    df = pd.read_csv(caminho_planilha)
    novo_dado = pd.DataFrame([[descricao, valor, tipo_pagamento, tipo, data]], columns=df.columns)
    df = pd.concat([df, novo_dado], ignore_index=True)
    df.to_csv(caminho_planilha, index=False)
    messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

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

    # Tamanho fixo para a janela
    root.geometry('500x500')  # Definindo o tamanho inicial da janela (largura x altura)
    root.minsize(500, 500)  # Tamanho mínimo da janela
    root.maxsize(500, 500)  # Tamanho máximo da janela
    root.resizable(False, False)  # Impedindo o redimensionamento da janela

    # Cores e tema
    root.config(bg="#f0f0f0")  # Cor de fundo suave
    cor_botao = "#4CAF50"  # Cor do botão de salvar
    cor_botao_hover = "#45a049"  # Cor do botão quando em hover
    cor_botao_gerar = "#2196F3"  # Cor do botão para gerar relatório
    cor_botao_gerar_hover = "#1976D2"  # Cor do botão de gerar relatório quando em hover

    # Estilo de fontes
    fonte_titulo = ("Arial", 14, "bold")
    fonte_label = ("Arial", 12)
    fonte_botao = ("Arial", 12, "bold")

    # Label para mostrar o nome da tabela
    tabela_label = tk.Label(root, text="Tabela: planilha_financeira", font=fonte_titulo, bg="#f0f0f0")
    tabela_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Descrição
    tk.Label(root, text="Descrição", font=fonte_label, bg="#f0f0f0").grid(row=1, column=0, pady=5, padx=10, sticky="w")
    descricao_entry = tk.Entry(root, font=fonte_label, width=30)
    descricao_entry.grid(row=1, column=1, pady=5)

    # Valor
    tk.Label(root, text="Valor", font=fonte_label, bg="#f0f0f0").grid(row=2, column=0, pady=5, padx=10, sticky="w")
    valor_entry = tk.Entry(root, font=fonte_label, width=30)
    valor_entry.grid(row=2, column=1, pady=5)

    # Tipo de Pagamento (usando OptionMenu)
    tk.Label(root, text="Tipo de Pagamento", font=fonte_label, bg="#f0f0f0").grid(row=3, column=0, pady=5, padx=10, sticky="w")
    tipo_pagamento_var = tk.StringVar()
    tipo_pagamento_var.set("Dinheiro")  # Valor padrão
    tipo_pagamento_menu = tk.OptionMenu(root, tipo_pagamento_var, "Dinheiro", "Pix", "Boleto", "Cartão")
    tipo_pagamento_menu.grid(row=3, column=1, pady=5)

    # Tipo (Receita/Despesa)
    tk.Label(root, text="Tipo (Receita/Despesa)", font=fonte_label, bg="#f0f0f0").grid(row=4, column=0, pady=5, padx=10, sticky="w")
    tipo_var = tk.StringVar()
    tipo_var.set("Receita")  # Valor padrão
    tipo_menu = tk.OptionMenu(root, tipo_var, "Receita", "Despesa")
    tipo_menu.grid(row=4, column=1, pady=5)

    # Data (no formato DD-MM-YYYY)
    tk.Label(root, text="Data (DD-MM-YYYY)", font=fonte_label, bg="#f0f0f0").grid(row=5, column=0, pady=5, padx=10, sticky="w")
    data_entry = tk.Entry(root, font=fonte_label, width=30)
    data_entry.grid(row=5, column=1, pady=5)

    # Função de salvar dados
    def on_salvar():
        descricao = descricao_entry.get()
        valor = float(valor_entry.get())
        tipo_pagamento = tipo_pagamento_var.get()
        tipo = tipo_var.get()
        data = data_entry.get()
        salvar_dados(descricao, valor, tipo_pagamento, tipo, data)

    # Botão de salvar
    salvar_button = tk.Button(root, text="Salvar", font=fonte_botao, bg=cor_botao, activebackground=cor_botao_hover, command=on_salvar)
    salvar_button.grid(row=6, column=0, padx=10, pady=20)

    # Botão para gerar relatório
    gerar_button = tk.Button(root, text="Gerar Relatório", font=fonte_botao, bg=cor_botao_gerar, activebackground=cor_botao_gerar_hover, command=gerar_relatorio)
    gerar_button.grid(row=6, column=1, padx=10, pady=20)

    root.mainloop()

# Abrir a interface gráfica
abrir_interface()
