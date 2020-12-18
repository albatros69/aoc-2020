#! /usr/bin/env python

import sys
import re

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

operators = ('+', '*', )

class Expression():
    operator=''
    right = None
    left = None

    def __init__(self, op, left, right):
        self.operator = op
        self.left = left
        self.right = right

    def eval(self):
        if self.left is None:
            raise ValueError
        elif isinstance(self.left, Expression):
            left = self.left.eval()
        else:
            left = int(self.left)
        if self.right is None:
            raise ValueError
        elif isinstance(self.right, Expression):
            right = self.right.eval()
        else:
            right = int(self.right)

        if self.operator=='+':
            return left + right
        elif self.operator=='*':
            return left * right

    def __repr__(self):
        if isinstance(self.left, Expression):
            left = "(%r)" % (self.left, )
        else:
            left = "%s" % (self.left, )
        if isinstance(self.right, Expression):
            right = "(%r)" % (self.right, )
        else:
            right = "%s" % (self.right, )
        return "%s %s %s" % (left, self.operator, right)

def read_int(text):
    if text == '':
        raise ValueError
    elif text[0].isdigit():
        i=0
        while i<len(text) and text[i].isdigit():
            i+=1
        return int(text[:i]), text[i:]
    else:
        raise SyntaxError("Unexpected caracter at "+ text)

# Part 1
def read_expr(text):
    if text == '':
        raise ValueError
    elif text[0] == ')':
        count=1; i=0
        while count>0:
            i+=1
            if i>=len(text):
                raise SyntaxError("Missing matching parenthesis "+str((text, i)))
            elif text[i]==')':
                count+=1
            elif text[i]=='(':
                count-=1
        return read(text[1:i]), text[i+1:]
    else:
        return read_int(text)

def read(text):
    if text == '':
        return None

    expr, rest = read_expr(text)
    if not rest:
        return expr
    else:
        return Expression(rest[0], expr, read(rest[1:]))

result = 0
for l in lines:
    # We need to read the expression from the right in order to get the evaluation order right
    expr = read(l.replace(' ', '')[::-1])
    # print(repr(expr))
    # print(f"{l} = {expr.eval()}")
    result += expr.eval()

print(result)

# Part 2
def read_expr(text):
    if text == '':
        raise ValueError
    else:
        fact, rest = read_factor(text)
        if rest=='':
            return fact, ''
        else:
            op = rest[0]
            if op=='*':
                expr, plop = read_expr(rest[1:])
                return Expression(op, fact, expr), plop
            else:
                return fact, rest

def read_factor(text):
    if text == '':
        raise ValueError
    else:
        term, rest = read_term(text)
        if rest=='':
            return term, ''
        else:
            op = rest[0]
            if op=='+':
                expr, plop = read_factor(rest[1:])
                return Expression(op, term, expr), plop
            else:
                return term, rest

def read_term(text):
    if text[0].isdigit():
        return read_int(text)
    elif text[0] == '(':
        count=1; i=0
        while count>0:
            i+=1
            if i>=len(text):
                raise SyntaxError("Missing matching parenthesis "+str((text, i)))
            elif text[i]=='(':
                count+=1
            elif text[i]==')':
                count-=1
        expr, _ = read_expr(text[1:i])
        return expr, text[i+1:]
    else:
        raise SyntaxError("Unexpected character at "+text)

result = 0
for l in lines:
    expr, _ = read_expr(l.replace(' ', ''))
    # print(repr(expr))
    # print(f"{l} = {expr.eval()}")
    result += expr.eval()

print(result)
