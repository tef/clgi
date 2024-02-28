# clgi: A commandline toolkit for python

This is demo code extracted from a larger project. 

`clgi` is an attempt to write command line applications a little bit more like a webapp.

## Overview

Instead of something like `argparse` or `optparse`, you define your application in terms of routes and commands:

```
import clgi

router = clgi.Router()

@router.on("hello", "hello:world")
@clgi.command()
def example(ctx):
    return clgi.Response("hello world")

app = clgi.App(name="test", version="2.3", command=router, args={})

app.main(__name__)
```

The `Router` can also be used to route errors, with `router.on_error()`, and the `@command` decorator takes a list of arguments to pass into the wrapped function:

```
import clgi
@clgi.command(args={"args": "string*"})
def example(ctx, args):
    out = " ".join(args)
    return clgi.Response(out)

app = clgi.App(name="test", version="2.3", command=example, args={})

app.main(__name__)
```

Underneath, `clgi` works by having a standard callback for handling command line requests, 
and a result code, much like wsgi. you don't have to use the `@command` decorator, or even a `Router`:

```
import clgi

def example_command(request, code):
    code(0) # return 0
    return "Hello, world!"

app = clgi.App(name="test", version="2.3", command=example_command, args={})

app.main(__name__)

```

The app doesn't care if it's a `Router` or a `@command`, or a raw function,
and neither does the Router. Only the `@command` decorator expects a normal
python function.

## Argument parsing and tab completion

Every `clgi` app comes with built in tab completion. Running `complete -C `pwd`/test.py test.py` tells bash to use the program itself to generate results.

The `@command` decorator accepts a dictionary of name-value pairs for args. Argument values can be things like strings, numbers, paths, files or directories.

```
args = {
    "first": "--int"  # mandatory integer named argument
    "second": "--string?" # optional string named argument
    "third":  "--string*" # optional string named argument, can repeat
    "fourth":  "--string*" # string named argument, can repeat

    "final":  "string*" # string positional argument, can repeat
    # could be "string", "string?" or "string+", for example
}
```

The `@command` only allows for one type of positional argument, because it makes tab completion a bit of a pain in the arse.  If you need it, it should be possible to write a raw clgi function. I believe I did, Bob.

Note: although boolean arguments are supported, subcommands are better imho.

### Pager

`clgi` comes with a built in pager, but it's sorely lacking. 

the original project this is lifted from did things like text reflow,
tables, headers, and lists. this code does "a list of strings" so there
isn't much to reflow on resize.

one day (not today), clgi will let you browse the app's documentation.
