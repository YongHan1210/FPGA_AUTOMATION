import argparse,yaml,os
from restructTesting import onpower_fpga_daughthercard,offpower_fpga_daughthercard,writeinterf,loopfunction
from rT_function import yamld,autofunc_download,autofunc_clk

def automation(modulename):
    pprohome = os.getenv('RTHome')
    workdir = os.getenv('S2C_WORKDIR')
    s2c_ip = os.getenv('S2C_IP')
    s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')
    hostname = os.getenv('S2C_HOSTNAME')
    print(pprohome)
    print(workdir)
    print(s2c_ip)
    print(s2c_pwr_ctrl_ip)
    print(hostname)

    with open("hello.yaml") as file:
        data = yaml.load(file, yaml.SafeLoader)
        fpga = yamld(data, modulename)
    print(fpga.s2c_clk_3)
    
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





if __name__ == '__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument("-f1","--on_fpga",help="turn on fpga",action="store_true")
    parser.add_argument("-f0","--off_fpga",help="turn off fpga",action="store_true")
    
    parser.add_argument("-dc1","--on_daughtercard",help="turn on daughter card",action="store_true")
    parser.add_argument("-dc0","--off_daughtercard",help="turn off daughter card",action="store_true")
    parser.add_argument("-5","--j8_status",help="turn on j11 daughter card", action="store_true")
    parser.add_argument("-3_3","--j9_status",help="turn on j9 daughter card", action="store_true")
    parser.add_argument("-1_8","--j11_status",help="turn on j8 daughter card", action="store_true")
    
    parser.add_argument("-d","--fpga_download",help="fpga1 download status",action="store_true")


    
    parser.add_argument("-c","--setclk",help="set clock in fpga", action="store_true")

    
    parser.add_argument("-a","--automation",help="automation main loop",action="store_true")
    parser.add_argument("--m",help="modulename in yaml file")
    args=parser.parse_args()
    
    
    if args.on_fpga:
        print("turn on fpga")
        return_code=onpower_fpga_daughthercard.fpga_onpower()
        if return_code!=0:
            print("Error in onpower fpga")
        
    if args.off_fpga:
        print("turn off fpga")
        offpower_fpga_daughthercard.offpowerdc()
        offpower_fpga_daughthercard.offpower()

    if args.setclk:
        if args.m!=None:
            print("set clock")
            print(args.m)
            with open("hello.yaml") as file:
                data = yaml.load(file, yaml.SafeLoader)
                fpga = yamld(data, args.m)
            listclk=[fpga.s2c_clk_1,fpga.s2c_clk_2,fpga.s2c_clk_3,fpga.s2c_clk_4,fpga.s2c_clk_5,fpga.s2c_clk_6,fpga.s2c_clk_7,fpga.s2c_clk_8]
            print(listclk)
            x=autofunc_clk()
            return_code=x.clockgenmain(listclk)
            if return_code!=0:
                print("Error in clkset fpga")
        else:
            print("Error: Please give a module name in yaml file")  


    if args.fpga_download:
        if args.m!=None:
            print("fpga1 download")
            print(args.m)
            with open("hello.yaml") as file:
                data = yaml.load(file, yaml.SafeLoader)
                fpga = yamld(data, args.m)
            print(fpga.bitfile_fpga1)
            print(fpga.bitfile_fpga2)
            x=autofunc_download()
            return_code=x.download(fpga.bitfile_fpga1,fpga.bitfile_fpga2)
            if return_code!=0:
                print("Error in download fpga")
        else:
            print("Error: Please give a module name in yaml file")     

    if args.on_daughtercard:
        print("turn on daughter card")
        powerJ11=1 if args.j11_status else 0
        powerJ9=1 if args.j9_status else 0
        powerJ8=1 if args.j8_status else 0
        
        if ((powerJ11==False and powerJ9==False and powerJ8==False)):
            print("Error: You have not declared any port")
        else:
            print(powerJ11,powerJ9,powerJ8)
            #onpower_fpga_daughthercard.daughthercard_onpower(powerJ11,powerJ9,powerJ8)
            
    if args.off_daughtercard:
        print("turn off daughter card")
        # offpower_fpga_daughthercard.offpowerdc()
        
       
              
            

  
    
    if args.automation:
        if args.m!=None:
            print("automation")
            print(args.m)
            automation(args.m)
        else:
            print("Error: Please give a module name in yaml file")     
    
    