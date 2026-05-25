# Notes - Week 1 Readings

## mypy

The mypy module in Python makes use of what's known as typing annotations - these are bits of information that tell the interpreter what datatype a variable/function return value is going to be. Python doesn't care for these annotations, and runs the code irrespective of the datatype assigned to the variable, but mypy checks these annotations before runtime to ensure that the right datatype has been assigned to a variable with a certain type annotation.

### Variables + Useful built-in Types

```python
# For assigning type annotations to variables, we do variable_name: type = value (not necessary to include value when assigning)
a: int = 8
f: float = 3.1415
s: str = "Hello!"
b: bool = True


# For assigning annotations to iterables, we do iterable_name: iterable_type[datatypes used] = value (optional)
l: list[str]
d: dict[str, int] = {"Alex": 9, "John": 13}         # 1st parameter inside [] = key type, 2nd parameter = value type              
t: tuple[str, int, bool] = ("Max", 21, True)        # only used for tuples of definite size, to define each value inside it
t2: tuple[int, ...] = (1, 2)                        # for variable tuples, we do datatype followed by ... (ellipsis)

# We can also use functions like | or Union and Optional[X] or X | None in cases of uncertainty
l: list[str | int] = []                             # use | or Union for iterables with > 1 datatype (from typing library)
x: str | None = "hi!" if fulfilled() else None      # use A | None for a value that could evaluate to None (one-line conditional)
assert x is not None                                # use assert if x is guaranteed to not be None
```

We can also inplement type annotating in functions, both in the function parameters and the return value.

```python
# The syntax for implementing type annotation in functions is def f_name(v1: type, v2: type, ...) -> return_type:

def add(a: str, b: str) -> str:
    return a + b

def subtract(a: int, b: int = 0) -> None;           # give None as the return value if no value is being returned
    print(a - b)                                    # if default arguments to be specified, write them as v_name: type = default_value
```

Note that non-annotated arguments are treated as an `Any` variable, and that functions without any annotations aren't checked by mypy.

Apart from just basic function usage, type annotation can also be implemented in the same way for `callable` and `iterator` functions as well. Furthermore, mypy can also understand positional-only and keyword-only arguments that have been type annotated.

### Classes

Type annotation can also be implemented in classes. Apart from the `self` parameter for internal class functions, every other parameter passed to any class function can be type annotated, and so can the return value. User-defined classes are also recognized as valid types in type annotations. One can also use the inheritance properties of parent classes to apply type annotation to child classes. 

```python
class BankAccount:
    def __init__(self, account_name: str, initial_balance: int = 0) -> None:
        self.account_name = account_name
        self.balance = initial_balance
    def deposit(self, amount: int) -> None:
        self.balance += amount
    def withdraw(self, amount: int) -> None:
        self.balance -= amount

account: BankAccount = BankAccount("Alice", 400)
def transfer(src: BankAccount, dst: BankAccount, amount: int) -> None:
    src.withdraw(amount)
    dst.deposit(amount)

# Functions accepting any class can also accept its subclasses
class AuditedBankAccount(BankAccount):
    audit_log: list[str]
    def __init__(self, account_name: str, initial_balance: int = 0) -> None:
        super().__init__(account_name, initial_balance)
        self.audit_log: list[str] = []
    def deposit(self, amount: int) -> None:
        self.audit_log.append(f"Deposited {amount}")
        self.balance += amount
    def withdraw(self, amount: int) -> None:
        self.audit_log.append(f"Withdrew {amount}")
        self.balance -= amount
audited = AuditedBankAccount("Bob", 300)
transfer(audited, account, 100)
```

One can use the `ClassVar[type]` variable to declare class variables, and implement overrides on `__setattr__` or `__getattr__` functions for dynamic attributes.

```python 
from typing import ClassVar

class Car:
    seats: ClassVar[int] = 4
    passengers: ClassVar[list[str]]
```

### Duck Typing

In Python, many functions don't actually need a specific type like `list` or `dict` — they just need something that "behaves" like one. This concept is called "duck typing". mypy standardises common duck types through the `collections.abc` module. You can also define your own duck types if there isn't a data structure that fits your requirements.

The two most useful ones are `Iterable` (used in "for" loops) and `Sequence` (for loops + indexing + usage of len()). For dict-like objects, `Mapping` is used primarily for reading purposes (immutable), and `MutableMapping` for writing as well (mutable)

```python
from collections.abc import Mapping, MutableMapping

def read_only(m: Mapping[str, int]) -> list[int]:
    m["new"] = 5  # mypy error, as Mapping doesn't support item assignment
    return list(m.values())

def read_write(m: MutableMapping[str, int]) -> list[int]:
    m["new"] = 5  # fine, as MutableMapping supports assignment
    return list(m.values())
```

### Forward References

A forward reference is when you need to use a class as a type annotation before that class has actually been defined in the file. By default this fails at runtime because Python reads files top to bottom and the name doesn't exist yet.

There are two ways to fix this. The cleanest is to add `from __future__ import annotations` at the top of the file, which makes
Python treat all annotations as strings and evaluate them lazily. The other option is to just put the type in quotes manually: `def f(foo: 'A')`. This also comes up inside class definitions when a method needs to return an instance of the class itself.


