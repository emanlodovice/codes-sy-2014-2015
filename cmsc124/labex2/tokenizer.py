import re


class Tokenizer(object):
    token_names = {
        'operator': ['+', '-', '/', '*', '%', '=', '<', '>', '!', '&', '->',
                     '++', '--', '<<', '>>', '<=', '>=', '==', '!=', '^', '|',
                     '&&', '||', '*=', '/=', '+=', '-=', '&=', '^=', '|='],
        'punctuator': ['{', '}', '(', ')', ';', '"', '\'', ',', '[', ']', '"'],
        'macro': re.compile('^#.+'),
        'function': re.compile('[a-zA-Z_][a-zA-Z0-9_]+'),
        'function call': re.compile('[a-zA-Z_][a-zA-Z0-9_]+'),
        'data type': ['int', 'long', 'float', 'double', 'char'],
        'variable': re.compile('[a-zA-Z_][a-zA-Z0-9_]*'),
        'value': re.compile('^[0-9]+\.?[0-9]*$|".*'),
        'keyword': ['if', 'else', 'for', 'while', 'do', 'switch', 'case',
                    'return'],
        'parameter': '.+',
        'argument': '.+',
        'comment': re.compile('^//.*|^\*.+')}

    def __init__(self, code):
        code = code.splitlines()
        cleaned = []
        for c in code:
            cleaned.append(c.strip())
        self.tokens = self._extract_tokens(cleaned)
    
    def print_distinct(self):
        for key in self.tokens:
            if len(self.tokens[key]) > 0:
                seen = []
                print key
                for code in self.tokens[key]:
                    if code not in seen:
                        seen.append(code)
                        print '   ' + code

    def _extract_tokens(self, lines):
        tokens = {
            'operator': [],
            'punctuator': [],
            'macro': [],
            'function': [],
            'function call': [],
            'data type': [],
            'variable': [],
            'value': [],
            'keyword': [],
            'parameter': [],
            'argument': [],
            'unknown': [],
            'comment': []}
        current_text = ''

        prev = None
        cur = None

        #flags
        was_string = False

        open_parenthesis_ctr = 0
        for code in lines:
            for c in code:
                if c in self.token_names['operator']:
                    if cur is not None:
                        # check if current string represents an operator
                        if cur == 'operator':
                            # check if current string can be a comment tag
                            if current_text + c in ['//', '/*']:
                                cur = 'comment'
                                current_text += c
                            else:
                                # check if possible comparator or same operator
                                if current_text + c in self.token_names[
                                        'operator']:
                                    current_text += c
                                    tokens[cur].append(current_text)
                                else:
                                    tokens[cur].append(current_text)
                                    tokens[cur].append(c)
                                current_text = ''
                                prev = cur
                                cur = None
                        elif cur == 'comment':
                            if current_text[:2] == '//':
                                current_text += c
                            else:
                                if c == '/' and current_text[-1] == '*':
                                    current_text += c
                                    tokens[cur].append(current_text)
                                    cur = None
                                    prev = 'comment'
                                    current_text = ''
                                else:
                                    current_text += c
                        # check if current string represents a macro
                        elif cur == 'macro':
                            if c == '>':
                                current_text += c
                                tokens['macro'].append(current_text)
                                current_text = ''
                                prev = cur
                                cur = None
                            elif c == '<':
                                current_text += c
                        # check if current string represents a
                        # parameter/argument or a string value
                        elif (cur in ['argument', 'parameter'] or
                                (cur == 'value' and was_string)):
                            current_text += c
                        else:
                            tokens[cur].append(current_text)
                            current_text = c
                            prev = cur
                            cur = 'operator'
                    # if no current string
                    else:
                        if prev in ['argument', 'parameter']:
                            current_text += c
                            cur = prev
                        elif prev == 'function':
                            current_text += c
                            cur = 'parameter'
                        elif prev == 'function call':
                            current_text += c
                            cur = 'argument'
                        else:
                            if current_text != '':
                                tokens['unknown'].append(current_text)
                            current_text = c
                            prev = cur
                            cur = 'operator'
                elif cur == 'comment':
                    current_text += c
                # check if current character is '('
                elif c == '(':
                    # check if current string represents a variable
                    if cur == 'variable':
                        if prev == 'data type':
                            tokens['function'].append(current_text)
                            tokens['punctuator'].append(c)
                            prev = 'function'
                            cur = None
                            current_text = ''
                        else:
                            tokens['function call'].append(current_text)
                            tokens['punctuator'].append(c)
                            prev = 'function call'
                            cur = None
                            current_text = ''
                        open_parenthesis_ctr = 1
                    # check if current string represents a keyword
                    elif cur == 'keyword':
                        tokens['keyword'].append(current_text)
                        tokens['punctuator'].append(c)
                        current_text = ''
                        prev = 'keyword'
                        cur = None
                    # check if current string represents a string value
                    elif cur == 'value' and was_string:
                        current_text += c
                    elif cur in ['parameter', 'argument']:
                        current_text += c
                        if not was_string:
                            open_parenthesis_ctr += 1
                    else:
                        if current_text != '':
                            if cur:
                                tokens[cur].append(current_text)
                            else:
                                tokens['unknown'].append(current_text)
                            tokens['punctuator'].append(c)
                            prev = 'punctuator'
                            cur = None
                            current_text = ''
                        else:
                            if prev == 'function':
                                current_text += c
                                cur = 'parameter'
                            elif prev == 'function call':
                                current_text += c
                                cur = 'argument'
                        open_parenthesis_ctr += 1
                elif c == ')':
                    if cur in ['parameter', 'argument']:
                        if was_string:
                            current_text += c
                        else:
                            open_parenthesis_ctr -= 1
                            if open_parenthesis_ctr == 0:
                                tokens[cur].append(current_text)
                                tokens['punctuator'].append(c)
                                current_text = ''
                                prev = 'punctuator'
                                cur = None
                            else:
                                current_text += c
                    elif cur == 'value' and was_string:
                        current_text += c
                    else:
                        if current_text != '':
                            if cur:
                                tokens[cur].append(current_text)
                            else:
                                tokens['unknown'].append(current_text)
                        tokens['punctuator'].append(c)
                        prev = 'punctuator'
                        cur = None
                        current_text = ''
                        open_parenthesis_ctr -= 1
                elif c == ',':
                    if cur in ['parameter', 'argument']:
                        if open_parenthesis_ctr == 1:
                            tokens[cur].append(current_text)
                            tokens['punctuator'].append(c)
                            prev = 'function'
                            if cur == 'argument':
                                prev = 'function call'
                            cur = None
                        else:
                            current_text += c
                    if cur == 'value' and was_string:
                        current_text += c
                    else:
                        if current_text != '':
                            if cur:
                                tokens[cur].append(current_text)
                            else:
                                tokens['unknown'].append(current_text)
                            prev = 'punctuator'
                            cur = None
                        else:
                            if prev not in ['function', 'function call']:
                                prev = 'punctuator'
                                cur = None
                        current_text = ''
                        tokens['punctuator'].append(c)
                elif c == ' ':
                    if (cur in ['operator', 'punctuator', 'data type',
                                'variable', 'keyword']):
                        tokens[cur].append(current_text)
                        current_text = ''
                        prev = cur
                        cur = None
                    elif cur == 'value':
                        if was_string:
                            current_text += c
                        else:
                            tokens[cur].append(current_text)
                            prev = cur
                            cur = None
                            current_text = ''
                    else:
                        if current_text != '':
                            current_text += c
                elif c == '"':
                    if current_text == '':
                        current_text += c
                        if prev == 'function':
                            cur = 'parameter'
                        elif prev == 'function call':
                            cur = 'argument'
                        else:
                            cur = 'value'
                        tokens['punctuator'].append(c)
                        was_string = True
                    else:
                        if cur in ['variable', 'parameter', 'argument']:
                            if current_text[-1] == '\\':
                                current_text += c
                            else:
                                was_string = False
                                tokens['punctuator'].append(c)
                                current_text += c
                                tokens[cur].append(current_text)
                                if cur == 'parameter':
                                    prev = 'function'
                                elif cur == 'argument':
                                    prev = 'function call'
                                else:
                                    prev = cur
                                cur = None
                                current_text = ''
                elif c in self.token_names['punctuator']:
                    if ((cur == 'value' and was_string) or
                            (cur in ['parameter', 'argument'])):
                        current_text += c
                    else:
                        if current_text != '':
                            if cur:
                                tokens[cur].append(current_text)
                            else:
                                tokens['unknown'].append(current_text)
                            current_text = ''
                            tokens['punctuator'].append(c)
                            prev = 'punctuator'
                            cur = None
                        else:
                            # if prev == 'keyword':
                            #     current_text += c
                            #     cur = 'parameter'
                            # else:
                            tokens['punctuator'].append(c)
                            prev = 'punctuator'
                            cur = None
                else:
                    if cur == 'operator':
                        tokens[cur].append(current_text)
                        current_text = ''
                        prev = cur
                        cur = None
                    current_text += c
                    if self.token_names['macro'].match(current_text):
                        cur = 'macro'
                    elif current_text in self.token_names['data type']:
                        cur = 'data type'
                    elif current_text in self.token_names['keyword']:
                        cur = 'keyword'
                    else:
                        if prev == 'function':
                            cur = 'parameter'
                        elif prev == 'function call':
                            cur = 'argument'
                        elif cur != 'macro':
                            if self.token_names['value'].match(current_text):
                                cur = 'value'
                            elif self.token_names['variable'].match(
                                    current_text):
                                cur = 'variable'
                            else:
                                cur = None
                        elif cur == 'value':
                            if not self.token_names['value'].match(
                                    'current_text'):
                                cur = None
            if cur == 'comment':
                if current_text[:2] == '//':
                    tokens[cur].append(current_text)
                    prev = cur
                    cur = None
                    current_text = ''
                else:
                    current_text += '\n'
            else:
                if current_text != '':
                    if cur:
                        tokens[cur].append(current_text)
                    else:
                        tokens['unknown'].append(current_text)
                    prev = cur
                    cur = None
                    current_text = ''



        return tokens


def test():
    with open('sample.c') as f:
        code = f.read()
        # print code
        a = Tokenizer(code)
        a.print_distinct()


test()