"""
with check_modified_imports() as modified:
    import foo
for m in modified:
    print("modified!", os.path.relpath(m), file=sys.stderr)
"""

import os
import sys
import os.path
from contextlib import contextmanager

def is_modified(file):
    dir, p = os.path.split(file)
    swapfile = os.path.join(dir, f".{p}.swp")
    if os.path.exists(swapfile):
        with open(swapfile,'rb') as fh:
            contents = fh.read()
            if contents[:5] != b"b0VIM": return
            fn = contents[108:1008].rsplit(b"\x00",1)[-1]
            if fn.endswith(b"U"):
                return True

if 'COMP_LINE' in os.environ and 'COMP_POINT' in os.environ:
    @contextmanager
    def check_modified_imports():
        yield ()
else:
    @contextmanager
    def check_modified_imports():
        old = set(sys.modules.keys())
        modified = []

        yield modified

        new = sys.modules.keys() - old

        path = os.path.dirname(os.path.abspath(__file__))
        files = [os.path.abspath(__file__)]

        for module in new:
            m = sys.modules[module]
            file = getattr(m, "__file__", "")
            if file and os.path.commonprefix([file, path]) == path:
                files.append(file)


        for file in files:
            if is_modified(file):
                modified.append(file)
