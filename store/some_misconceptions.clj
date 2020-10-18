($
  (p (it
    "This post is inspired by various interview question 'aggregates' like "
    (a "https://data-flair.training/blogs/top-python-interview-questions-answer/" "this one")
    "."))

  (horizontal-rule)
  ((h 2)
    "Q1. Is Python " (it "intepreted") " or " (it "compiled") "?")
  (p "Can you compile Python to machine code? "
    "Yes, you can use Nuitka for that. Does it have a JIT compiler? "
    "Yes, it's called PyPy.")
  (p "The most widely used and supported Python implementation is "
    (it "CPython") ". CPython executes a program by first compiling it "
    "into bytecode and then executing the bytecode. This is the model used "
    "in other languages, like JavaScript, Lua, Java, C#.")
  (p "Some languages are usually compiled all the way to machine code, like "
    "C, C++, Rust, Go, Haskell. Some languages can be compiled to "
    "machine code but can also be ran as bytecode, for example, "
    "Haskell can also target the JVM.")
  (p (it "Compiled") " and " (it "interpreted") " are poorly defined "
    "and inconsistently applied (i.e. Java is 'compiled' while Python "
    "is 'interpreted', even though they both compile to bytecode). "
    "Besides, a single language can have multiple implementations that "
    "have different execution models. It's much more useful to elaborate "
    "and discuss"
    (list-unordered
      "how execution speed differs between langauges"
      "how a particular implementation of a language works"
      "how memory models differ between languages and implementation"
      "how type systems differ between languages"))
  (horizontal-rule)
  (p "Some resources get it wrong even worse. For example, "
    (a "https://www.interviewbit.com/python-interview-questions/" "this website")
    " claims that: " (it "An Interpreted language executes its statements line by line. "
    "Languages such as Python, Javascript, R, PHP and Ruby are prime examples of "
    "Interpreted languages. Programs written in an interpreted language runs directly "
    "from the source code, with no intermediary compilation step."))

  (horizontal-rule)
  ((h 2)
    "Q2. Are tuples hashable?")
  (p "Some of them are. Some of them aren't.")
  (p "A tuple is hashable if all of its elements are hashable. "
     "For example, " (mono "hash((1, 2, 3))") " will succeed, while "
     (mono "hash(([1, 2], [3, 4]))") " will raise an exception.")

  (horizontal-rule)
  ((h 2)
    "Q3. How do you check if a stirng only contains digits "
    "(for example, if you want to convert a string into an integer)?")
  (p (mono "str.isdigit") " might seem an obvious choice, but there's "
    "a catch: it will also accept special digit characters like ². The "
    "right method to use here is " (mono "str.isdecimal"))

  (horizontal-rule)
  ((h 2)
    "Q4. What operations do " (mono "<, >, <=, >=") " stand for?")
  (p "Those operations help determine ordering: whether one element "
    "comes before or after another. Unlike some languages, like Python 2 and "
    "JavaScript, comparing two uncomparable values (for example, a number "
    "and a string) will raise an exception. Strings, lists, and tuples "
    "are compared lexicographically.")
  (p "There is also an unexpected usage of those operators in the standard "
    "library: when used on sets, they act as "
    (e "sub") ", " (e "sup") ", " (e "sube") ", " (e "supe") ".")

  (horizontal-rule)
  ((h 2)
    "Q5. What data types does Python support?")
  (p "All of them!")
  (p "Seriously, though, this is a vague question. You probably cannot "
    "hold all the built-in data types in your head because there are just "
    "so many of them. Firstly, there are obvious types like integers, strings, "
    "lists, dicts, and so on. Then there are other standard library types: "
    "stuff from " (mono "collections") ", " (mono "datetime") " etc. ")
  (p "Then there are datatypes which hide in plain sight: many people don't realize "
    "they are separate data types. For example, " (mono "range") " is not a function, "
    "it's a class " (--) " and calling it creates a " (mono "range") " object, "
    "which is iterable, but not an iterator. " (mono "map") ", " (mono "filter")
    ", " (mono "int/list/str/...") " are all classes as well " (--) " not functions.")
  (p "And don't forget that in Python, " (it "class") " is the same thing "
    "as " (it "type") ", so every time you define a class you create "
    "a new data type. So statements like " (it "'There are N data types"
    " in Python'") " are misleading. There can be as many types in Python as "
    "you want.")


  (horizontal-rule)
  ((h 2)
    "Q6. What does a decorator return?")
  (p "Most of the times, a decorator returns something callable. It can be "
    "a function, and sometimes it's a custom callable object (as it is "
    "with " (mono "property") ", " (mono "staticmethod") ", "
    (mono "classmethod") ", for example.")
  (p "But it doesn't have to: a decorator can return whatever you want.")
  (pre
    ">>> def name_length(fn):"
    "...     return len(fn.__name__)"
    "..."
    ">>> @name_length"
    "... def my_function():"
    "...     pass"
    "..."
    ">>> my_function"
    "12"
    ">>>"
  )

  (horizontal-rule)
  ((h 2)
    "Q7. What is " (mono "self") " in Python?")
  (p (mono "self") (it " is a keyword that...") " No, " (mono "self") " is not "
    "a keyword " (--) " it's just a convention to use " (mono "self") "as the name "
    "of the first parameter in methods. A " (it "keyword") " is a reserved word "
    "that has a special meaning for the parser, like " (mono "if") " or " (mono "import") ". ")

  (horizontal-rule)
  ((h 2)
    "Q8. What does the " (mono "__init__") " method do?")
  (p "The " (mono "__init__") " method does not create an obejct and "
    (it "definitely") " doesn't allocate any memory. This method get called "
    "after the object has already been created.")

  (horizontal-rule)
  ((h 2)
    "Q9. What is ")

)