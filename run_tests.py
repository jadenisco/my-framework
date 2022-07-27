#!./venv/bin/python3
import sys
import traceback
import config
import sanity_run_vpp
from config import config, num_cpus, available_cpus, max_vpp_cpus

if __name__ == "__main__":
    
    print("{}({})".format(__name__.strip('_'), locals()))
    print("--------------------------------------")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.path}")
    print(f"Config is: {config}")
    print("--------------------------------------")

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
