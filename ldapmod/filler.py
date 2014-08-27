#!/usr/bin/env python3

import sys
import jinja2
import jinja2.meta

def _read(path):
    with open(path, 'r') as f:
        return f.read()

def _input(out=sys.stdout, text=''):
    print(text, file=out, end='')
    out.flush()
    return sys.stdin.readline().rstrip()

class Filler():
    def __init__(self):
        self.env = jinja2.Environment()

    def load(self, path, bindings={}, interactive=False):
        template_str = _read(path)
        ast = self.env.parse(template_str)
        undeclared = jinja2.meta.find_undeclared_variables(ast) - set(bindings)

        if not interactive and undeclared:
            raise RuntimeError('Undefined template variables: {}'.format(undeclared))

        for var in undeclared:
            bindings[var] = _input(sys.stderr, text='{}: '.format(var))

        return self.env.from_string(template_str).render(**bindings)

    def loadi(self, path, bindings={}):
        return self.load(path, bindings, interactive=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: {} path [var=value ...]'.format(sys.argv[0]))

    path = sys.argv[1]
    bind_args = sys.argv[2:]

    bindings = {}
    for arg in bind_args:
        if '=' not in arg:
            sys.exit('Error: {} is not a binding'.format(arg))
        var, value = arg.split('=', 1)
        bindings[var] = value

    f = Filler()
    print(f.load(path, bindings=bindings, interactive=sys.stdout.isatty()))
