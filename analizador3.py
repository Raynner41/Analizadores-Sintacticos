# Analizador Sintáctico para Defini funciones
# Estructura: def function_name ([parameter [, parameter ...]]) : simple_stmt | \n statement*

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            if self.current_char == '\n':
                self.advance()
                return Token('NEWLINE', '\n')
            if self.current_char in '(),:':
                char = self.current_char
                self.advance()
                return Token(char, char)
            if self.current_char.isalpha() or self.current_char == '_':
                result = ''
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
                if result == 'def':
                    return Token('DEF', 'def')
                else:
                    return Token('IDENTIFIER', result)
            raise Exception(f"Caracter invalido: {self.current_char}")
        return Token('EOF', None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis en funcion: {mensaje}")

    def eat(self, token_tipo):
        if self.current_token.tipo == token_tipo:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Se esperaba {token_tipo}, se encontró {self.current_token.tipo}")

    def parse(self):
        self.eat('DEF')
        if self.current_token.tipo == 'IDENTIFIER':
            func_name = self.current_token.valor
            self.eat('IDENTIFIER')
        else:
            self.error("Se esperaba el nombre de la función")

        # Parametros opcionales entre parentesis
        if self.current_token.tipo == '(':
            self.eat('(')
            if self.current_token.tipo == 'IDENTIFIER':
                self.eat('IDENTIFIER')
                while self.current_token.tipo == ',':
                    self.eat(',')
                    self.eat('IDENTIFIER')
            self.eat(')')

        self.eat(':')

        # Cuerpo: simple_stmt o con salto de línea
        if self.current_token.tipo == 'NEWLINE':
            self.eat('NEWLINE')
            while self.current_token.tipo == 'IDENTIFIER':
                self.eat('IDENTIFIER')
        else:
            if self.current_token.tipo == 'IDENTIFIER':
                self.eat('IDENTIFIER')

        print("Definicion de función en Python analizada sintacticamente con exito")

if __name__ == "__main__":
    test_code0 = "def calcular(a, b):\n    resultado"
    test_code1 = "def serie(a, b, c, d, f, g): la_serie"
    test_code2 = "function funcion(a, b): res"

    print(f"Analizando: {test_code0}")
    lexer0 = Lexer(test_code0)
    parser0 = Parser(lexer0)
    parser0.parse()

    print(f"Analizando: {test_code1}")
    lexer1 = Lexer(test_code1)
    parser1 = Parser(lexer1)
    parser1.parse()

    # Prueba de error
    print(f"Analizando: {test_code2}")
    lexer2 = Lexer(test_code2)
    parser2 = Parser(lexer2)
    parser2.parse()
