from flask import Flask, request, redirect, render_template
import psycopg2

app = Flask(__name__)


# CONEXÃO SUPABASE

def conectar():
    conn = psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        database="postgres",
        user="postgres.mgcbcossxhdyzlyfbgkp",
        password="260923@Pesquisa",
        port="6543",
        sslmode="require"
    )
    return conn



# CRIAR TABELA

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS respostas (
        id SERIAL PRIMARY KEY,
        idade TEXT,
        trabalha TEXT,
        cor_raca TEXT,
        acesso TEXT,
        internet TEXT,
        tecnologia TEXT,
        curso TEXT,
        aprender TEXT,
        acessivel TEXT,
        melhorar TEXT,
        realidade TEXT,
        pessoas TEXT,
        social TEXT,
        sofreu TEXT,
        comentario TEXT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()



# PAGINA INICIAL

@app.route("/")
def index():
    sucesso = request.args.get("sucesso")
    return render_template("index.html", sucesso=sucesso)



# RECEBER FORMULÁRIO

@app.route("/enviar", methods=["POST"])
def enviar():

    idade = request.form.get("Pergunta1", "")
    trabalha = request.form.get("trabalha", "")
    cor_raca = request.form.get("cor_raca", "")
    acesso = request.form.get("acesso", "")
    internet = request.form.get("Internet", "")
    tecnologia = request.form.get("tecnologia", "")
    curso = request.form.get("curso", "")
    aprender = request.form.get("aprender", "")
    acessivel = request.form.get("acessivel", "")
    melhorar = request.form.get("melhorar", "")
    realidade = request.form.get("realidade", "")
    pessoas = request.form.get("pessoas", "")
    social = request.form.get("social", "")
    sofreu = request.form.get("sofreu", "")
    comentario = request.form.get("comentario", "")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO respostas (
        idade, trabalha, cor_raca, acesso, internet,
        tecnologia, curso, aprender, acessivel,
        melhorar, realidade, pessoas, social,
        sofreu, comentario
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        idade, trabalha, cor_raca, acesso, internet,
        tecnologia, curso, aprender, acessivel,
        melhorar, realidade, pessoas, social,
        sofreu, comentario
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/?sucesso=1")



# RESPOSTAS

@app.route("/respostas")
def respostas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM respostas ORDER BY id DESC")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("respostas.html", dados=dados)



# ANALISE

@app.route("/analise")
def analise():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM respostas")
    total = cursor.fetchone()[0]

    if total == 0:
        total = 1

    def contar(coluna):
        cursor.execute(f"SELECT COUNT(*) FROM respostas WHERE {coluna}='Sim'")
        sim = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM respostas WHERE {coluna}='Não'")
        nao = cursor.fetchone()[0]

        return sim, nao

    trabalha_sim, trabalha_nao = contar("trabalha")
    tecnologia_sim, tecnologia_nao = contar("tecnologia")
    acesso_sim, acesso_nao = contar("acesso")
    internet_sim, internet_nao = contar("internet")
    curso_sim, curso_nao = contar("curso")
    acessivel_sim, acessivel_nao = contar("acessivel")
    melhorar_sim, melhorar_nao = contar("melhorar")
    realidade_sim, realidade_nao = contar("realidade")
    oportunidade_sim, oportunidade_nao = contar("pessoas")
    dificuldade_sim, dificuldade_nao = contar("social")
    preconceito_sim, preconceito_nao = contar("sofreu")

    # IDADES
    cursor.execute("SELECT idade FROM respostas")
    idades = cursor.fetchall()

    menor = jovem = adulto = idoso = 0

    for item in idades:
        try:
            idade = int(item[0])

            if idade <= 17:
                menor += 1
            elif idade <= 30:
                jovem += 1
            elif idade <= 59:
                adulto += 1
            else:
                idoso += 1
        except:
            pass

    idade_menor = round((menor / total) * 100)
    idade_jovem = round((jovem / total) * 100)
    idade_adulto = round((adulto / total) * 100)
    idade_idoso = round((idoso / total) * 100)

    # COR / RAÇA
    def porcentagem_cor(nome):
        cursor.execute(
            "SELECT COUNT(*) FROM respostas WHERE cor_raca=%s",
            (nome,)
        )
        qtd = cursor.fetchone()[0]
        return round((qtd / total) * 100)

    branca = porcentagem_cor("Branca")
    negra = porcentagem_cor("Negra")
    parda = porcentagem_cor("Parda")
    amarela = porcentagem_cor("Amarela")
    indigena = porcentagem_cor("Indígena")

    cursor.close()
    conn.close()

    return render_template(
        "analise.html",

        trabalha_sim=trabalha_sim,
        trabalha_nao=trabalha_nao,

        tecnologia_sim=tecnologia_sim,
        tecnologia_nao=tecnologia_nao,

        acesso_sim=acesso_sim,
        acesso_nao=acesso_nao,

        internet_sim=internet_sim,
        internet_nao=internet_nao,

        curso_sim=curso_sim,
        curso_nao=curso_nao,

        acessivel_sim=acessivel_sim,
        acessivel_nao=acessivel_nao,

        melhorar_sim=melhorar_sim,
        melhorar_nao=melhorar_nao,

        realidade_sim=realidade_sim,
        realidade_nao=realidade_nao,

        oportunidade_sim=oportunidade_sim,
        oportunidade_nao=oportunidade_nao,

        dificuldade_sim=dificuldade_sim,
        dificuldade_nao=dificuldade_nao,

        preconceito_sim=preconceito_sim,
        preconceito_nao=preconceito_nao,

        idade_menor=idade_menor,
        idade_jovem=idade_jovem,
        idade_adulto=idade_adulto,
        idade_idoso=idade_idoso,

        branca=branca,
        negra=negra,
        parda=parda,
        amarela=amarela,
        indigena=indigena
    )



# INICIAR

if __name__ == "__main__":
    criar_banco()
    app.run(host="0.0.0.0", port=5000, debug=True)
