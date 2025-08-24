from flask import Flask, render_template, request, session, redirect
from datetime import timedelta
import string
import random as r
import sympy as sp
import os
app = Flask(__name__)
app.secret_key = 'Pedro Couto'
app.permanent_session_lifetime = timedelta(days=1)

pontuação = r"!@#$%¨&*()_=+§²¹³£¢¬[{]}ªº´`^~;:>,</?\|° "
acentuadas = "áàãâäÁÀÃÂÄéèêëÉÈÊËíìîïÍÌÎÏóòõôöÓÒÕÔÖúùûüÚÙÛÜçÇ"
sem_acento = "aaaaaAAAAAeeeeEEEEiiiiIIIIoooooOOOOOuuuuUUUUcC"

def replace_letras(b: str)->str:
    tabela=str.maketrans('','',string.ascii_letters)
    return b.translate(tabela)

def replace_master(texto: str)->str:
    tabela1=str.maketrans(acentuadas, sem_acento)
    tabela2=str.maketrans('','',pontuação)
    return texto.translate(tabela1).translate(tabela2)

@app.route('/')
def home():
    return render_template('Sobre.html')

@app.route('/conversor-c-f',methods=['GET','POST'])
def conversorcpf():
    resposta1=""
    resposta2=""
    if request.method=='POST':
        if 'convertercpf' in request.form:
            entrada=request.form['texto_usuario']
            try:
                p=float(replace_letras(replace_master(entrada.lower().replace(',','.'))))
                resposta1=f'{p} graus Celcius equivalem a {(9/5*p+32)} graus Fahrenheit'
            except ValueError:
                resposta1='Entrada inválida, Digite novamente.'
        if 'converterfpc' in request.form:
            entrada=request.form['texto_usuario2']
            try:
                p=float(replace_letras(replace_master(entrada.lower().replace(',','.'))))
                resposta2=f'{p} graus Fahrenheit equivalem a {((p - 32) * 5/9)} graus Celcius'
            except ValueError:
                resposta2='Entrada inválida, Digite novamente.'
    return render_template('Conversor CpF.html', resposta1=resposta1, resposta2=resposta2)

@app.route('/palindromo', methods=['GET','POST'])
def palindromo():
    resposta = ""
    if request.method == 'POST':
        entrada = request.form['texto_usuario']
        p=list(replace_master(entrada.lower()))
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
    return render_template('Contador.html')

@app.route('/fatorial', methods=['GET', 'POST'])
def calculadora_fatorial():
    fatorial = ''
    erro = 'Valor inválido! Digite outro valor.'
    
    if request.method == 'POST' and 'calc' in request.form:
        try:
            entrada = replace_master(request.form['fatoriando'].replace(',', '.'))
            fatoriando = float(entrada)
            
            if fatoriando < 0:
                fatorial = erro
            elif fatoriando > 100000:
                fatorial = f'{fatoriando} é grande demais para calcular'
            else:
                resultado = sp.factorial(fatoriando)
                
                if abs(resultado - round(resultado)) < 1e-10:
                    resultado = int(round(resultado))
                    fatorial = f'O fatorial de {fatoriando} é {resultado}'.replace('.',',')
                else:
                    fatorial = f'O fatorial de {fatoriando} é {resultado:.15g}'.replace(".", ",")
        except ValueError:
            fatorial = erro
    
    return render_template('Calculadora de fatorial.html', fatorial=fatorial)

