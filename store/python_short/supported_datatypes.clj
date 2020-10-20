($
  (p "All of them!")
  (p
    "Seriously, though, this is a vague question. You probably cannot
    hold all the built-in data types in your head because there are just
    so many of them. Firstly, there are obvious types like integers, strings,
    lists, dicts, and so on. Then there are other standard library types:
    stuff from " (mono "collections") ", " (mono "datetime") " etc. ")
  (p
    "Then there are datatypes which hide in plain sight: many people don't realize
    they are separate data types. For example, " (mono "range") " is not a function,
    it's a class " (--) " and calling it creates a " (mono "range") " object,
    which is iterable, but not an iterator. " ((sepmap ", " mono) "map" "filter" "int/list/str")
    " are all classes as well " (--) " not functions.")
  (p
    "And don't forget that in Python, " (it "class") " is the same thing
    as " (it "type") ", so every time you define a class you create
    a new data type. So statements like " (it "'There are N data types
     in Python'") " are misleading. There can be as many types in Python as
    you want.")
)