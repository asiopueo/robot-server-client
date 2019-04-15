import time
import serial


class PID:
    def __init__(self, Kp=1., Kd=1., Ki=1.):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki

        self.last_t = time.time()
        self.last_x = 0    # Used for computing the differential
        self.integral = 0  #

    def compute(self, d):
        dt = time.time() - self.last_t
        self.last_t = time.time()
        # Differential:
        dd = (d-self.last_x)/dt
        # Integral:
        self.integral += d*dt

        return - self.Kp*d - self.Kd*dd - self.Ki*self.integral

#####################
# Range of values ? #
#####################


if __name__=='__main__':
    s = serial.Serial('/dev/ttyACM0', 14400)

    pid = PID(0.2, 0.1, 1.0)

    while True:
        t = time.time()
        try:
            str = s.readline().decode() #read_until('\r\n')
            str = str.split('=')[1].split(',')[0]
            yaw = float(str)
            print("Yaw: {}".format(yaw))
            print("Value: {}".format(pid.compute(yaw)))

        except UnicodeDecodeError: #catch error and ignore it
            print('Something went wrong!')