@app.route('/validarsenha', methods=['GET','POST'])
def validador_senha():
    if 'mostrar' not in session:
        session['mostrar'] = False  # Mudando para booleano para melhor controle
    
    resposta = '' 
    resposta2 = ''
    npont = False
    nnum = False
    nup = False
    nlow = False
    
    if 'verify' in request.form:
        session['Input'] = str(request.form['senha'])
        if not any(elem in string.punctuation for elem in list(session['Input'])):
            npont = True
        if not any(elem in string.digits for elem in list(session['Input'])):
            nnum = True
        if not any(elem in string.ascii_lowercase for elem in list(session['Input'])):
            nlow = True
        if not any(elem in string.ascii_uppercase for elem in list(session['Input'])):
            nup = True
            
        if not (npont or nnum or nup or nlow):
            resposta = 'Senha válida'
            session['mostrar'] = True  # Mostrar campo de confirmação
        else:
            resposta = 'Senha inválida'
            if npont:
                resposta += ', ela necessita de algum caractere especial'
            if nnum:
                resposta += ', ela necessita de algum numeral'
            if nup:
                resposta += ', ela necessita de alguma letra maiúscula'
            if nlow:
                resposta += ', ela necessita de alguma letra minúscula'
            resposta += '.'
            session['mostrar'] = False  # Não mostrar campo de confirmação
    
    if 'define' in request.form:
        if request.form['csenha'] == session['Input']:
            resposta = 'Senha válida'
            resposta2 = 'Senha definida'
            session['Senha'] = session['Input']
            session['mostrar'] = True  # Esconder após definir
        else:
            resposta = 'Senha válida'
            resposta2 = 'Confirmação incorreta, tente novamente'
            session['mostrar'] = True  # Manter visível para nova tentativa
    
    return render_template('Validador de senha.html', mostrar=session['mostrar'], resposta=resposta, resposta2=resposta2)

@app.route('/paginabloqueada', methods=['POST','GET'])
def bloqueador_da_página():
    resposta=''
    if 'Senha' not in session:
        session['Senha']='Xx_Abraham-Lincoln_xXD'
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

    if 'valor' not in session or not (1 <= session['valor'] <= 50):
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

@app.route('/resetar',methods=['GET','POST'])
def sair():
    session.clear()
    return redirect('/')

