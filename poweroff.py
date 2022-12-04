from overall import autofunc_offpow
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("powermoduleip", help="powercontrol IP",type=str)
    args = parser.parse_args()
    powermoduleip=args.powermoduleip
    autofunc_offpow.offpower(powermoduleip)