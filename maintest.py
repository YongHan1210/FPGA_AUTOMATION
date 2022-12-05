from overall import yamld,automationmain,autofunc_offpow,getpowermoduleip
import argparse,yaml
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
    args = parser.parse_args()
    modulename=args.modulename

    with open("hello.yaml") as file:
        data = yaml.load(file, yaml.SafeLoader)
        fpga = yamld(data, modulename)
        
    powermoduleip=getpowermoduleip.def_powermodule_ip(fpga.hostname)
    listvar=[fpga.power_1_8V, fpga.power_3_3V, fpga.power_5_0V,fpga.s2c_clk_1,fpga.s2c_clk_2,fpga.s2c_clk_3,fpga.s2c_clk_4,fpga.s2c_clk_5,fpga.s2c_clk_6,fpga.s2c_clk_7,fpga.s2c_clk_8,fpga.bitfile_fpga1,fpga.bitfile_fpga2,fpga.hostname,powermoduleip]

    program_retry=1
    auto=automationmain(modulename,listvar)
    while(program_retry<4):
        return_code=auto.loopfunction(program_retry)
        if return_code==0:
            break
        else:
            autofunc_offpow.offpower(powermoduleip)
            program_retry+=1