class Tokenizer(object):
    token_names = {
        'punctuator': ['+', '-', '/', '*', '%', '{', '}', '(', ')', ';',
                       '=', '"', '\'', ','],
        'macro': '#.+',
        'function': '[a-zA-Z0-9_]+',
        'function call': '[a-zA-Z0-9_]+',
        'data type': ['int', 'long', 'float', 'double', 'char'],
        'variable': '[a-zA-Z0-9_]+',
        'value': '.+',
        'keywords': ['if', 'else', 'for', 'while', 'do'],
        'parameters': '.+'}

    def __init__(self, code):
        code = code.splitlines()
        text = ''
        for c in code:
            text += c.strip()
        self.tokens = {'punctuator': [], 'macro': [], 'function': [],
                       'function call': [], 'data type': [], 'variable': [],
                       'value': [], 'keywords': [], 'parameters': []}
        self._extract_tokens(text)

    def _extract_tokens(self, code):
        self.stack = []
        current_text = ""
        prev = None
        last = None
        for c in code:
            if self._last_token is None:
                pass


def test():
    with open('sample.c') as f:
        code = f.read()
        print code
        Tokenizer(code)


test()