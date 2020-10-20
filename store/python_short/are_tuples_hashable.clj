($
  (p
    "Some of them are. Some of them aren't.")
  (p
    "A tuple is hashable if all of its elements are hashable. "
    "For example, " (mono "hash((1, 2, 3))") " will succeed, while "
    (mono "hash(([1, 2], [3, 4]))") " will raise an exception.")
)