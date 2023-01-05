import argparse,yaml,os
from restructTesting import onpower_fpga_daughthercard,offpower_fpga_daughthercard,writeinterf,loopfunction
from rT_function import yamld,autofunc_download,autofunc_clk

def automation(modulename):

    print(f"RTHome          : {os.getenv('RTHome')}")
    print(f"S2C_WORKDIR     : {os.getenv('S2C_WORKDIR')}")
    print(f"S2C_IP          : {os.getenv('S2C_IP')}")
    print(f"S2C_PWR_CTRL_IP : {os.getenv('S2C_PWR_CTRL_IP')}")
    print(f"S2C_HOSTNAME    : {os.getenv('S2C_HOSTNAME')}")

    try:
        with open("hello.yaml") as file:
            data = yaml.load(file, yaml.SafeLoader)
            fpga = yamld(data, args.m)
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

def clkarg():
    if args.m!=None:

        try:
            with open("hello.yaml") as file:
                data = yaml.load(file, yaml.SafeLoader)
                fpga = yamld(data, args.m)

        except:
            print("Error:There is no such test_config modulename in yaml file!")
            exit()

        listclk=[fpga.s2c_clk_1,fpga.s2c_clk_2,fpga.s2c_clk_3,fpga.s2c_clk_4,fpga.s2c_clk_5,fpga.s2c_clk_6,fpga.s2c_clk_7,fpga.s2c_clk_8]
        x=autofunc_clk()
        x.clockgenmain(listclk)

    else:
        print("Error: Please give a module name in yaml file")  

def downlargv():
    if args.m!=None:

        try:
            with open("hello.yaml") as file:
                data = yaml.load(file, yaml.SafeLoader)
                fpga = yamld(data, args.m)

        except:
            print("Error:There is no such test_config modulename in yaml file!")
            exit()

        x=autofunc_download()
        x.download(fpga.bitfile_fpga1,fpga.bitfile_fpga2)

    else:
        print("Error: Please give a module name in yaml file")     

def ondcargv():

    powerJ11=1 if args.j11_status else 0
    powerJ9=1 if args.j9_status else 0
    powerJ8=1 if args.j8_status else 0
    
    if ((powerJ11==False and powerJ9==False and powerJ8==False)):
        print("Error: You have not declared any port")

    else:
        print(powerJ11,powerJ9,powerJ8)
        onpower_fpga_daughthercard.daughthercard_onpower(powerJ11,powerJ9,powerJ8)

if __name__ == '__main__':

    parser= argparse.ArgumentParser()

    group1=parser.add_argument_group("ON_OFF FPGA_POWER")
    group1.add_argument("-f1","--on_fpga",help="turn on fpga",action="store_true")
    group1.add_argument("-f0","--off_fpga",help="turn off fpga",action="store_true")

    group2=parser.add_argument_group("ON_OFF FPGA_DAUGHTER_CARD")
    group2.add_argument("-dc1","--on_daughtercard",help="turn on daughter card",action="store_true")
    group2.add_argument("-dc0","--off_daughtercard",help="turn off daughter card",action="store_true")
    group2.add_argument("-5_0","--j8_status",help="turn on j11 daughter card", action="store_true")
    group2.add_argument("-3_3","--j9_status",help="turn on j9 daughter card", action="store_true")
    group2.add_argument("-1_8","--j11_status",help="turn on j8 daughter card", action="store_true")

    group3=parser.add_argument_group("DOWNLOAD_BITFILE_FPGA")
    group3.add_argument("-d","--fpga_download",help="fpga1 download status",action="store_true")

    group4=parser.add_argument_group("CLOCK_GENERATE_FPGA")
    group4.add_argument("-c","--setclk",help="set clock in fpga", action="store_true")

    group5=parser.add_argument_group("AUTOMATION_FPGA")
    group5.add_argument("-a","--automation",help="automation main loop",action="store_true")
    group5.add_argument("--m",help="modulename in yaml file")
    
    args=parser.parse_args()
    
    
    if args.on_fpga:
        return_code=onpower_fpga_daughthercard.fpga_onpower()

        
    if args.off_fpga:
        offpower_fpga_daughthercard.offpowerdc()
        offpower_fpga_daughthercard.offpower()

    if args.setclk:
        clkarg()


    if args.fpga_download:
        downlargv()

    if args.on_daughtercard:
        ondcargv()
            
    if args.off_daughtercard:
        offpower_fpga_daughthercard.offpowerdc()
  
    if args.automation:
        if args.m!=None:
            automation(args.m)
        else:
            print("Error: Please give a module name in yaml file")     
    
    