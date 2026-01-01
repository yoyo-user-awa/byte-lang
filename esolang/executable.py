import os
import interpreter as interp
import argparse as argp


class Error:
    def __init__(self, label):
        self.label = label

    def __call__(self, msg):
        print(f'\033[31m{self.label}: {msg}\033[0m')
        quit()


parser = argp.ArgumentParser(add_help=False)
parser.add_argument('-v', '--version', action='version', version='ByteLang v1.0-release')
parser.add_argument('path', nargs='?', default='@undefined', type=str)
parser.add_argument('-h', '--help', action='store_true', default=argp.SUPPRESS)
cmdargs = parser.parse_args()


class Help:
    def __init__(self, **params: tuple[str, str]):
        self.args = params

    def print_help(self) -> None:
        print('ByteLang v1.0-release')
        print('Ext: .bytl')
        print('Usage:')
        for k, v in self.args.items():
            if v[1] == 'pos':
                print(f'\t{k:<20}{v[0]:<30}')
            if v[1] == 'short_kw':
                print(f'\t{'-' + k:<20}{v[0]:<30}')
            if v[1] == 'long_kw':
                print(f'\t{"--" + k:<20}{v[0]:<30}')
        print('-' * 20)


helper = Help(
    version=('Show ByteLang interpreter version', 'long_kw'),
    v=('A shortcut of "--version"', 'short_kw'),
    path=('Filepath of the file that you want to run', 'pos')
)
if cmdargs.help:
    helper.print_help()
elif cmdargs.path == '@undefined':
    print('Correct usage:')
    helper.print_help()
else:
    if os.path.isfile(cmdargs.path) and os.path.exists(cmdargs.path):
        if not cmdargs.path.endswith('.bytl'):
            err = Error('ExtError')
            err(f'The file "{cmdargs.path}" is not a ByteLang file')
            print('Correct ext: .bytl')
        with open(cmdargs.path, 'r') as f:
            code = f.read()
        interpreter = interp.Interpreter()
        interpreter.exe(code)
    else:
        err = Error('FileError')
        err(f'The file "{cmdargs.path}" is not a file / not exists')