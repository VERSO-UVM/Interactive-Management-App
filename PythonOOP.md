# OOP Python Guide #

## Classes ##

Classes do all of the following:

1. They all have the same data fields
2. They all have the same functions to operate on those data fields

### Writing a class ###

```
class Category():   # Arguments in the () mean Category inherits from another class
                    # That means another class calls its own __init__(self, ...) with the
                    # arguments in this class's arguments, and this class can access the data
                    # and functions in the parent. Try not to use inheritance

    # declare a variable inside Category but before __init__(self, ...) to make a static member
    # static means there can be a million instances of Category with unique data in their fields,
    # but only one copy of the static member exists in memory and every instance of Category shares it.
    # You can't combine self (meaning this specific Category) with something static if it changes the data
    # in the specific Category
    DEFAULT_DESCRIPTION = "Type here to enter a description of this idea!"  # <= Static variable

    def __init__(self,
                 name: str,
                 id: int # You can use `variable: type` to tell someone what type the argument should be)

        # self means this instance of the class. There can be a million instances of Category,
        but each one has its own values stored in the member fields of a particular instance (like name)

        # Initialize data fields for this class instance here, like this:
        self.name = name # name comes from the arguments in the class's __init__(self, ...) method
        self.__ID = id   # Use two __ to make a variable private. Private means only the class can access it
                         # In Python it is just a suggestion. There is no actual private-public concept.
        self.__IDEA      # Use SNAKE_CASE to make a variable constant (const in C++, final in Java, etc...)
                         # There is no real concept of const in Python. It is also just a suggestion
        

        # Define a function inside the class with `self` as the first argument to make a member function
        # You can then use `self` inside the method to access this particular Category's member fields
        def set_name(self, name) -> None:   # Use an arrow to a type ` -> type: ` to indicate the return type
            self.name = name
        

        def __repr__(self):                      # __repr__ is like toString() in Java. You can build a string
            return "Category name: " + self.name # that gets printed if you print this particular
                                                 # instance of Category: print(category1)
```
