#!./venv/bin/python3
import sys
import traceback
import config
import sanity_run_vpp
from config import config, num_cpus, available_cpus, max_vpp_cpus

myArg = 0

class Rectangle():
#    def __init__(cls, length, width):
#        cls.length = length
#        cls.width = width

    def setUpClass(self):
        super(Rectangle)
        self.length = 4
        self.width = 4

    def area(cls):
        return cls.length * cls.width

    def perimeter(cls):
        return 2 * cls.length + 2 * cls.width

class Square(Rectangle):
    def __init__(cls, length):
        super(Square, cls).__init__(length, length)

class Cube(Square):
    def surface_area(self):
        face_area = super().area()
        return face_area * 6

    def volume(self):
        face_area = super().area()
        return face_area * self.length

if __name__ == "__main__":
    
    print("{}({})".format(__name__.strip('_'), locals()))
    print("--------------------------------------")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.path}")
    print(f"Config is: {config}")
    print("--------------------------------------")

    tc = Rectangle()
    tc.setUpClass()

    print(tc.area())

    if config.sanity:
        print("Running sanity test case.")
        try:
            rc = sanity_run_vpp.main()
            if rc != 0:
                sys.exit(rc)
        except Exception as e:
            print(traceback.format_exc())
            print("Couldn't run sanity test case.")
            sys.exit(-1)
