from plyplus import Grammar, STransformer

json_grammar = Grammar(r"""
@start: value ;

?value : object | array | string | number | boolean | null ;
?comment : one_line_comment | mulitline_comment ;

string : '".*?(?<!\\)(\\\\)*?"' ;
number : '-?([1-9]\d*|\d)(\.\d+)?([eE][+-]?\d+)?' ;
pair : ( comment )* string ':' value ( comment )* ;
object : ( comment )* '\{' ( comment )* ( pair ( comment )* ( ',' ( comment )* pair ( comment )* )* )? ( comment )* '\}' ( comment )* ;
array : ( comment )* '\[' ( comment )* ( value ( comment )* ( ',' ( comment )* value ( comment )* )* )? ( comment )* '\]' ( comment )* ;
boolean : 'true' | 'false' ;
null : 'null' ;

one_line_comment : '//.*\n';
mulitline_comment: '/\*(.|\n)*?\*/';

WS: '[ \t\n]+' (%ignore) (%newline);
""")


# ***** Mniej produkcji, ale problem z rekursja: *****

# json_grammar = Grammar(r"""
# @start: supervalue ;
#
# ?supervalue : comment supervalue | supervalue comment | value;
# value : object | array | string | number | boolean | null ;
# ?comment : one_line_comment | mulitline_comment ;
#
# string : '".*?(?<!\\)(\\\\)*?"' ;
# number : '-?([1-9]\d*|\d)(\.\d+)?([eE][+-]?\d+)?' ;
# pair : ( comment )* string ':' supervalue ( comment )* ;
# object : '\{' ( pair ( ',' pair )* )? '\}' ;
# array : '\[' ( supervalue ( ',' supervalue ) * )? '\]' ;
# boolean : 'true' | 'false' ;
# null : 'null' ;
#
# one_line_comment : '//.*\n';
# mulitline_comment: '/\*(.|\n)*?\*/';
#
# WS: '[ \t\n]+' (%ignore) (%newline);
# """)



class JSON_Transformer(STransformer):
    """Transforms JSON AST into Python native objects."""
    number = lambda self, node: float(node.tail[0])
    string = lambda self, node: node.tail[0][1:-1]
    boolean = lambda self, node: True if node.tail[0] == 'true' else False
    null = lambda self, node: None
    array = lambda self, node: node.tail
    pair = lambda self, node: {node.tail[0]: node.tail[1]}
    one_line_comment = lambda self, node: node.tail[0][2:-1]
    mulitline_comment = lambda self, node: node.tail[0][2:-2].replace('\t', '')
    value = lambda self, node: node.tail[0]
    supervalue = lambda self, node: node.tail
    object = lambda self, node: node.tail


def json_parse(json_string):
    """Parses a JSON string into native Python objects."""
    return JSON_Transformer().transform(json_grammar.parse(json_string))


def main():
    json = open('../a.json', 'r').read()
    print '### JSON Parser using PlyPlus'
    print '  # JSON allows empty arrays and objects.'
    print '  # This requires that empty AST sub-trees be kept in the AST tree.'
    print '  # If you pass the kwarg "keep_empty_trees=False" to the'
    print '  # Grammar() constructor, empty arrays and objects will be removed'
    print '  # and the JSON_Transformer class will fail.'
    print
    print '### Input'
    print json
    print '### Output'
    result = json_parse(json)
    import pprint
    pprint.pprint(result)


if __name__ == '__main__':
    main()