@app.route('/trivia', methods=['GET','POST'])
def trivia():
    if 'aba' not in session:
        session['aba'] = 'Trivia-master/Trivia.html'
    if 'pontuação' not in session:
        session['pontuação']=0
        
    if 'certo200' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+200
    if 'certo400' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+400
    if 'certo600' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+600
    if 'certo800' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+800
    if 'certo1000' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+1000

    if 'errado200' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-100
    if 'errado400' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-200
    if 'errado600' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-300
    if 'errado800' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-400
    if 'errado1000' in request.form:
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-500
        
    if 'cat' not in session:
        session['cat']=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ]

    if 'cat1-200' in request.form and not session['cat'][0]=='Press':
        session['aba'] = 'Trivia-master/cat1-200.html'
        session['cat'][0]='Press'
    if 'cat1-400' in request.form and not session['cat'][1]=='Press':
        session['aba'] = 'Trivia-master/cat1-400.html'
        session['cat'][1]='Press'
    if 'cat1-600' in request.form and not session['cat'][2]=='Press':
        session['aba'] = 'Trivia-master/cat1-600.html'
        session['cat'][2]='Press'
    if 'cat1-800' in request.form and not session['cat'][3]=='Press':
        session['aba'] = 'Trivia-master/cat1-800.html'
        session['cat'][3]='Press'
    if 'cat1-1000' in request.form and not session['cat'][4]=='Press':
        session['aba'] = 'Trivia-master/cat1-1000.html'
        session['cat'][4]='Press'

    if 'cat2-200' in request.form and not session['cat'][5]=='Press':
        session['aba'] = 'Trivia-master/cat2-200.html'
        session['cat'][5]='Press'
    if 'cat2-400' in request.form and not session['cat'][6]=='Press':
        session['aba'] = 'Trivia-master/cat2-400.html'
        session['cat'][6]='Press'
    if 'cat2-600' in request.form and not session['cat'][7]=='Press':
        session['aba'] = 'Trivia-master/cat2-600.html'
        session['cat'][7]='Press'
    if 'cat2-800' in request.form and not session['cat'][8]=='Press':
        session['aba'] = 'Trivia-master/cat2-800.html'
        session['cat'][8]='Press'
    if 'cat2-1000' in request.form and not session['cat'][9]=='Press':
        session['aba'] = 'Trivia-master/cat2-1000.html'
        session['cat'][9]='Press'

    if 'cat3-200' in request.form and not session['cat'][10]=='Press':
        session['aba'] = 'Trivia-master/cat3-200.html'
        session['cat'][10]='Press'
    if 'cat3-400' in request.form and not session['cat'][11]=='Press':
        session['aba'] = 'Trivia-master/cat3-400.html'
        session['cat'][11]='Press'
    if 'cat3-600' in request.form and not session['cat'][12]=='Press':
        session['aba'] = 'Trivia-master/cat3-600.html'
        session['cat'][12]='Press'
    if 'cat3-800' in request.form and not session['cat'][13]=='Press':
        session['aba'] = 'Trivia-master/cat3-800.html'
        session['cat'][13]='Press'
    if 'cat3-1000' in request.form and not session['cat'][14]=='Press':
        session['aba'] = 'Trivia-master/cat3-1000.html'
        session['cat'][14]='Press'

    if 'cat4-200' in request.form and not session['cat'][15]=='Press':
        session['aba'] = 'Trivia-master/cat4-200.html'
        session['cat'][15]='Press'
    if 'cat4-400' in request.form and not session['cat'][16]=='Press':
        session['aba'] = 'Trivia-master/cat4-400.html'
        session['cat'][16]='Press'
    if 'cat4-600' in request.form and not session['cat'][17]=='Press':
        session['aba'] = 'Trivia-master/cat4-600.html'
        session['cat'][17]='Press'
    if 'cat4-800' in request.form and not session['cat'][18]=='Press':
        session['aba'] = 'Trivia-master/cat4-800.html'
        session['cat'][18]='Press'
    if 'cat4-1000' in request.form and not session['cat'][19]=='Press':
        session['aba'] = 'Trivia-master/cat4-1000.html'
        session['cat'][19]='Press'

    if 'cat5-200' in request.form and not session['cat'][20]=='Press':
        session['aba'] = 'Trivia-master/cat5-200.html'
        session['cat'][20]='Press'
    if 'cat5-400' in request.form and not session['cat'][21]=='Press':
        session['aba'] = 'Trivia-master/cat5-400.html'
        session['cat'][21]='Press'
    if 'cat5-600' in request.form and not session['cat'][22]=='Press':
        session['aba'] = 'Trivia-master/cat5-600.html'
        session['cat'][22]='Press'
    if 'cat5-800' in request.form and not session['cat'][23]=='Press':
        session['aba'] = 'Trivia-master/cat5-800.html'
        session['cat'][23]='Press'
    if 'cat5-1000' in request.form and not session['cat'][24]=='Press':
        session['aba'] = 'Trivia-master/cat5-1000.html'
        session['cat'][24]='Press'

    return render_template(session['aba'],
                           pontuação=session['pontuação'],
                           cat1_200=session['cat'][0],
                           cat1_400=session['cat'][1],
                           cat1_600=session['cat'][2],
                           cat1_800=session['cat'][3],
                           cat1_1000=session['cat'][4],
                           cat2_200=session['cat'][5],
                           cat2_400=session['cat'][6],
                           cat2_600=session['cat'][7],
                           cat2_800=session['cat'][8],
                           cat2_1000=session['cat'][9],
                           cat3_200=session['cat'][10],
                           cat3_400=session['cat'][11],
                           cat3_600=session['cat'][12],
                           cat3_800=session['cat'][13],
                           cat3_1000=session['cat'][14],
                           cat4_200=session['cat'][15],
                           cat4_400=session['cat'][16],
                           cat4_600=session['cat'][17],
                           cat4_800=session['cat'][18],
                           cat4_1000=session['cat'][19],
                           cat5_200=session['cat'][20],
                           cat5_400=session['cat'][21],
                           cat5_600=session['cat'][22],
                           cat5_800=session['cat'][23],
                           cat5_1000=session['cat'][24],
                           )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) 
    app.run(debug=True, host='0', port=port)