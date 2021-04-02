# ptilis.py

Simple python-based lisp-like code interpreter.

## Features

- Read and execute files.
- Really basic syntax correction
- Read–eval–print loop (REPL): execution line-by line from console
- Support for functions and recursivity
- Can import more "native" functions, and you create new ones if needed
- Basic (but incomplete) exception handling

## Basics

The syntax is heavily inspired by LISP (List processing).

Since its based on Python, the language is  dynamically-typed typed, with implicit casts.

The supported types right now are `integers`, `floats`, `strings`, and, most importantly `lists`. Lists can contain element of all types at the same time.

A `string` is declared by putting `"`quotes`"` around the text (Note that strings are always stripped).

A `list` is made of symbols separated by blank characters, all contained with parenthesis.

Examples of lists:
- `(this is a "List")`
- `(9 (list in list ) 15 "foo")`

Another "type" is the `Symbol`, which are used to refer to variables and functions.

Everything has to be contained in a list.

Each statements is a list that has the following structure : ```(statement [argument1] [...] [argumentn])```. For example to do the operation `5 + 4`, the correct syntax would be ```(+ 5 4)```

To create a new variable, you have to use ```(define varName [value])```, to change the value later, you can use ```(set varName newValue)```.

To declare a new function, use ```(defun functionName argumentList body)```.

I recommend checking out the examples in the `demo` folder.

## Usage

  To execute a script file, call the function `parseAndRunFile()` with the relative path to your script as first argument. You can also run from a python string using `parseAndRunString()`.
  
  You can start the Read–eval–print loop by calling the `REPL()` function, or simply by executing `ptilis.py` as your main file.

  To add new natives functions, you can either edit the files in the `env` folder, or create a new one with a simillar syntax, import the file in `DefaultEnvs.py`, and add it to the `EnvList` dictionnary.
