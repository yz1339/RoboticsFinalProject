# run as super user
# port: /dev/ttyUSB0

import struct
import sys, glob # for listing serial ports
import time

try:
    import serial
except ImportError:
    tkMessageBox.showerror('Import error', 'Please install pyserial.')
    raise

connection = None

TEXTWIDTH = 40 # window width, in characters
TEXTHEIGHT = 16 # window height, in lines

VELOCITYCHANGE = 100
ROTATIONCHANGE = 150

class TetheredDriveApp():
    # sendCommandASCII takes a string of whitespace-separated,
    # ASCII-encoded base 10 values to send
    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.sendCommandRaw(cmd)

    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        try:
            if connection is not None:
                connection.write(command)
            else:     
                print "Not connected."
        except serial.SerialException:
            print "Lost connection"
            connection = None

        print ' '.join([ str(ord(c)) for c in command ])

    # getDecodedBytes returns a n-byte value decoded using a format string.
    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection
        
        try:
            print('return')
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print "Lost connection"
            connection = None
            return None
        except struct.error:
            print "Got unexpected data from serial port."
            return None

    # get8Unsigned returns an 8-bit unsigned value.
    def get8Unsigned(self):
        return getDecodedBytes(1, "B")

    # get8Signed returns an 8-bit signed value.
    def get8Signed(self):
        return getDecodedBytes(1, "b")

    # get16Unsigned returns a 16-bit unsigned value.
    def get16Unsigned(self):
        return getDecodedBytes(2, ">H")

    # get16Signed returns a 16-bit signed value.
    def get16Signed(self):
        return getDecodedBytes(2, ">h")

    def connect(self):
        global connection

        if connection is not None:
            print('Oops', "You're already connected!")
            return

        port = '/dev/tty.usbserial-DA01NPT0'

        try:
            connection = serial.Serial(port, baudrate=115200, timeout=1)
            print "Connected!"
            self.sendCommandASCII('128') # P: Passive
            self.sendCommandASCII('131') # S: Safe
            self.sendCommandASCII('140 3 1 64 16 141 3') # Beep
        except:
            print "Failed."

    def testDrive(self):
        self.moveForward()
        time.sleep(1)
        self.stop()

        self.rotateRight()
        time.sleep(0.5)
        self.stop()

        self.rotateLeft()
        time.sleep(0.5)
        self.stop()

        self.moveBackward()
        time.sleep(1)
        self.stop()
    
    def moveForward(self):
        # compute left and right wheel velocities
        vr = VELOCITYCHANGE
        vl = VELOCITYCHANGE
        # create drive command
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.sendCommandRaw(cmd)

    def moveBackward(self):
        vr = -VELOCITYCHANGE
        vl = -VELOCITYCHANGE
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.sendCommandRaw(cmd)

    def rotateRight(self):
        vr = -ROTATIONCHANGE/2
        vl = ROTATIONCHANGE/2
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.sendCommandRaw(cmd)

    def rotateLeft(self):
        vr = ROTATIONCHANGE/2
        vl = -ROTATIONCHANGE/2
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.sendCommandRaw(cmd)

    def stop(self):
        vr = 0
        vl = 0
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.sendCommandRaw(cmd)
    

if __name__ == "__main__":
    app = TetheredDriveApp()
    app.connect()
    time.sleep(0.5)
    app.testDrive()
