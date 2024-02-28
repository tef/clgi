#!/usr/bin/env python3
""" Example Command Line Application"""

# Run this command in your terminal to setup tab complete
# Inside the examples directory:
# complete -C `pwd`/test.py test.py

## Boilerplate to allow project to run from checkout
import os.path
import sys
FILENAME = os.path.normpath(__file__)
PROJECT_ROOT = os.path.split(os.path.dirname(FILENAME))[0]
MODULE_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.append(MODULE_PATH)
## You do not want this in your project

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Response

class AppError(Error):
    pass

router = Router()

@router.on_error(AppError)
def app_error(request, code):
    args = request.args
    error_args, original_request = args['args'], args['request']
    code(-1)
    filename = error_args
    if filename:
        return ["app error: {}".format(filename)]

@router.on("sum", "add") 
@command(args=dict(nums="int*"))
def Sum(ctx, nums):
    app = ctx['app']
    name = ctx['name']
    out = sum(nums)
    return Response(str(out))


app = App(
    name="test", 
    version="0.0.1",
    command=router,
    args={ },
)

app.main(__name__)
