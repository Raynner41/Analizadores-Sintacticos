# Analizador Sintáctico para Expresiones logicas
# Estructura: expresion_logica -> '(' (or|and|termino|termino) termino (and|factor|factor) (not|()|True|False) expresion_logica? ')'

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
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char in '()':
                char = self.current_char
                self.advance()
                return Token(char, char)
            if self.current_char.isalpha() or self.current_char == '_':
                result = ''
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
                if result in ('and', 'or', 'not', 'True', 'False'):
                    return Token(result.upper(), result)
                else:
                    return Token('TERMINO', result)
            raise Exception(f"Caracter inválido: {self.current_char}")
        return Token('EOF', None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis: {mensaje}")

    def eat(self, token_tipo):
        if self.current_token.tipo == token_tipo:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Se esperaba {token_tipo}, se encontró {self.current_token.tipo}")

    def parse(self):
        # expresion_logica
        self.eat('(')
        # Operadores logicos y terminos
        if self.current_token.tipo in ('AND', 'OR'):
            self.current_token = self.lexer.get_next_token()

        # Procesar termino principal
        if self.current_token.tipo == 'TERMINO' or self.current_token.tipo in ('TRUE', 'FALSE'):
            self.current_token = self.lexer.get_next_token()
        elif self.current_token.tipo == '(':
            self.parse()
        # Opcional factor / operador secundario
        if self.current_token.tipo in ('AND', 'NOT'):
            self.current_token = self.lexer.get_next_token()
            if self.current_token.tipo == '(':
                self.parse()
            elif self.current_token.tipo in ('TERMINO', 'TRUE', 'FALSE'):
                self.current_token = self.lexer.get_next_token()

        self.eat(')')
        print("¡Expresión lógica analizada sintacticamente con exito")

if __name__ == "__main__":
    test_expr0 = "(and termino and True)"
    test_expr1 = "(or termino and False)"
    test_expr2 = "(termino termino and termino)"
    test_expr3 = "(termino no or y termino)"

    print(f"Analizando: {test_expr0}")
    lexer0 = Lexer(test_expr0)
    parser0 = Parser(lexer0)
    parser0.parse()

    print(f"Analizando: {test_expr1}")
    lexer1 = Lexer(test_expr1)
    parser1 = Parser(lexer1)
    parser1.parse()

    print(f"Analizando: {test_expr2}")
    lexer2 = Lexer(test_expr2)
    parser2 = Parser(lexer2)
    parser2.parse()

    print(f"Analizando: {test_expr3}")
    lexer3 = Lexer(test_expr3)
    parser3 = Parser(lexer3)
    parser3.parse()
