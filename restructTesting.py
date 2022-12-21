import os,yaml,argparse
from rT_function import autofunc_onpow_fpga,autofunc_offpow_fpga,autofunc_clk,autofunc_clkdet,autofunc_download,yamld,runcall,countd

class onpower_fpga_daughthercard(autofunc_onpow_fpga):
    def daughthercard_onpower(powerJ11=None,powerJ9=None,powerJ8=None):  
        interface="  POWER ON DAUGHTHER CARD"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        j11status=0
        j9status=0
        j8status=0
        run=0
        s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')
        print(f"S2C_POWERMODULE_IP== {s2c_pwr_ctrl_ip}")
        os.system('S2C_stm32_lwip.exe --ip ' + f'{s2c_pwr_ctrl_ip}' + ' --port 8080 --readEth > readEth.txt')
        with open(r"readEth.txt","r") as f:
            item=f.readlines()
            if 'J11:on\n' in item:
                j11status=1
            if 'J9:on\n' in item:
                j9status=1
            if 'J8:on\n' in item:
                j8status=1
        if powerJ11:
            if j11status==1:
                print("J11 is already on..\n")
                return_code=0
            else:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J11 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {s2c_pwr_ctrl_ip}, J11 1_8V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
        else:
            if j11status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J11 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J11 1_8V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
            else:
                print("J11 is already off..\n")
                return_code=0
            
        if return_code!=0:
            return return_code 
        
        if powerJ9:
            if j9status==1:
                print("J9 is already on..\n")
                return_code=0
            else:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J9 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {s2c_pwr_ctrl_ip}, J9 3_3V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
        else:
            if j9status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J9 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J9 3_3V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
            else:
                print("J9 is already off..\n")
                return_code=0
        if return_code!=0:
            return return_code 
        
        if powerJ8:
            if j8status==1:
                print("J8 is already on..\n")
                return_code=0
            else:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J8 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {s2c_pwr_ctrl_ip}, J8 5_0V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
        else:
            if j8status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J8 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J8 5_0V ...")
                return_code=runcall.subpcall(cmd,time_out=30)
                run+=1
            else:
                print("J8 is already off..\n")
                return_code=0
        if return_code!=0:
            return return_code 
        if run!=0:
            print("Warming up DAUGHTER CARD in [10 seconds]...")
            countd.countdown(20)
        print("COMPLETE!")
        return return_code

class offpower_fpga_daughthercard(autofunc_offpow_fpga):
    def offpowerdc():
        interface="      POWER OFF DAUGHTHER CARD"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')
        cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J11 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J11 1_8V ...")
        return_code=runcall.subpcall(cmd,time_out=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J9 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J8 3_3V ...")
        return_code=runcall.subpcall(cmd,time_out=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J8 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, J8 5_0V ...")
        return_code=runcall.subpcall(cmd,time_out=30)
        if return_code!=0:
            return return_code 
        
        return return_code

def writeinterf(program_retry,modulename):
        interface="    TESTING RUN {} [{}]".format(program_retry,modulename)
        print("\t"*6,"-"*30)
        print("\t"*6,interface)
        print("\t"*6,"-"*30)
        
def loopfunction(fpga):
    listclk=[fpga.s2c_clk_1,fpga.s2c_clk_2,fpga.s2c_clk_3,fpga.s2c_clk_4,fpga.s2c_clk_5,fpga.s2c_clk_6,fpga.s2c_clk_7,fpga.s2c_clk_8]
    
    return_code=onpower_fpga_daughthercard.fpga_onpower()
    if return_code!=0:
        return return_code 

    x=autofunc_clk()
    return_code=x.clockgenmain(listclk)
    if return_code!=0:
        return return_code

    x=autofunc_download()
    return_code=x.download(fpga.bitfile_fpga1,fpga.bitfile_fpga2)
    if return_code!=0:
        return return_code

    return_code=onpower_fpga_daughthercard.daughthercard_onpower(fpga.power_1_8V ,fpga.power_3_3V,fpga.power_5_0V)
    if return_code!=0:
        return return_code  

    # offpower_fpga_daughthercard.offpowerdc()
    # offpower_fpga_daughthercard.offpower()
    
    return 0


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
    args = parser.parse_args()
    modulename=args.modulename

    
    print(f"RTHome          : {os.getenv('RTHome')}")
    print(f"S2C_WORKDIR     : {os.getenv('S2C_WORKDIR')}")
    print(f"S2C_IP          : {os.getenv('S2C_IP')}")
    print(f"S2C_PWR_CTRL_IP : {os.getenv('S2C_PWR_CTRL_IP')}")
    print(f"S2C_HOSTNAME    : {os.getenv('S2C_HOSTNAME')}")

    try:
        with open("hello.yaml") as file:
            data = yaml.load(file, yaml.SafeLoader)
            fpga = yamld(data, modulename)
    except:
        print("Error:There is no such test_config modulename in yaml file!")
        exit()
    
    program_retry=1
    while(program_retry<4):
        writeinterf(program_retry,modulename)
        return_code=loopfunction(fpga)
        if return_code==0:
            break
        else:
            offpower_fpga_daughthercard.offpowerdc()
            offpower_fpga_daughthercard.offpower()
            program_retry+=1