### Decorators

Decorators are functions that wrap other functions to add behaviour. To type annotate a decorator properly so that mypy knows the wrapped function keeps its original signature, you use generics with the new `[F: ...]` syntax (Python 3.12+):

### Coroutines and asyncio

Async functions (coroutines) are typed exactly like normal functions — the only difference is the `async` keyword. mypy understands `async def` and knows that calling it returns a coroutine object rather than the value directly, which is why you need `await` to get the actual result.

## FastAPI

FastAPI is a Python-based web framework that is used for building APIs (Application Programming Interfaces). In other words, FastAPI is a set of mechanisms that defines how requests and responses are processed between different software applications, without either application needing to know the working of the other application. 

Note that you need to carry out set up a virtual enviroment (venv) and carry out `pip install fastapi[standard]` while in it, so that on running `fastapi dev`, the server hosting and running of the FastAPI .py files takes place simultaneously. We assume uvicorn to host the website at the location `http://127.0.0.1:8000` by default on any machine.

```python
from fastapi import FastAPI                             # library used to declare FastAPI app instances

app = FastAPI()                                         # app instance being declared

@app.get("/items")                                      # FastAPI endpoint being established with a GET request, using a decorator
async def get_item():                                   # asynchronously defining the get_item function
    return {"message": "Hello, world!"}                 # returning a JSON response to the GET request
```
Given is the basic setup of a FastAPI endpoint with a GET request to return a JSON response `{"message": "Hello, world!"}` on visiting `http://127.0.0.1:8000/items`. The working of each line has been described in the comments above. Each decorator (the `@app` lines) tell the Python interpreter that the function below the decorator is incharge of handling requests at the URL defined in the decorator (here, `http://127.0.0.1:8000/items`).

One of the most useful aspects of using FastAPI is the interactive API documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc). You get a fully browsable, testable API reference for free just by writing properly typed code. The raw OpenAPI schema is also available at `/openapi.json`.
Taking the example URL above, the documentation would be located at `http://127.0.0.1:8000/docs`, with alternate documentation located at `http://127.0.0.1:8000/redoc`

### Path Parameters

Path parameters are variables embedded in the URL used in the decorator that handles requests sent to that specific URL. They help classify the sub-categories for the URL to which requests may be sent (for example, /items/{item_id} tells the decorator to expect requests from any URL of the form `http://127.0.0.1:8000/items/item_id`, where item_id may be of any datatype). These parameters are defined in a similar way to f-strings, and even though this is sent to the app as a string, FastAPI allows for data parsing and recognizes the datatype that these path parameters were established as.

```python
@app.get("/items/{item_id}")                            # here, item_id is the path parameter, and its value can be used below
async def read_item(item_id: int):                      # type annotation of item_id so that FastAPI knows what to parse it as
    return {"item_id": item_id}
```

By adding a type annotation to the parameter, FastAPI automatically parses the incoming string into that type and validates it. If you pass `"foo"` (or any other value that is NOT an int) to an endpoint expecting an `int`, FastAPI returns a clear validation error
pointing to exactly where it failed.

It is important to note that path operations are evaluated in order, so more specific paths like `/users/me` must be declared before dynamic ones like `/users/{user_id}`, otherwise the dynamic one matches first and "me" gets treated as a user ID, rather than a specific path of its own.

You can also restrict a path parameter to a fixed set of values using a Python Enum. FastAPI will validate against those values and display them as options in the interactive docs automatically.

```python
from enum import Enum                                   # library used for Enums in Python
from fastapi import FastAPI

class ModelName(str, Enum):                             # Enum ModelName being defined using alexnet, resnet and lenet as class
    alexnet = "alexnet"                                 # attributes with corresponding string values
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):             # type annotation using ModelName
    if model_name is ModelName.alexnet:                 # model_name being directly compared to class attribute
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":                     # model_name's value being directly compared to the string 'lenet'
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### Query Parameters

Any function parameter that isn't part of the path is automatically treated as a query parameter — the `?key=value` pairs in a URL. They work exactly like path parameters: FastAPI parses and validates them using the given type annotations. The difference is they can have default values, making them optional.

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

Setting the default to `None` makes a parameter fully optional. Omitting the default entirely makes it required - FastAPI will return an error if the caller doesn't provide it. FastAPI is also smart about bool query parameters — values like "true", "yes", "1", and "on" (i.e, any value apart from 0, False, None, '' etc.) all get correctly parsed to `True`.

## What Surprised Me

There were quite a few things I learnt while going through the reading material that struck me as very interesting -

- I expected FastAPI to be a lot of work, even to set up a simple "hello world" endpoint, but it effectively rendered as just 5 lines of simple, readable code. Everything from the setting up of the development environment to the syntax was quite comprehensible

- It struck me as interesting that Python effectively ignores the type hints during runtime and still allows for the assignment of values to variables that have a different type annotated to them, while in the case of FastAPI, having the type annotations is crucial to knowing what kind of data type needs to be passed as path/query parameters to the app URL.

- The fact that FastAPI automatically sets up an interactive documentation page for us to monitor the endpoint is surprisingly convenient in regards to monitoring error codes + successful transfer of requests and responses


