from overall import yamld,automationmain,autofunc_offpow
import argparse
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
    args = parser.parse_args()
    modulename=args.modulename

    yamld=yamld(modulename)
    listvar=yamld.getlistvar()
   
    powermoduleip=listvar[14]
    program_retry=1
    auto=automationmain(modulename,listvar)
    while(program_retry<4):
        return_code=auto.loopfunction(program_retry)
        if return_code==0:
            break
        else:
            autofunc_offpow.offpower(powermoduleip)
            program_retry+=1