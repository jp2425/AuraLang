# VibeLang

VibeLang is a small interpreted language built on top of Python and Lark.  
It focuses on simple structure, readable syntax, and predictable behavior.

The language is designed to be easy to understand, easy to extend, and useful for experimenting with parsing and runtime execution.

## Overview

VibeLang includes:

- A custom grammar defined with Lark
- A transformer that converts parse trees into a clean AST
- A runtime interpreter that executes programs
- A small standard library for common operations

The goal is to keep things minimal while still expressive enough to build non-trivial programs.

## Core Ideas

- Clear and explicit syntax for assignments and control flow
- Simple data types: numbers (NUMBERS), strings (LETTERS), booleans (VIBE), lists (SQUAD), and json (JASON)
- Boolean values are written as `real` and `fake`
- Built-in operations cover common needs without adding unnecessary complexity

## Language Features

- Variable declaration with `MOOD`
- Assignment with `IS_GIVING`
- Conditionals using `VIBE_CHECK`, `SLAY`, and `FLOP`
- Loops using `COOK_FOR`
- Function calls with arguments
- Structured data like lists and objects

## Standard Library

The built-in functions provide support for:

- Working with collections (e.g. size and indexing)
- Type conversion
- String and template formatting
- Basic value inspection
- Output

## Project Structure

The project is organized into several main parts:

- grammar: language definition
- parsing: parser, AST nodes, and transformers
- interpreter: runtime execution
- lib: standard library functions
- runtime: formatting and helpers

## Running Programs

Programs are executed as following

```
pip install .
aura path_to_program.vibe inputkey=value1 inputkey2=value2 ...
```

Additional arguments can be passed and used as inputs within the program.

## Language Syntax

VibeLang uses a clear and structured syntax that follows a consistent pattern across all constructs. The goal is to keep programs easy to read and reason about.

### Variables and Assignment

Variables are declared using `MOOD` and assigned with `IS_GIVING`.

A variable can also be reassigned without `MOOD`.

MOOD number IS_GIVING 10  
number IS_GIVING number PLUS 5  

### Data Types

VibeLang supports a small set of core types:

- Numbers (e.g. 10, 3.14)
- Strings (e.g. "hello")
- Booleans (`real`, `fake`)
- Lists (e.g. [1, 2, 3])
- Objects (e.g. {"name":"alice"})

### Booleans

Boolean values are written as:

- real (true)
- fake (false)

They are used in conditions and logical expressions.

### Arithmetic

Basic arithmetic operations are supported:

number PLUS 5  
number MINUS 2  
number TIMES 3  
number DIVIDED 2  

### Comparisons

Comparisons are written using keywords:

number ME_TOO 10  
number BIG 5  
number SMALL 20  

### Logical Expressions

Logical operations include:

- REKT (negation)
- AND
- OR

Examples:

REKT fake  
real AND fake  
real OR fake  

### Conditionals

Conditional execution uses `VIBE_CHECK`, with `SLAY` and optional `FLOP` blocks:

VIBE_CHECK(condition)  
SLAY  
{  
    // code if true  
}  
FLOP  
{  
    // code if false  
}  

### Loops

Loops are defined using `COOK_FOR`:

COOK_FOR(count, i)  
    // loop body  
CHEFF_KISS  

The loop runs `count` times, using `i` as the iteration variable.

### Functions

Functions are called using standard call syntax:

SIZE(list)  
SPILL(list, index)  
SCREAM("hello")  

Arguments can be variables, literals, or other function calls.

### Output and Return

- `SCREAM(...)` prints values  
- `DROP(value)` returns a value and ends execution  

Example:

SCREAM("processing...")  
DROP result  

### Structure

A program starts with an `AURA` declaration defining its inputs:

AURA X, Y  

Followed by a sequence of commands executed in order.

---

## Notes

VibeLang is an evolving project focused on language design and execution models.  
The implementation is intentionally kept straightforward to make experimentation and modification easy.

> **DO NOT USE THIS IN PRODUCTION**