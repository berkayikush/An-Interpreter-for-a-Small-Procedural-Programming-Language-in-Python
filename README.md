# The Compact Programming Language

![Programming_Language-Python-blue](https://img.shields.io/badge/Programming_Language-Python-blue.svg)
![Python_Version-3.11.4-brown](https://img.shields.io/badge/Python_Version-3.11.4-brown.svg)
![Status-Complete-green](https://img.shields.io/badge/Status-Complete-green.svg)

## Overview

Compact is a small procedural programming language explicitly created to be interpreted by my interpreter.

It supports a range of fundamental programming concepts, including variable declaration,
order of operations, conditional statements, nested loops, nested functions, and recursion.

The syntax of Compact is designed to be easy to read and understand.

## Grammar

```text
program = statement_list ;

statement_list = statement, statement_list | empty_statement ;
statement = func_decl_statement | return_statement, SEMICOLON | var_decl_statement, SEMICOLON | for_statement
            | continue_statement, SEMICOLON | break_statement, SEMICOLON | while_loop_statement
            | conditional_statement | func_call, SEMICOLON | assignment_statement, SEMICOLON | empty_statement ;

func_decl_statement = K_FUNC, LEFT_PARENTHESIS, return_type, RIGHT_PARENTHESIS, IDENTIFIER,
                              LEFT_PARENTHESIS, [ func_params ], RIGHT_PARENTHESIS,
                              LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET ;
func_params = func_param, { COMMA, func_param } ;
func_param = K_VAR, LEFT_PARENTHESIS, var_type, RIGHT_PARENTHESIS, var_name, [ ASSIGN, logical_expr ] ;

return_statement = K_RETURN, [ logical_expr ] ;
return_type = K_INT | K_FLOAT | K_BOOL | K_STR | K_VOID ;

var_decl_statement = K_VAR, LEFT_PARENTHESIS, var_type, RIGHT_PARENTHESIS,
                     var_name, [ ASSIGN, logical_expr ], { COMMA, var_name, [ ASSIGN, logical_expr ] } ;
var_type = K_INT | K_FLOAT | K_BOOL | K_STR ;

for_statement = K_FOR, LEFT_PARENTHESIS, K_VAR, LEFT_PARENTHESIS, var_type, RIGHT_PARENTHESIS, var_name,
                K_FROM, ( logical_expr | range_expr ), RIGHT_PARENTHESIS,
                LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET ;

range_expr = logical_expr, K_TO, logical_expr, [ K_STEP, logical_expr ] ;

continue_statement = K_CONTINUE ;
break_statement = K_BREAK ;

while_statement = K_WHILE, LEFT_PARENTHESIS, logical_expr, RIGHT_PARENTHESIS,
                  LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET ;

conditional_statement = K_IF, LEFT_PARENTHESIS, logical_expr, RIGHT_PARENTHESIS, LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET,
                        { K_ELSEIF, LEFT_PARENTHESIS, logical_expr, RIGHT_PARENTHESIS, LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET },
                        [ K_ELSE, LEFT_CURLY_BRACKET, statement_list, RIGHT_CURLY_BRACKET ] ;

assignment_statement = ( var_name | accessor ), ( ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MULTIPLICATION_ASSIGN
                                                  | FLOAT_DIVISION_ASSIGN | INT_DIVISION_ASSIGN
                                                  | MODULO_ASSIGN ), logical_expr ;
empty_statement = ;

logical_expr = comparison_expr, { ( K_AND | K_OR ), comparison_expr } ;
comparison_expr = K_NOT, comparison_expr
                  | arithmetic_expr, { ( EQUALS | NOT_EQUALS | LESS_THAN | LESS_THAN_OR_EQUALS
                                         | GREATER_THAN | GREATER_THAN_OR_EQUALS ), arithmetic_expr } ;

arithmetic_expr = term, { ( PLUS | MINUS ), term } ;
term = factor, { ( MULTIPLICATION | INT_DIVISION | FLOAT_DIVISION | MODULO ), factor } ;

factor = ( INT | FLOAT | BOOL | STR )
         | LEFT_PARENTHESIS, logical_expr, RIGHT_PARENTHESIS
         | ( PLUS | MINUS ), factor
         | accessor
         | func_call
         | var_name ;

accessor = ( STR | var_name ), LEFT_SQUARE_BRACKET, logical_expr, [ COLON, logical_expr ], RIGHT_SQUARE_BRACKET ;
func_call = IDENTIFIER, LEFT_PARENTHESIS, [ logical_expr, { COMMA, logical_expr } ], RIGHT_PARENTHESIS ;
var_name = IDENTIFIER ;
```

## Examples

Check out the example programs in the examples folder.

```text
───────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: examples/factorial.co
───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ func(int) factorial(var(int) n = 0) {
   2   │     if (n == 0) {
   3   │         return 1;
   4   │     }
   5   │
   6   │     return n * factorial(n - 1);
   7   │ }
   8   │
   9   │ println(factorial(toint(input("Enter a number: "))));
───────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

```text
───────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: examples/check_num_occurances.co
───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ func(int) checkNumOccurances(var(str) word, var(str) charToCheck) {
   2   │     var(int) count = 0;
   3   │
   4   │     for (var(str) char from word) {
   5   │         if (char == charToCheck) {
   6   │             count += 1;
   7   │         }
   8   │     }
   9   │
  10   │     return count;
  11   │ }
  12   │
  13   │ println(checkNumOccurances("hello", "l")); /* 2 */
  14   │ println(checkNumOccurances("hello", "o")); /* 1 */
  15   │ println(checkNumOccurances("hello", "z")); /* 0 */
───────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

## Running the Project

```zsh
git clone https://github.com/berkaykush/Compact-Programming-Language-in-Python
cd Compact-Programming-Language-in-Python
python main.py examples/program_name.co
```

## Author

Berkay Kush
