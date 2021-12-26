import math
from utils.parsers import scan_lines


open_to_close_symbols = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

close_to_open_symbols = {close_symbol: open_symbol for open_symbol, close_symbol in open_to_close_symbols.items()}

error_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

auto_complete_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def solve1():
    syntax_errors = {symbol: 0 for symbol in close_to_open_symbols}
    for line in scan_lines("day10/input.txt"):
        symbols = []
        for symbol in line:
            if symbol in '([{<':
                symbols.append(symbol)
            if symbol in ')]}>' and symbols.pop() != close_to_open_symbols[symbol]:
                syntax_errors[symbol] += 1
                break
    syntax_score = 0
    for symbol, frequency in syntax_errors.items():
        syntax_score += error_scores[symbol] * frequency
    print(syntax_score)

def solve2():
    scores = []
    for line in scan_lines("day10/input.txt"):
        symbols = []
        for symbol in line:
            if symbol in '([{<':
                symbols.append(symbol)
            if symbol in ')]}>' and symbols.pop() != close_to_open_symbols[symbol]:
                break
        else:
            score = 0
            while symbols:
                score *= 5
                score += auto_complete_scores[open_to_close_symbols[symbols.pop()]]
            scores.append(score)
    scores.sort()
    print(scores[math.floor(len(scores) / 2)])
