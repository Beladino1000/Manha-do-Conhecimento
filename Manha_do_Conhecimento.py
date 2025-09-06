from flask import Flask, render_template, request, session, redirect
from datetime import timedelta
import string
import random as r
import sympy as sp
import os
app = Flask(__name__)
app.secret_key = 'Pedro Couto'
app.permanent_session_lifetime = timedelta(days=1)

pontuação = r"!@#$%¨&*()_=+§²¹³£¢¬[{]}ªº´`^~;:>,</?\|°- "
acentuadas = "áàãâäÁÀÃÂÄéèêëÉÈÊËíìîïÍÌÎÏóòõôöÓÒÕÔÖúùûüÚÙÛÜçÇ"
sem_acento = "aaaaaAAAAAeeeeEEEEiiiiIIIIoooooOOOOOuuuuUUUUcC"

def replace_letras(b: str)->str:
    tabela=str.maketrans('','',string.ascii_letters)
    return b.translate(tabela)

def replace_master(texto: str)->str:
    tabela1=str.maketrans(acentuadas, sem_acento)
    tabela2=str.maketrans('','',pontuação)
    return texto.translate(tabela1).translate(tabela2)

def elemento_comum(lista1,lista2):
    for elem in lista1:
        if elem in lista2:
            return elem
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

    certos=['certo200','certo400','certo600','certo800','certo1000']
    errados=['errado200','errado400','errado600','errado800','errado1000']
    if elemento_comum(certos,request.form):
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])+int(replace_letras(elemento_comum(certos,request.form)))

    if elemento_comum(errados,request.form):
        session['aba'] = 'Trivia-master/Trivia.html'
        session['pontuação']=int(session['pontuação'])-(int(replace_letras(elemento_comum(errados,request.form)))//2)

    explicações=['Com 66,26% e 55,67% dos votos, o plebiscito de 1993 determinou o sistema de governo do Brasil como uma República Presidencialista.', 'Ao contrário das demais alternativas, campanhas de vacinação em massa estão associadas com o aumento radical da população global nos Séculos XX e XXI.', 'Ainda que os Estados Unidos seja um dos maiores produtores e consumidores de petróleo do mundo, sua posição geopolítica distancia o país de ser filiado à OPEP.', 'O delta é uma das partes mais icônicas de um rio, e costumam ser lugares ideais para a habitação humana. Os deltas do Rio Nilo e do Rio Amazonas podem ser facilmente vistos do espaço!', 'Através de um processo lento, a água da chuva chega às cavernas, e ao gotejar na ponta da estalactite, libera dióxido de carbono e deposita minerais, permitindo o crescimento da estrutura. Já jogou Minecraft?', 'Alguns animais põem ovos, outros não. A galinha é um exemplo clássico de animal que bota ovos, enquanto cachorros, gatos e cavalos dão à luz filhotes vivos.', 'As plantas conseguem produzir seu próprio alimento usando luz solar, água e gás carbônico em um processo chamado fotossíntese. Durante esse processo, elas transformam a energia da luz em glicose (um tipo de açúcar) que serve como alimento para crescer e se manter vivas. Além disso, liberam oxigênio, que é essencial para a respiração de animais e seres humanos.', 'No DNA, as bases nitrogenadas se emparelham de forma específica: adenina com timina, e citosina com guanina. No RNA, que é uma molécula parecida com o DNA mas geralmente de fita simples, a timina não existe. No lugar dela, entra a uracila (U), que se liga à adenina (A).<br>Ou seja, enquanto o DNA usa A-T e C-G, o RNA usa A-U e C-G. Isso é importante porque o RNA é usado para copiar a informação do DNA e levar às células para produzir proteínas, funcionando como uma “mensagem temporária” da informação genética.', 'A respiração celular é o processo pelo qual os seres vivos obtêm energia dos alimentos. Durante esse processo, a glicose é quebrada e liberada energia, e como resultado é produzido dióxido de carbono (CO₂), que é devolvido à atmosfera. Esse CO₂ pode depois ser usado pelas plantas na fotossíntese, completando o ciclo do carbono na natureza.', 'Anelídeos, como minhocas e sanguessugas, têm o corpo dividido em segmentos chamados metâmeros. Cada segmento possui órgãos repetidos ou semelhantes, o que facilita o movimento e a organização do corpo.', 'Apesar do arquivo .bat executar um código, arquivos .exe são arquivos que podem ser executados.', 'Em python, utiliza-se print() para se mostrar uma mensagem na tela, mais especificamente, no terminal.', 'CPU significa Central processing unit', 'Alan Turing é o portador do título de pai da computação, apesar de nunca ter sido totalmente reconhecido em seu país pelo fato de ser homossexual', 'Tim Berners Lee foi um físico britânico, cientista da computação e professor do MIT. Ele foi responsável por criar a World Wide Web', 'Deodoro da Fonseca assumiu a presidência em 1889, após a Proclamação da República.', 'O lema “Liberdade, Igualdade e Fraternidade” tornou-se o símbolo dos ideais da Revolução.', 'A França foi invadida pela Alemanha em 1940 e não fazia parte da aliança do Eixo (Alemanha, Itália e Japão).', 'O czar Alexandre I foi o responsável por enfrentar Napoleão, usando a estratégia da “terra arrasada”.', 'O Primeiro Triunvirato foi uma aliança política entre Júlio César, Pompeu e Crasso.', 'Um número primo é aquele que só pode ser dividido por 1 e por ele mesmo, sem sobrar nada. Então: 2 é primo (só divide por 1 e 2), 3 é primo (1 e 3), 5 é primo (1 e 5) e 7 é primo (1 e 7). Os outros não servem porque têm mais divisores. Assim, existem 4 números primos no intervalo de 0 a 10.', 'Maria aplica seu dinheiro e ele cresce 10% ao ano. Como os juros vão sendo reinvestidos, isso é chamado de juros compostos. A fórmula é:<br>M=P⋅(1+i)t<br>onde M é o valor final, P é o valor inicial, i é a taxa (0,1 no caso) e t o tempo. Para dobrar o dinheiro, fazemos 2P=P⋅(1,1)t; Cortando o P, sobra 2 = 1,1t. Para resolver, usamos logaritmo (ou uma calculadora para quem não aprendeu log ainda):<br>t=ln⁡(2)/ln⁡(1,1) = 7,27 (aproximadamente)<br>Ou seja, em pouco mais de 7 anos o valor dobra. Como precisa passar 1 ano inteiro para o dinheiro render e não 0,27 anos, a resposta correta é 8 anos.', 'Quando fazemos potência, temos duas regrinhas que sempre funcionam separadas: qualquer número não nulo elevado a 0 dá 1 (ex.: 150 = 1), e 0 elevado a qualquer número positivo dá 0 (ex.: 03 = 0). Se tentarmos aplicar as duas ao mesmo tempo em 00, elas batem de frente: uma sugere 1, a outra sugere 0. Na matemática, olhamos também “como chegamos” a esse ponto: se aproximamos por contas do tipo x0 com x tendendo a 0, o resultado aproxima 1; se aproximamos por 0y com y tendendo a 0, o resultado aproxima 0 Como depende do caminho, não há um único resultado natural—por isso dizemos que 00 é indeterminado. (Em alguns contextos específicos, como combinatória, às vezes definem 00=1 por conveniência, mas isso é uma convenção, não uma regra geral.)', 'O número 360 pode ser decomposto em fatores primos como 23⋅32⋅5. O Teorema Fundamental da Aritmética diz exatamente isso: todo número inteiro maior que 1 pode ser escrito de uma única forma como produto de números primos, mudando apenas a ordem. Ou seja, não existe outro jeito diferente de fatorar 360 em primos, sempre chegaremos a 23⋅32⋅5.', 'A área inicial é 121π = πr2; r2=121; r=11; <br>O novo raio é 11+1=12 cm, então a área nova é π⋅122=π⋅144=144π<br>Número de pedaços: 144π÷3,6π = 144÷3,6 = 40, o resultado é 40 pedaços.<br>Dividindo entre 8 irmãs (nove filhas excluindo Severina): 40÷8 = 5 pedaços para cada uma.<br>Como são 5 (pedaços) para as 8 (irmãs), a hora é 7:55.']

    if 'explicacao' not in session:
        session['explicacao']=''

    if 'cat' not in session:
        session['cat']=['']*25

    if 'cat1-200' in request.form and not session['cat'][0]=='Press':
        session['aba'] = 'Trivia-master/cat1-200.html'
        session['cat'][0]='Press'
        session['explicacao']=explicações[0]
    if 'cat1-400' in request.form and not session['cat'][1]=='Press':
        session['aba'] = 'Trivia-master/cat1-400.html'
        session['cat'][1]='Press'
        session['explicacao']=explicações[1]
    if 'cat1-600' in request.form and not session['cat'][2]=='Press':
        session['aba'] = 'Trivia-master/cat1-600.html'
        session['cat'][2]='Press'
        session['explicacao']=explicações[2]
    if 'cat1-800' in request.form and not session['cat'][3]=='Press':
        session['aba'] = 'Trivia-master/cat1-800.html'
        session['cat'][3]='Press'
        session['explicacao']=explicações[3]
    if 'cat1-1000' in request.form and not session['cat'][4]=='Press':
        session['aba'] = 'Trivia-master/cat1-1000.html'
        session['cat'][4]='Press'
        session['explicacao']=explicações[4]

    if 'cat2-200' in request.form and not session['cat'][5]=='Press':
        session['aba'] = 'Trivia-master/cat2-200.html'
        session['cat'][5]='Press'
        session['explicacao']=explicações[5]
    if 'cat2-400' in request.form and not session['cat'][6]=='Press':
        session['aba'] = 'Trivia-master/cat2-400.html'
        session['cat'][6]='Press'
        session['explicacao']=explicações[6]
    if 'cat2-600' in request.form and not session['cat'][7]=='Press':
        session['aba'] = 'Trivia-master/cat2-600.html'
        session['cat'][7]='Press'
        session['explicacao']=explicações[7]
    if 'cat2-800' in request.form and not session['cat'][8]=='Press':
        session['aba'] = 'Trivia-master/cat2-800.html'
        session['cat'][8]='Press'
        session['explicacao']=explicações[8]
    if 'cat2-1000' in request.form and not session['cat'][9]=='Press':
        session['aba'] = 'Trivia-master/cat2-1000.html'
        session['cat'][9]='Press'
        session['explicacao']=explicações[9]

    if 'cat3-200' in request.form and not session['cat'][10]=='Press':
        session['aba'] = 'Trivia-master/cat3-200.html'
        session['cat'][10]='Press'
        session['explicacao']=explicações[10]
    if 'cat3-400' in request.form and not session['cat'][11]=='Press':
        session['aba'] = 'Trivia-master/cat3-400.html'
        session['cat'][11]='Press'
        session['explicacao']=explicações[11]
    if 'cat3-600' in request.form and not session['cat'][12]=='Press':
        session['aba'] = 'Trivia-master/cat3-600.html'
        session['cat'][12]='Press'
        session['explicacao']=explicações[12]
    if 'cat3-800' in request.form and not session['cat'][13]=='Press':
        session['aba'] = 'Trivia-master/cat3-800.html'
        session['cat'][13]='Press'
        session['explicacao']=explicações[13]
    if 'cat3-1000' in request.form and not session['cat'][14]=='Press':
        session['aba'] = 'Trivia-master/cat3-1000.html'
        session['cat'][14]='Press'
        session['explicacao']=explicações[14]

    if 'cat4-200' in request.form and not session['cat'][15]=='Press':
        session['aba'] = 'Trivia-master/cat4-200.html'
        session['cat'][15]='Press'
        session['explicacao']=explicações[15]
    if 'cat4-400' in request.form and not session['cat'][16]=='Press':
        session['aba'] = 'Trivia-master/cat4-400.html'
        session['cat'][16]='Press'
        session['explicacao']=explicações[16]
    if 'cat4-600' in request.form and not session['cat'][17]=='Press':
        session['aba'] = 'Trivia-master/cat4-600.html'
        session['cat'][17]='Press'
        session['explicacao']=explicações[17]
    if 'cat4-800' in request.form and not session['cat'][18]=='Press':
        session['aba'] = 'Trivia-master/cat4-800.html'
        session['cat'][18]='Press'
        session['explicacao']=explicações[18]
    if 'cat4-1000' in request.form and not session['cat'][19]=='Press':
        session['aba'] = 'Trivia-master/cat4-1000.html'
        session['cat'][19]='Press'
        session['explicacao']=explicações[19]

    if 'cat5-200' in request.form and not session['cat'][20]=='Press':
        session['aba'] = 'Trivia-master/cat5-200.html'
        session['cat'][20]='Press'
        session['explicacao']=explicações[20]
    if 'cat5-400' in request.form and not session['cat'][21]=='Press':
        session['aba'] = 'Trivia-master/cat5-400.html'
        session['cat'][21]='Press'
        session['explicacao']=explicações[21]
    if 'cat5-600' in request.form and not session['cat'][22]=='Press':
        session['aba'] = 'Trivia-master/cat5-600.html'
        session['cat'][22]='Press'
        session['explicacao']=explicações[22]
    if 'cat5-800' in request.form and not session['cat'][23]=='Press':
        session['aba'] = 'Trivia-master/cat5-800.html'
        session['cat'][23]='Press'
        session['explicacao']=explicações[23]
    if 'cat5-1000' in request.form and not session['cat'][24]=='Press':
        session['aba'] = 'Trivia-master/cat5-1000.html'
        session['cat'][24]='Press'
        session['explicacao']=explicações[24]

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
                           mensagem=session['explicacao']
                           )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) 
    app.run(debug=True, host='0', port=port)