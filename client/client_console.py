#!/usr/bin/env python
import cmd, sys
import client_backend


def parse(arg):
    return tuple(map(int, arg.split()))


class Shell(cmd.Cmd):
    intro = 'Welcome to Robbie\'s command prompt'

    def do_forward(self, arg):
        'Move vehicle forward'
        client_backend.forward_fun()

    def do_backward(self, arg):
        'Move vehicle backward'
        client_backend.backward_fun()

    def do_left(self, arg):
        'Turn vehicle left'
        client_backend.left_fun()

    def do_right(self, arg):
        'Turn vehicle right'
        client_backend.right_fun()

    def do_stop(self, arg):
        'Stop vehicle'
        client_backend.stop_fun()

    def do_quit(self, arg):
        'Quit the console'
        client_backend.quit_fun()



if __name__=='__main__':
    Shell().cmdloop()
