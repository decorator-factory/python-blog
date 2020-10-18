($
  (p (it
    "This post is inspired by various interview question 'aggregates' like "
    (a "https://data-flair.training/blogs/top-python-interview-questions-answer/" "this one")
    "."))

  (horizontal-rule)
  ((h 2)
    "Q1. Is Python " (it "intepreted") " or " (it "compiled") "?")
  (p "TODO: Q1")

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
    "so many of them. First, there are obvious types like integerss, strings, "
    "lists, dicts, and so on. Then there are standard library types that are not "
    "built-in: stuff from " (mono "collections") ", " (mono "datetime") " etc. ")
  (p "Then there are datatypes which hide in plain sight: many people don't realize "
    "they are separate data types. For example, " (mono "range") " is not a function, "
    "it's a class " (--) " and calling it create a " (mono "range") " object, "
    "which is iterable, but not an iterator. " (mono "map") ", " (mono "filter")
    ", " (mono "itertools.groupby") ", " (mono "int/list/str/...") " are all "
    "classes as well.")
  (p "And don't forget that in Python, " (it "class") " is the same thing "
    "as " (it "type") ", so every time you define a class you create "
    "a new data type. So statements like " (it "'There are N data types"
    " in Python'") " are misleading. There can be as many types in Python as "
    "you want")


)