"""Retain reported lower bounds separately from independently verified bounds.

The closed-form evaluator computes a conservative rational value of the
published formula. Evaluating the formula does not replay its covering proof.
"""
from fractions import Fraction
import ast
import math
import re


def approximation(expression):
    """Evaluate the register's displayed arithmetic without evaluating Python."""
    expression = expression.strip('`')
    root = re.fullmatch(r'root\([^,]+,\s*([0-9.]+)\)', expression)
    if root:
        return float(root[1])
    text = re.sub(r'√(\d+)', r'sqrt(\1)', expression)
    text = re.sub(r'(?<=[\d)])\s*sqrt', '*sqrt', text)

    def read(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp):
            left, right = read(node.left), read(node.right)
            operations = {ast.Add: lambda: left+right, ast.Sub: lambda: left-right,
                          ast.Mult: lambda: left*right, ast.Div: lambda: left/right,
                          ast.Pow: lambda: left**right}
            if type(node.op) in operations:
                return operations[type(node.op)]()
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -read(node.operand)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in ('sqrt', 'floor') and len(node.args) == 1 and not node.keywords):
            return {'sqrt': math.sqrt, 'floor': math.floor}[node.func.id](read(node.args[0]))
        raise ValueError(f'Unsupported bound expression: {expression}')

    return float(read(ast.parse(text, mode='eval').body))


def closed_form(n, intervals, places=30):
    """A rational lower approximation to the source's claimed a(n), or None."""
    if n < 49 or math.isqrt(n)**2 == n:
        return None
    k = math.isqrt(n)
    scale = 10**places
    choices = []
    for item in intervals:
        alpha = Fraction(item['alpha'])
        beta = Fraction(item['beta'])
        d0, d1 = Fraction(item['d0']), Fraction(item['d1'])
        radicand = 4*alpha*alpha+n+4*beta-4*alpha*k
        if radicand < 0:
            continue
        threshold = k+d0-2*alpha
        if threshold >= 0 and radicand <= threshold*threshold:
            continue
        root = Fraction(math.isqrt(radicand.numerator*scale*scale//radicand.denominator), scale)
        bound = min(2*alpha+root, k+d1)
        choices.append((bound, item['index']))
    return max(choices) if choices else None


def rational_floor(value, places=12):
    scale = 10**places
    q = Fraction(value)*scale
    floor = q.numerator//q.denominator
    return f'{floor//scale}.{floor%scale:0{places}d}'
