from lexer import lexer
import re


#gramatica ´
# Exp  --> Term Exp2
# Exp2 --> SUM Term Exp2
#        | SUB Term Exp2
#        | ε

# Term --> Factor Term2
# Term2 --> MUL Factor Term2
#         | DIV Factor Term2
#         | ε

# Factor --> INT
#          | PA Exp PF
prox_simb = ('Erro', '', 0, 0)

    





def rec_Factor():
    global prox_simb
    if prox_simb and prox_simb.type == 'INT':
        print(f"Reconheci INT {prox_simb.value}")
        prox_simb = lexer.token()
    elif  prox_simb and prox_simb.type == 'PA':
        prox_simb = lexer.token()  # consome '('
        rec_Exp()
        if prox_simb and prox_simb.type == 'PF':
            prox_simb = lexer.token()  # consome ')'
        else:
            print("Erro: esperava ')'")
    else:
        print(f"Erro: esperava INT ou '(' em vez de ' {prox_simb.value} ' ")

def rec_TermTwo():
    global prox_simb
    if prox_simb and (prox_simb.type == 'MUL' or prox_simb.type == 'DIV'):
        op = prox_simb.type
        prox_simb = lexer.token()   # consome o operador
        rec_Factor()
        rec_TermTwo()
    else:
        pass

def rec_Term():
    rec_Factor()
    rec_TermTwo()


def rec_ExpTwo():
    global prox_simb
    if prox_simb and (prox_simb.type == 'SUM' or prox_simb.type == 'SUB'):
        op = prox_simb.type
        prox_simb = lexer.token()   
        rec_Term()
        rec_ExpTwo() 
    else:
        pass

def rec_Exp():
    rec_Term()
    rec_ExpTwo()

def rec_Parser(linha):
 
    global prox_simb
    lexer.input(linha)
    prox_simb = lexer.token()
    rec_Exp()
    print("That's all folks!")

linha = input("Introduza uma expressão: ")
rec_Parser(linha)
