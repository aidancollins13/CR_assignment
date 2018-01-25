import ply.lex as lex
import sys

if(len(sys.argv) < 2):
    sys.exit("no file specified")

try:
    f = open(sys.argv[1], "r")
except:
    sys.exit("failed to open {0}".format(sys.argv[1]))

tokens = (
        'PN',
        'PROPERTY',
        'OPERATION',
        'COMPARATOR',
        'CONTEXT',
        'LPAREN',
        'RPAREN',
        'VALUE',
        )

t_OPERATION = r'@(count|lower|upper)'
t_COMPARATOR= r'(==|>=|<=|>|<|!=|matches|removed|(?:not )(has|in|contains|match))'
t_VALUE = r'[^\s-]+'

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_PN(t):
    r'P|N'
    return t

def t_PROPERTY(t):
    ' ([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)+)'
    return(t)

def t_CONTEXT(t):
    r'[a-z]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

lexer = lex.lex()

import ply.yacc as yacc

def p_pn(p):
    '''begin : PN expression'''
    p[0] = p[2]

def p_pn_error(p):
    '''begin : error expression
             | error VALUE
             | error CONTEXT
             | error COMPARATOR'''
    print("line doesn't start with P or N")

def p_property(p):
    '''expression : PROPERTY term'''
    p[0] = p[2]

def p_operation(p):
    '''expression : OPERATION LPAREN po RPAREN term'''
    p[0] = p[3]

def p_property_error(p):
    '''expression : error'''
    print('invalid operatoin or property', end=' ')

def p_po_operation(p):
    '''po : OPERATION LPAREN po  RPAREN'''
    p[0] = p[3]

def p_po_error(p):
    '''po : error'''
    print('invalid operation or property in operatoin', end=' ')


def p_po_property(p):
    '''po : PROPERTY'''
    p[0] = 'syntax ok'

def p_term(p):
    '''term : CONTEXT COMPARATOR term2
            | COMPARATOR term2 '''
    if(len(p) == 4):
        p[0] = p[3]
    else:
        p[0] = p[2]

def p_term_error(p):
    ''' term : CONTEXT error term2
            | error term2'''
    print("invalid comparator", end=' ')

def p_term2(p):
    '''term2 : VALUE
             | OPERATION LPAREN po RPAREN
             | PROPERTY
             | CONTEXT
             | VALUE term2
             | OPERATION LPAREN po RPAREN term2
             | PROPERTY term2
             | CONTEXT term2 '''
    p[0] = 'syntax ok'

def p_term2_error(p):
    '''term2 : error'''
    print("invalid syntax after comparator", end=' ')


def p_error(p):
    print("syntax error", end=' ')

parser = yacc.yacc()

for i,line in enumerate(f):
    print("Line: {}".format(i+1), end=' ')

    lexer.input(line)

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)

    result = parser.parse(line)
    if result:
        print(result)
    else:
        print('')

