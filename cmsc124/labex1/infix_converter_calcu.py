import re


class PostFix(object):

    def __init__(self):
        super(PostFix, self).__init__()
        self.__preceed = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3,
                          '(': 0}

    def convert(self, express):
        stack = []
        express = express.replace(' ', '')
        res = []
        prev_is_var = False
        prev_is_paren = False
        for char in express:
            if char not in self.__preceed and char != '(' and char != ')':
                if prev_is_var:
                    res[-1] += str(char)
                else:
                    res.append(str(char))
                prev_is_var = True
            elif char == '(':
                if prev_is_var:
                    return "Invalid Expression!"
                prev_is_var = False
                stack.append(char)
            elif char == ')':
                if not prev_is_var:
                    return "Invalid Expression!"
                index = len(stack) - 1
                try:
                    while stack[index] != '(':
                        res.append(stack[index])
                        index -= 1
                    stack = stack[:index]
                except IndexError:
                    return 'Not Matching Parenthesis.'
            else:
                if not prev_is_var:
                    return "Invalid Expression!"
                prev_is_var = False
                if (len(stack) == 0 or
                        self.__preceed[char] > self.__preceed[stack[-1]]):
                    stack.append(char)
                elif self.__preceed[char] == self.__preceed[stack[-1]]:
                    res.append(stack[-1])
                    stack[-1] = char
                else:
                    index = len(stack) - 1
                    while (index >= 0 and self.__preceed[stack[index]] >
                            self.__preceed[char]):
                        res.append(stack[index])
                        index -= 1
                    stack = stack[:index + 1]
                    stack.append(char)
        if char in self.__preceed:
            return 'Invalid Expression!'
        for char in stack[::-1]:
            if char == '(':
                return 'Not Matching Parenthesis.'
            res.append(char)

        ex = ' '.join(res)
        return ex

    def calculate(self, postfix):
        postfix = re.split(' +', postfix)
        operands = []
        for op in postfix:
            try:
                num = float(op)
                operands.append(num)
            except ValueError:
                if op in self.__preceed and len(operands) > 1 and op != '(':
                    last_index = len(operands) - 1
                    if op == '^':
                        ctr = operands[last_index]
                        res = operands[last_index - 1]
                        while ctr > 1:
                            res *= operands[last_index - 1]
                            ctr -= 1
                    else:
                        res = eval(str(operands[last_index - 1]) +
                                   op + str(operands[last_index]))
                    operands = operands[:last_index-1]
                    operands.append(res)
                else:
                    return "Invalid expression!"
        if len(operands) > 1:
            return "Invalid expression!"
        return operands[0]


a = PostFix()

s = raw_input('Enter the infix expression: ')
print a.convert(s)
s = raw_input('Enter the postfix expression: ')
print a.calculate(s)
