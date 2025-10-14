import json, sys
from lexe import lexer
from datetime import date



def main():
    with open("stock.json","r", encoding="utf-8") as f:
        stock = json.load(f)
    euro = 0.0
    
    lexer.dados = stock
    lexer.euro = euro
    
    data=date.today()
    print(f"{data}, Stock carregado, Estado atualizado.")
    print("Bom dia. Estou disponível para atender o seu pedido.")
    for linha in sys.stdin:
        lexer.input(linha)
        lexer.input(linha)
        tok = lexer.token()
        while tok:
            tok = lexer.token()


    
    with open("stock.json", "w", encoding="utf-8") as f:
        json.dump(lexer.dados, f, indent=4, ensure_ascii=False)

    print("Até à próxima")
    return


if __name__ == "__main__":
    main()