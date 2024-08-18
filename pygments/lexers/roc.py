"""
    pygments.lexers.roc
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the Roc programming language.

    :copyright: Copyright 2006-2024 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, include, bygroups, using, this, \
    default
from pygments.token import Comment, Keyword, Name, Number, Punctuation, \
    String, Whitespace, Text

__all__ = ['RocLexer']


class RocLexer(RegexLexer):
    """
    For Roc source code.
    """

    name = 'Roc'
    url = 'https://roc-lang.org/'
    aliases = ['roc']
    filenames = ['*.roc']
    mimetypes = ['text/x-roc']
    version_added = '2.1'

    validName = r'[a-z_][a-zA-Z0-9_\']*'

    specialName = r'^main '

    builtinOps = (
        '%', '^', '!', '!=', '/', '//', '|>', '>', '>=', '-', '<', '<=', '==',
        '||', '*', '+', '&&'
    )

    punctuation = (
        '=', '\\', '->', '<-', ':=', ':', '&', '?'
    )

    reservedWords = words((
        'as', 'crash', 'dbg', 'else', 'expect', 'expect-fx', 'if', 'import',
        'imports', 'is', 'then', 'when', 'app', 'exposes', 'exposing', 'generates',
        'implements', 'module', 'package', 'packages', 'platform', 'requires',
        'where', 'with', 'provides', 'interface', 'hosted', 'to', '_'
    ), suffix=r'\b(?!:)')

    tokens = {
        'root': [

            # Comments
            (r'#.*', Comment.Single),

            # Whitespace
            (r'\s+', Whitespace),

            # Strings
            (r'"', String, 'doublequote'),

            # Modules
            (r'^(\s*)(module)(\s*)', bygroups(Whitespace, Keyword.Namespace,
                Whitespace), 'imports'),

            # Imports
            (r'^(\s*)(import)(\s*)', bygroups(Whitespace, Keyword.Namespace,
                Whitespace), 'imports'),

            # Keywords
            (reservedWords, Keyword.Reserved),

            # Types
            (r'@?[A-Z][a-zA-Z0-9_]*', Keyword.Type),

            # Main
            (specialName, Keyword.Reserved),
            (words(punctuation), Punctuation),
            # Prefix Operators
            (words((builtinOps), prefix=r'\(', suffix=r'\)'), Name.Function),

            # Infix Operators
            (words(builtinOps), Name.Function),

            # Numbers
            include('numbers'),

            # Variable Names
            (validName, Name.Variable),

            # Parens
            (r'[,()\[\]{}]', Punctuation),
        ],

        'doublequote': [
            (r'(\$\()(.*?)(\))',
             bygroups(String.Interpol, using(this), String.Interpol)),
            (r'\\u[0-9a-fA-F]{4}', String.Escape),
            (r'\\[nrfvb\\"]', String.Escape),
            (r'[^"]', String),
            (r'"', String, '#pop'),
        ],

        'imports': [
            (r'\w+(\.\w+)*', Name.Class, '#pop'),
        ],

        'numbers': [
            (r'_?\d+\.(?=\d+)(f(32|64))?', Number.Float),
            (r'_?\d+', Number.Integer, 'int_lit'),
        ],
        'int_lit': [
            (r'[ui](8|16|32|64|128)', Number.Integer, '#pop'),
            (r'dec', Number.Integer, '#pop'),
            default('#pop'),
        ],
    }
