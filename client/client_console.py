#!/usr/bin/env python
import cmd, sys
import client_backend


def parse(arg):
    return tuple(map(int, arg.split()))


class Shell(cmd.Cmd):
    intro = 'Welcome to Robbie\'s command prompt'

    ###################
    # PROPULSION
    ###################
    def do_forward(self, arg):
        'Move vehicle forward'
        client_backend.forward_fun(*parse(arg))

    def do_backward(self, arg):
        'Move vehicle backward'
        client_backend.backward_fun(*parse(arg))

    def do_left(self, arg):
        'Turn vehicle left'
        client_backend.left_fun(*parse(arg))

    def do_right(self, arg):
        'Turn vehicle right'
        client_backend.right_fun(*parse(arg))

    def do_stop(self, arg):
        'Stop vehicle'
        client_backend.stop_fun()

    def do_bearing(self, arg):
        'Turn to bearing'
        client_backend.bearing_fun(*parse(arg))

    ####################
    # CAMERA
    ####################

    def do_cam_left(self, arg):
        'Move camera left'
        client_backend.x_increase(*parse(arg))

    def do_cam_right(self, arg):
        'Move camera right'
        client_backend.x_decrease(*parse(arg))

    def do_cam_up(self, arg):
        'Move camera up'
        client_backend.y_increase(*parse(arg))

    def do_cam_down(self, arg):
        'Move camera down'
        client_backend.y_decrease(*parse(arg))

    def do_cam_center(self, arg):
        'Move camera back to center'
        client_backend.xy_home()


    ####################
    # QUIT CONSOLE
    ####################

    def do_quit(self, arg):
        'Quit the console'
        client_backend.quit_fun()



if __name__=='__main__':
    Shell().cmdloop()
