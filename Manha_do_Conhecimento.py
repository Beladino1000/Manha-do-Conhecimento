from flask import Flask, render_template, request, session, redirect
import string
import random as r
from flask import Flask

app = Flask(__name__)
app.secret_key = 'Pedro Couto'

@app.route('/')
def home():
    return render_template('Sobre.html')

@app.route('/conversorcpf',methods=['GET','POST'])
def conversorcpf():
    resposta=""
    if request.method=='POST':
        entrada=request.form['texto_usuario']
        try:
            p=float(entrada.lower().replace('°','').replace(' ','').replace('c','').replace('º','').replace(',','.').replace('graus',''))
            resposta=f'{p} graus Celcius equivalem a {(9/5*p+32)} graus Fahrenheit'
        except ValueError:
            resposta='Entrada inválida, Digite novamente.'
    return render_template('Conversor CpF.html', resposta=resposta)

@app.route('/conversorfpc',methods=['GET','POST'])
def conversorfpc():
    resposta=""
    if request.method=='POST':
        entrada=request.form['texto_usuario']
        try:
            p=float(entrada.lower().replace('°','').replace(' ','').replace('f','').replace('º','').replace(',','.').replace('graus',''))
            resposta=f'{p} graus Fahrenheit equivalem a {((p - 32) * 5/9)} graus Celcius'
        except ValueError:
            resposta='Entrada inválida, Digite novamente.'
    return render_template('Conversor FpC.html', resposta=resposta)

@app.route('/palindromo', methods=['GET','POST'])
def palindromo():
    resposta = ""
    if request.method == 'POST':
        entrada = request.form['texto_usuario']
        p=list(entrada.replace(' ','').lower())
        r=0
        for n in range(0,len(p)):
            if not p[n-1]==p[-n]:
                r=1
            if r==1:
                resposta=f'{entrada} não é um palíndromo'
            else:
                resposta=f'{entrada} é um palíndromo'
    return render_template('Palíndromo.html', resposta=resposta)

@app.route('/contador',methods=['GET','POST'])
def contador():
    if 'valor' not in session:
        session['valor']=0
    if request.method=='POST':
        if 'add1' in request.form:
            session['valor']+=1
        elif 'subtract1' in request.form:
            session['valor']+=-1
        elif 'reset' in request.form:
            session['valor']=0
        elif 'addvp' in request.form:
            try:
                valor_digitado=int(request.form["vp"])
                session['valor']+=valor_digitado
            except ValueError:
                pass
        elif 'subtractvp' in request.form:
            try:
                valor_digitado=int(request.form["vp"])*(-1)
                session['valor']+=valor_digitado
            except ValueError:
                pass
    return render_template('Contador.html',valor=session['valor'])

@app.route('/fatorial',methods=['GET','POST'])
def calculadora_fatorial():
    fatorial=''
    if request.method=='POST':
        if 'calc' in request.form:
            try:
                fatoriando=int(request.form['fatoriando'])
                if fatoriando>-0.0001:
                    fatorial=1
                    fatorial_lista=[]
                    for n in range(1,fatoriando+1):
                        fatorial_lista.append(n)
                    for n in fatorial_lista:
                        fatorial=fatorial*n
                    fatorial=f' O fatorial de {fatoriando} é {fatorial}'
                else:
                    fatorial='Valor inválido! Digite outro valor.'
            except ValueError:
                fatorial='Valor inválido! Digite outro valor.'
    return render_template('Calculadora de fatorial.html',fatorial=fatorial)

@app.route('/validarsenha', methods=['GET','POST'])
def validador_senha():
    resposta='' 
    resposta2=''
    npont=False
    nnum=False
    nup=False
    nlow=False
    if 'verify' in request.form:
        session['Input']=str(request.form['senha'])
        if not any(elem in string.punctuation for elem in list(session['Input'])):
            npont=True
        if not any(elem in string.digits for elem in list(session['Input'])):
            nnum=True
        if not any(elem in string.ascii_lowercase for elem in list(session['Input'])):
            nlow=True
        if not any(elem in string.ascii_uppercase for elem in list(session['Input'])):
            nup=True
        if not (npont or nnum or nup or nlow):
            resposta='Senha válida'
        else:
            resposta='Senha inválida'
            if npont:
                resposta+=', ela necessita de algum caractere especial'
            if nnum:
                resposta+=', ela necessita de algum numeral'
            if nup:
                resposta+=', ela necessita de alguma letra maiúscula'
            if nlow:
                resposta+=', ela necessita de alguma letra minúscula'
            resposta+='.'
    if 'define' in request.form:
        if request.form['csenha']==session['Input']:
            resposta='Senha válida'
            resposta2='Senha definida'
            session['Senha']=session['Input']
        else:
            resposta='Senha válida'
            resposta2='Confirmação incorreta, tente novamente'
    return render_template('Validador de senha.html',resposta=resposta, resposta2=resposta2)

@app.route('/paginabloqueada', methods=['POST','GET'])
def bloqueador_da_página():
    resposta=''
    if request.method == 'POST' and 'confirm' in request.form:
        if request.form['dsenha']==session['Senha']:
            return redirect('/paginadesbloqueada')
        else:
            resposta='Senha incorreta. Tente novamente.'
    return render_template('Página bloqueada por senha.html', resposta=resposta)

@app.route('/paginadesbloqueada',)
def página_desbloqueada():
    return render_template('Página desbloqueada por senha.html')

@app.route('/adivinhação', methods=['GET', 'POST'])
def jogo_de_adivinhação():

    # Inicializações
    if 'valor' not in session:
        session['valor'] = r.randint(1, 50)
    if 'tentativas' not in session:
        session['tentativas'] = 5
    if 'jogos' not in session:
        session['jogos'] = 1
    if 'vitórias' not in session:
        session['vitórias'] = 0
    if 'rodando' not in session:
        session['rodando'] = True

    resposta = ''
    continuar = ''

    if session['rodando']:
        if request.method == 'POST' and 'adivinhar' in request.form:
            try:
                palpite = int(request.form['Input'])
                valor = session['valor']

                if palpite == valor:
                    resposta = f'🎉 Ganhou! A resposta realmente era {valor}!'
                    session['vitórias'] += 1
                    session['rodando'] = False
                    continuar = 'Jogar novamente'
                else:
                    session['tentativas'] -= 1
                    dica = 'maior' if valor > palpite else 'menor'
                    if session['tentativas'] == 0:
                        resposta = f'❌ Perdeu! A resposta era {valor}.'
                        session['rodando'] = False
                        continuar = 'Jogar novamente'
                    else:
                        resposta = f'Errou! O número é {dica} que {palpite}. Tente novamente!'
            except ValueError:
                resposta = 'Entrada inválida! Digite um número entre 1 e 50.'

    elif request.method == 'POST':
        if 'continuar' in request.form:
            session['jogos'] += 1
            session['tentativas'] = 5
            session['valor'] = r.randint(1, 50)
            session['rodando'] = True
            resposta = ''
            continuar = ''
    
        elif 'reset' in request.form:
            session['jogos'] = 1
            session['vitórias'] = 0
            session['tentativas'] = 5
            session['valor'] = r.randint(1, 50)
            session['rodando'] = True
            resposta = ''
            continuar = ''

    elif not session['rodando']:
        continuar = 'Jogar novamente'

    return render_template(
        'Jogo de adivinhação.html',
        resposta=resposta,
        tentativas=session['tentativas'],
        jogos=session['jogos'],
        vitórias=session['vitórias'],
        continuar=continuar
    )
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)