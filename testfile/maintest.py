from overall import yamld,autofunc_offpow,getpowermoduleip,autofunc_onpow,autofunc_clk,autofunc_hardware,autofunc_download,autofunc_clkdet
import argparse,yaml

def writeinterf(program_retry,modulename):
        interface="    TESTING RUN {} [{}]".format(program_retry,modulename)
        print("\t"*6,"-"*30)
        print("\t"*6,interface)
        print("\t"*6,"-"*30)
        
def loopfunction(program_retry,modulename,fpga,powermoduleip):
    listclk=[fpga.s2c_clk_1,fpga.s2c_clk_2,fpga.s2c_clk_3,fpga.s2c_clk_4,fpga.s2c_clk_5,fpga.s2c_clk_6,fpga.s2c_clk_7,fpga.s2c_clk_8]
    writeinterf(program_retry,modulename)

    return_code=autofunc_onpow.fpga_onpower(powermoduleip)
    if return_code:
        return return_code  
        
    return_code=autofunc_clk.clockgenmain(listclk)
    if return_code:
        return return_code

    return_code=autofunc_hardware.hardware()
    if return_code:
        return return_code
        
    return_code=autofunc_download.download(fpga.bitfile_fpga1,fpga.bitfile_fpga2,fpga.hostname)
    if return_code:
        return return_code
    
    return_code=autofunc_clkdet.readcheckclkmain(fpga.hostname,listclk)
    if return_code:
        return return_code
    
    return_code=autofunc_onpow.daughthercard_onpower(fpga.power_1_8V ,fpga.power_3_3V,fpga.power_5_0V,powermoduleip)
    if return_code:
        return return_code  
    
    return return_code

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
    args = parser.parse_args()
    modulename=args.modulename

    with open("hello.yaml") as file:
        data = yaml.load(file, yaml.SafeLoader)
        fpga = yamld(data, modulename)
    print(fpga.hostname)
    powermoduleip=getpowermoduleip.def_powermodule_ip(fpga.hostname)
    program_retry=1

    while(program_retry<4):
        return_code=loopfunction(program_retry,modulename,fpga,powermoduleip)
        if return_code==0:
            break
        else:
            autofunc_offpow.offpower(powermoduleip)
            program_retry+=1