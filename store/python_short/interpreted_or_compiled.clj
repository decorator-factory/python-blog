($
  (p
    "Can you compile Python to machine code? Yes, you can use Nuitka for that.
    Does it have a JIT compiler? Yes, it's called PyPy.")
  (p
    "The most widely used and supported Python implementation is "
    (it "CPython") ". CPython executes a program by first compiling it
    into bytecode and then executing the bytecode. This is the model used
    in other languages, like JavaScript, Lua, Java, C#.")
  (p
    "Some languages are usually compiled all the way to machine code, like
    C, C++, Rust, Go, Haskell. Some languages can be compiled to
    machine code but can also be ran as bytecode, for example,
    Haskell can also target the JVM.")
  (p
    (it "Compiled") " and " (it "interpreted") " are poorly defined
    and inconsistently applied (i.e. Java is 'compiled' while Python
    is 'interpreted', even though they both compile to bytecode).
    Besides, a single language can have multiple implementations that
    have different execution models. It's much more useful to elaborate
    and discuss"
    (list-unordered
      "how execution speed differs between langauges"
      "how a particular implementation of a language works"
      "how memory models differ between languages and implementation"
      "how type systems differ between languages"))
  (horizontal-rule)
  (p
    "Another common misconception is that Python, JavaScript, Ruby or other
    'interpreted' languages are interpreted directly from source code,
    line-by-line. This is simply not true, and websites like "
    (a "https://www.interviewbit.com/python-interview-questions/" "this one")
    " should stop saying that.")
)