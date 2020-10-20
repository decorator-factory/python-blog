($
  (p
    "Most of the times, a decorator returns something callable. It can be
    a function, and sometimes it's a custom callable object (as it is
    with " ((sepmap ", " mono) "property" "staticmethod" "classmethod")
    ", for example.")
  (p
    "But it doesn't have to: a decorator can return whatever you want.")
  (pre """
    >>> def name_length(fn):
    ...     return len(fn.__name__)
    ...
    >>> @name_length
    ... def my_function():
    ...     pass
    ...
    >>> my_function
    12
    >>>
    """
  )
)