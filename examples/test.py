#!/usr/bin/env python3
""" Example Command Line Application"""

## Boilerplate to allow project to run from checkout
import os.path
import sys
PROJECT_ROOT = os.path.split(os.path.dirname(__file__))[0]
sys.path.append(os.path.join(PROJECT_ROOT, "src"))
## You do not want this in your project

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext

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
    return Plaintext(str(out))


app = App(
    name="test", 
    version="0.0.1",
    command=router,
    args={ },
)

app.main(__name__)
