# Analizador Sintáctico para el Bucle 'for'
# Estructura: for target_list in expression_list : (simple_stmt | suite+ (else : Newline | suite_else)?)

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
        while self.current_char is not None and self.current_char in ' \t\r\n':
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char in ' \t\r\n':
                self.skip_whitespace()
                continue
            if self.current_char == ':':
                self.advance()
                return Token(':', ':')
            if self.current_char.isalpha() or self.current_char == '_':
                result = ''
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
                if result == 'for':
                    return Token('FOR', 'for')
                elif result == 'in':
                    return Token('IN', 'in')
                elif result == 'else':
                    return Token('ELSE', 'else')
                else:
                    return Token('IDENTIFIER', result)
            raise Exception(f"Caracter inválido: {self.current_char}")
        return Token('EOF', None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, mensaje):
        raise Exception(f"Error de sintaxis en bucle for: {mensaje}")

    def eat(self, token_tipo):
        if self.current_token.tipo == token_tipo:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Se esperaba {token_tipo}, se encontró {self.current_token.tipo}")

    def parse(self):
        self.eat('FOR')
        self.eat('IDENTIFIER')
        self.eat('IN')
        self.eat('IDENTIFIER')
        self.eat(':')

        # Cuerpo del bucle
        self.eat('IDENTIFIER')

        # Opcional else
        if self.current_token.tipo == 'ELSE':
            self.eat('ELSE')
            self.eat(':')
            self.eat('IDENTIFIER')

        print("Bucle 'for' en Python analizado sintacticamente con exito")

if __name__ == "__main__":
    test_code0 = "for item in items: procesar"
    test_code1 = "for item in items: procesar else: no_procesar"

    print(f"Analizando: {test_code0}")
    lexer0 = Lexer(test_code0)
    parser0 = Parser(lexer0)
    parser0.parse()

    print(f"Analizando: {test_code1}")
    lexer1 = Lexer(test_code1)
    parser1 = Parser(lexer1)
    parser1.parse()
