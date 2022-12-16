import argparse
from restructTesting import onpower_fpga_daughthercard,offpower_fpga_daughthercard

if __name__ == '__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument("-1_f","--on_fpga",help="turn on fpga",action="store_true")
    parser.add_argument("-0_f","--off_fpga",help="turn off fpga",action="store_true")
    
    parser.add_argument("-1_dc","--on_daughtercard",help="turn on daughter card",action="store_true")
    parser.add_argument("-0_dc","--off_daughtercard",help="turn off daughter card",action="store_true")
    parser.add_argument("-j11","--setclk",help="set clock in fpga", action="store_true")
    parser.add_argument("-j9","--setclk",help="set clock in fpga", action="store_true")
    parser.add_argument("-j8","--setclk",help="set clock in fpga", action="store_true")
    
    parser.add_argument("-df1","--fpga1_download",help="fpga1 download status",action="store_true")
    parser.add_argument("-df2","--fpga2_download",help="fpga2 download status",action="store_true")

    
    parser.add_argument("-c","--setclk",help="set clock in fpga", action="store_true")

    
    parser.add_argument("-a","--automation",help="automation main loop",action="store_true")
    parser.add_argument("-m","--modulename",help="modulename in yaml file")
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
    
    if args.on_daughtercard:
        print("turn on daughter card")
    
    if args.off_daughtercard:
        print("turn off daughter card")
        
    if args.fpga1_download:
        if args.modulename!=None:
            print("fpga1 download")
            print(args.modulename)
        else:
            print("Error: Please give a module name in yaml file")        

    if args.fpga2_download:
        if args.modulename!=None:
            print("fpga2 download")
            print(args.modulename)
        else:
            print("Error: Please give a module name in yaml file")       
            
    if args.setclk:
            print("set clock")
            print(args.clock_list)
  
    
    if args.automation:
        if args.modulename!=None:
            print("automation")
            print(args.modulename)
        else:
            print("Error: Please give a module name in yaml file")     
    
    