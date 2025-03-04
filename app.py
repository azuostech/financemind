from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import json
import os

app = Flask(__name__)

# Carregar os dados da tabela do JSON
with open("dados.json", "r", encoding="utf-8") as file:
    DADOS_TABELA = json.load(file)

@app.route('/')
#def index():
#    return render_template("index.html")
def home():
    return render_template("index.html")
    #return "Deploy com Fly.io!"




@app.route('/process', methods=['POST'])
def process():
    respostas = request.form.to_dict()
    
    # Determinar o perfil emocional predominante
    perfil = analisar_respostas(respostas)
    
    # Pegar os dados correspondentes do JSON
    dados_perfil = DADOS_TABELA.get(perfil, {})
    
    # Gerar relatório em PDF
    pdf_path = gerar_relatorio(respostas, perfil, dados_perfil)
    
    return send_file(pdf_path, as_attachment=True)

def analisar_respostas(respostas):
    """Analisa as respostas e determina o perfil emocional predominante."""
    perfis = {
        "Rejeição": 0,
        "Abandono": 0,
        "Humilhação": 0,
        "Traição": 0,
        "Injustiça": 0
    }
    
    for chave, resposta in respostas.items():
        if "rejeicao" in chave:
            perfis["Rejeição"] += int(resposta)
        elif "abandono" in chave:
            perfis["Abandono"] += int(resposta)
        elif "humilhacao" in chave:
            perfis["Humilhação"] += int(resposta)
        elif "traicao" in chave:
            perfis["Traição"] += int(resposta)
        elif "injustica" in chave:
            perfis["Injustiça"] += int(resposta)
    
    # Determinar qual ferida emocional tem a maior pontuação
    perfil_dominante = max(perfis, key=perfis.get)
    return perfil_dominante

def gerar_relatorio(respostas, perfil, dados_perfil):
    """Gera um relatório em PDF com base no perfil identificado."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "Relatório de Perfil Financeiro Emocional", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Perfil predominante: {perfil}", ln=True, align='L')
    pdf.ln(10)
    
    # Adicionar dados do perfil ao PDF
    for chave, valor in dados_perfil.items():
        pdf.multi_cell(0, 10, f"{chave}: {valor}")
        pdf.ln(3)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Respostas do questionário:", ln=True, align='L')
    pdf.ln(5)
    
    for pergunta, resposta in respostas.items():
        pdf.multi_cell(0, 10, f"{pergunta}: {resposta}")
        pdf.ln(3)
    
    pdf_path = "relatorio.pdf"
    pdf.output(pdf_path)
    return pdf_path

#if __name__ == '__main__':
 #   app.run(debug=True)

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=8080)
