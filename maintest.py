
from nono import yamld,mkfolfildir,automationmain,autofunc_offpow,argparse
import s2cyh

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
    args = parser.parse_args()
    modulename=args.modulename

    yamld=yamld(modulename)
    hostname=yamld.gethostname()
    powermoduleip=yamld.getpowermodule_ip()
    listvar=[yamld.getpower_1_8V(),yamld.getpower_3_3V(),yamld.getpower_5_0V(),yamld.getS2CCLK_1(),yamld.getS2CCLK_2(),yamld.getS2CCLK_3(),yamld.getS2CCLK_4(),yamld.getS2CCLK_5(),yamld.getS2CCLK_6(),yamld.getS2CCLK_7(),yamld.getS2CCLK_8(),yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile()]

    mk=mkfolfildir(yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile())
    fpga1outpath,fpga2outpath=mk.mainff()
    
    program_retry=1
    auto=automationmain(modulename,hostname,powermoduleip,listvar,fpga1outpath,fpga2outpath)
    #auto=automationmain(powermoduleip,hostname,yamld.getpower_1_8V(),yamld.getpower_3_3V(),yamld.getpower_5_0V(),yamld.getS2CCLK_1(),yamld.getS2CCLK_2(),yamld.getS2CCLK_3(),yamld.getS2CCLK_4(),yamld.getS2CCLK_5(),yamld.getS2CCLK_6(),yamld.getS2CCLK_7(),yamld.getS2CCLK_8(),yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile(),fpga1outpath,fpga2outpath)
    while(program_retry<4):
        return_code=auto.loopfunction(program_retry)
        if return_code==0:
            break
        else:
            autofunc_offpow.offpower(powermoduleip,fpga1outpath,fpga2outpath)
            program_retry+=1