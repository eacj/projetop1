###########################################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Eric Araujo
#            Pedro Vinicius
#
# Email:    eacj@cin.ufpe.br
#            pvls@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Eric Araujo, Pedro Vinicius.
#
###########################################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"`/\',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result


def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))


def stopWords(fname):
    '''Pega as palavras de um arquivo de stop words e os guarda em uma lista.'''
    lista = []
    f = open(fname, 'r')
    for termo in f.readlines():        
        limpa = clean_up(termo)        
        lista.append(limpa)
    f.close()
    return lista

def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    words = dict()
    stop = stopWords('stopWords.txt')                           #lista de stopWords
    f = open(fname, 'r')
    for linha in f.readlines():
        separar = list(split_on_separators(linha,' '))          #separa em palavras a linha do arquivo, e retorna uma lista com as mesmas.
        score = int(separar.pop(0))                             #retira o score da lista e o salva.
        f.close() 
        for palavra in separar: 
            limpa = clean_up(palavra)                           #depois que o score e' retirado, as palavras sao limpadas pela funcao uma a uma.
            if limpa != '':                                     #se por acaso a palavra apresentar alguma restricao do clean_up, ela devolve string vazia. 
                for PalStop in stop:                            #checa se a palavra depois de limpa e nao string vazia, esta na lista de stopWords.
                    if PalStop == limpa:                        #se tiver a renomeia como string vazia e nao entra na condicao posterior. 
                        limpa = ''
                if limpa != '':
                    if limpa not in words:                      #checa se e' uma nova palavra, se for ela e' adicionada no dicionario.          
                        freq = 1
                        words[limpa] = [limpa,freq,score]
                        
                    else:
                        words[limpa][1] += 1
                        words[limpa][2] += score                #se ela ja' existir, apenas soma a seus devidos lugares.
        
    
    for elemento in words:        
        media = words[elemento][2]//words[elemento][1]
        words[elemento] = (elemento,words[elemento][1],media)   #renomeia cada conteudo das chaves do dicionario com a frequencia geral e a media dos scores inteiros.
                                                      
    
    return words


def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	retorna um vetor/lista de pares (escore,texto) dos
	comentarios presentes no arquivo.
    '''    
    reviews = []
    f = open(fname,'r')
    for linha in f.readlines():                                 #le as linhas, as limpa de algumas restricoes.
        limpa = clean_up(linha)
        palavras = []                                           #apenas é criado uma lista local para separar as strings e pegar o score na posicao 1.
        for partes in limpa:                                    #mesmo pegando string por string e adicionando na lista, o objetivo é pegar o score.
            palavras.append(partes)
            
        Pont = int(palavras.pop(0))                             #pega o score.
        reviews.append((Pont,limpa[1:]))                        #adiciona na lista reviews a pontuacao e o comentario e os coloca na tupla e poe na lista.
    
    
    f.close()
    
    # Implementado
    return reviews


def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''

    score = 0.0
    count = 0                                                   #aqui checa o comentario e calcula a media score/count.
    stop = stopWords('stopWords.txt')
    if review != '':    
        separar = list(split_on_separators(review, ' '))        #separa.  
        for palavra in separar:
            limpa = clean_up(palavra)                           #limpa.
            if limpa != '':                                     #se a funcao devolver string vazia, ela nao entra.
                for PalStop in stop:                            #checa se a palavra esta nas stopWords, para quando chegar na proxima parte nao ir somando o desnecessario.
                    if PalStop == limpa:                
                        limpa = ''
                if limpa in words:                              #se existir, soma o score que ta salvo no dicionario na chave da palavra e soma o count.
                    score += words[limpa][2]
                    count += 1
                else:
                    score += 2                                  #se nao existir, soma 2 no score, porque e' neutro.
                    count += 1
    
    return score/count


def computeSumSquaredErrors(reviews, words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    resultado_final = 0
    for frase in reviews:                                       #calcula o resultado final, a soma dos quadrados dos erros.
        sentimento = computeSentiment(frase[1], words)          #devolve o score/count.
        if frase[0] != sentimento:
            diferenca = frase[0] - sentimento                   #faz a diferenca entre a nota do comentario e o sentimento obtido da frase.
            resultado = diferenca**2
            resultado_final += resultado
            sse = resultado_final / len(reviews)
            
    return sse


def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()

