# ptilis.py

Simple python-based lisp-like code interpreter.

## Features

- Read and execute files.
- Really basic syntax correction
- Read–eval–print loop (REPL): execution line-by line from console
- Support for functions and recursivity
- Can import more "native" functions, and lets you create new ones if needed
- Basic (but incomplete) exception handling

## Basics

The syntax is heavily inspired by LISP (List processing).

Since its based on Python, the language is  dynamically-typed typed, with implicit casts.

The supported types right now are `integers`, `floats`, `strings`, and, most importantly `lists`. Lists can contain element of all types at the same time.

A `string` is declared by putting `"`quotes`"` around the text (Note that strings are always stripped).

A `list` is made of symbols separated by blank characters, all contained with parenthesis.

Examples of lists:

- `(this is a "List")`
- `(9 (list in list) 15 "foo")`

Another "type" is the `Symbol`, which are used to refer to variables and functions.

Everything has to be contained in a list.

Each statements is a list that has the following structure : ```(statement [argument_1] [...] [argument_n])```. For example to do the operation `5 + 4`, the correct syntax would be ```(+ 5 4)```

To create a new variable, you have to use ```(define varName [value])```, to change the value later, you can use ```(set varName newValue)```.

To declare a new function, use ```(defun functionName argumentList body)```.

Comments start with `;` and end with a new line

### Environnements

What i call an "`Environement`" is a collection of `symbols` (aka functions and variables). Each environement inherits from a parent environement, except for the default environement, which contains global variables and built-in functions.

Each statement is executed in the context of the current environement, and `symbols` are resolved in the current environement first, then recursively in the parents environement until a matching symbol is found.

New environements are created:

- When calling a function, in which case the parent environement is the environement in which the function was declared
- Inside conditions
- At each iteration of any loop.
- At the beginning of a `for` loop, to contain the iterator
- When using the `(load new envName [...])` and `(load file envName "Filename" [...])` statements.

### Load

The `load` symbol is used to change the current environement, and sets the old environement as parent of the new one. It's syntax is `(load envName ([code]))`. The new environement is only applied within this list, and we return to the parent environement at the end.

`load` can only access environnements added to the list of accessible environnements, which can contain user defined environement as well as the "built-in" ones.

There are two variants if this symbol, which i presented earlyer: `load new` and `load file`.

The first one creates a new environement, and adds it to the list of accessible environnements.

`(load file envName "Filename" [...])` does the same, but also executes the code contained in the file called `Filename`, within the new environement, using the current environement as parent.

***I recommend checking out the examples in the `demo` folder.***

## Usage

  To execute a script file, call the function `parseAndRunFile()` with the relative path to your script as first argument. You can also run from a python string using `parseAndRunString()`.
  
  You can start the Read–eval–print loop by calling the `REPL()` function, or simply by executing `ptilis.py` as your main file.

  To add new natives functions, you can either edit the files in the `env` folder, or create a new one with a similar syntax, import the file in `DefaultEnvs.py`, and add it to the `EnvList` dictionnary.
