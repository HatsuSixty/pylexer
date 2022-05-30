import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import *

class TokenKind(Enum):
    WORD=auto()
    INT=auto()
    SEMICOLON=auto()
    OPENPAREN=auto()
    CLOSEPAREN=auto()
    COMMA=auto()
    SPACE=auto()

@dataclass
class TokenValue:
    string:  str
    integer: int

@dataclass
class Token:
    kind:  TokenKind
    value: TokenValue

@dataclass
class Lexer:
    tokens: List[Token]
    token:  Token
    string: str
    attok:  int
    atstr:  int

def lexer_lex_line(lexer: Lexer, line: str) -> Lexer:
    lexer.string = line
    return lexer

def lexer_new() -> Lexer:
    return Lexer(
        [],
        Token(TokenKind.WORD, TokenValue("", 0)),
        "",
        0,
        0
    )

def isspecial(lexer: Lexer) -> bool:
    return handle_special(lexer, False)

def handle_special(lexer: Lexer, advance: bool) -> bool:
    if lexer.string[lexer.atstr] == ';':
        lexer.token = Token(TokenKind.SEMICOLON, TokenValue(';', 0))
        if advance: lexer.atstr += 1
    elif lexer.string[lexer.atstr] == '(':
        lexer.token = Token(TokenKind.OPENPAREN, TokenValue('(', 0))
        if advance: lexer.atstr += 1
    elif lexer.string[lexer.atstr] == ')':
        lexer.token = Token(TokenKind.CLOSEPAREN, TokenValue(')', 0))
        if advance: lexer.atstr += 1
    elif lexer.string[lexer.atstr] == ',':
        lexer.token = Token(TokenKind.COMMA, TokenValue(',', 0))
        if advance: lexer.atstr += 1
    elif lexer.string[lexer.atstr].isspace():
        lexer.token = Token(TokenKind.SPACE, TokenValue(' ', 0))
        if advance: lexer.atstr += 1
    else:
        return False
    return True

def lexer_next_token(lexer: Lexer) -> Lexer:
    assert lexer.atstr < len(lexer.string)

    string = ""
    if handle_special(lexer, True):
        lexer.attok += 1
        lexer.tokens.append(lexer.token)
        return lexer
    else:
        while not isspecial(lexer):
            if isspecial(lexer):
                break
            string += lexer.string[lexer.atstr]
            lexer.atstr += 1
    lexer.token = Token(TokenKind.WORD, TokenValue(string, 0))
    lexer.attok += 1
    lexer.tokens.append(lexer.token)
    return lexer

def main():
    lexer = lexer_new()
    lexer = lexer_lex_line(lexer, "write(hababa,      abcba,    dwaiudhwaiu c, uhdawi);")
    while lexer.attok < 100:
        lexer = lexer_next_token(lexer)
        print(lexer.token.value.string)

if __name__ == '__main__':
    main()
