import os,re,time
from s2cyh import S2cPlayerPro,S2C_FPGAS
from utilsyh import Util


class yamld:
    def __init__(self, fpga_data,module):
            data = fpga_data[module]['fpga']
            self.power_1_8V    = data['power_1_8V']
            self.power_3_3V    = data['power_3_3V']
            self.power_5_0V    = data['power_5_0V']
            self.s2c_clk_1     = data['S2CCLK_1']
            self.s2c_clk_2     = data['S2CCLK_2']
            self.s2c_clk_3     = data['S2CCLK_3']
            self.s2c_clk_4     = data['S2CCLK_4']
            self.s2c_clk_5     = data['S2CCLK_5']
            self.s2c_clk_6     = data['S2CCLK_6']
            self.s2c_clk_7     = data['S2CCLK_7']
            self.s2c_clk_8     = data['S2CCLK_8']
            self.bitfile_fpga1 = data['bitfile_fpga1']
            self.bitfile_fpga2 = data['bitfile_fpga2']

class countd():
    def countdown(t):
        while t:
            time.sleep(1)
            t-=1


class autofunc_offpow_fpga:

    def offpowerdc():
        return 0

    def offpower():
        interface="      POWER OFF FPGA"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)

        s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')
        print(f"S2C_POWERMODULE_IP== {s2c_pwr_ctrl_ip}")

        cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J6 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {s2c_pwr_ctrl_ip}, S2C_POWER_BASE ...")
        return_code=runcall.subpcall(cmd,time_out=30)
        if return_code!=0:
            return return_code 

        print("Cooling down FPGA in 10 seconds...")
        countd.countdown(10)
        os.system('S2C_stm32_lwip.exe --ip ' + f'{s2c_pwr_ctrl_ip}' + ' --port 8080 --readEth > readEth.txt')
        offstate=0
        with open(r"readEth.txt","r") as f:
            item=f.readlines()
            if 'J6:off\n' not in item:
                offstate+=1
            if 'J8:off\n' not in item:
                offstate+=1
            if 'J9:off\n' not in item:
                offstate+=1
            if 'J11:off\n' not in item:
                offstate+=1
        if offstate!=0:
            print("Error in TURNING OFF FPGA POWER")
            return_code=1
        else:
            print("FPGA Successfully TURN OFF..")
            return_code=0
  
        return return_code

class fpga_powerstatus:
    def check_powerstatus():
        s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')
        j6status=0
        os.system('S2C_stm32_lwip.exe --ip ' + f'{s2c_pwr_ctrl_ip}' + ' --port 8080 --readEth > readEth.txt')
        with open(r"readEth.txt","r") as f:
            item=f.readlines()
            if 'J6:on\n' in item:
                j6status=1
        return j6status

class autofunc_onpow_fpga:
    
    def fpga_onpower():
        interface="      POWER ON FPGA"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        s2c_pwr_ctrl_ip = os.getenv('S2C_PWR_CTRL_IP')

 
        if fpga_powerstatus.check_powerstatus()==1:
            print("S2C_POWER_BASE is already on.")
            return 0
        else:
            print("S2C_POWER_BASE is off.")
            cmd=f"S2C_stm32_lwip.exe --ip {s2c_pwr_ctrl_ip} --port 8080 --pwr J6 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {s2c_pwr_ctrl_ip}, S2C_POWER_BASE ...")
            return_code=runcall.subpcall(cmd,time_out=30)
            if return_code!=0:
                return return_code 
            print("Warming up FPGA in [20 seconds]...")
            countd.countdown(20)
            return return_code
    
    def daughthercard_onpower():
        return 0

class Parentvariable:
    def __init__(self):
        workdir=os.getenv('S2C_WORKDIR')
        pprohome=os.getenv('RTHome')
        hostname = os.getenv('S2C_HOSTNAME')

        self.clktemp_path=f"CLKTEMP.txt"
        with open(self.clktemp_path,"w")as f:
            f.close()
        self.downloadtemp_path=f"DOWNLOADTEMP.txt"
        with open(self.downloadtemp_path,"w")as f:
            f.close()
        self.ppro=S2cPlayerPro(pprohome, workdir)
        self.ppro.select_target_hardware(hostname)
        
        s2c_fpga=S2C_FPGAS[hostname]

        self.boardtypeT=s2c_fpga.get_boardtype()
        self.s2chome=os.path.join(workdir, '.s2chome')+'\/'
        self.pprohome_firmware_bin=os.path.join(pprohome, 'firmware','bin')
        self.pprohome_bin_tools=os.path.join(pprohome, 'bin','tools')


class autofunc_clk(Parentvariable):
    def __init__(self):
        Parentvariable.__init__(self)

    def clockgenmain(self,listclk):
        if fpga_powerstatus.check_powerstatus()==1:
            pass
        else:
            print("Error: Fpga J6 is Off>> Redirecting to TURN ON FPGA..")
            time.sleep(2)
            autofunc_onpow_fpga.fpga_onpower()
        clkexec_direc=os.path.join(self.pprohome_firmware_bin,'s2cclockgen_vuls.exe')
        s2chome=self.s2chome
        boardtype=self.boardtypeT
        hardwareexec_direc=os.path.join(self.pprohome_bin_tools,'S2C_HardWare.exe')

        interface="      CLOCKGEN MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)

        returncode=self.clockgen1(listclk,clkexec_direc,s2chome,boardtype)
        if returncode!=0:
            return returncode
        returncode=self.clockgen2(listclk,clkexec_direc,s2chome,boardtype)
        if returncode!=0:
            return returncode
        returncode=self.hardware(hardwareexec_direc,s2chome,boardtype)
        if returncode!=0:
            return returncode
        x=autofunc_clkdet()
        return_code=x.readcheckclkmain(listclk)
        if return_code!=0:
            return return_code

        return returncode


    def clockgen1(self,listclk,clkexec_direc,s2chome,boardtype):

        cmd=r'{} -q --ind  --file {}  -r 112 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(clkexec_direc,s2chome,str(listclk[0]),str(listclk[1]),str(listclk[2]),str(listclk[6]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return runcall.subpcall(cmd,time_out=30)

    def clockgen2(self,listclk,clkexec_direc,s2chome,boardtype):

        cmd=r'{} -q --ind  --file {}  -r 113 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(clkexec_direc,s2chome,str(listclk[3]),str(listclk[4]),str(listclk[5]),str(listclk[7]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return runcall.subpcall(cmd,time_out=30)

    def hardware(self,hardwareexec_direc,s2chome,boardtype):

        interface="      HARDWARE MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)

        cmd= r'{} -f {} --mode clk -b {}'.format(hardwareexec_direc,s2chome,boardtype)
        print("\nRUNNING CMD:{}".format(cmd))
        return runcall.subpcall(cmd,time_out=30)

class autofunc_clkdet(Parentvariable):
    def __init__(self):
        Parentvariable.__init__(self)
    def readcheckclkmain(self,listclk=None):
        self.ppro.read_hwinfo(self.clktemp_path)
        self.readclock(listclk)
        if listclk!=None:
            clkdetret=self.clkchecking(listclk)
            return clkdetret
        else:
            return 0

    def readclock(self,inputclk_list=None):
        desarr=[" << A1 >>"," << A2 >>"," << A3 >>","<< B1 >>","<< B2 >>","<< B3 >>","<< A4 >>","<< B4 >>"]
        interface="    READCLOCK MODULE"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        if inputclk_list!=None:
            print("\t\t\t         PLAYER PRO CLOCK\t                   INPUT CLOCK")
        else:
             print("\t"*6,"    PLAYER PRO CLOCK")
        fileread=open(self.clktemp_path,"r")
        text="			<S2CCLK"
        lines=fileread.readlines()
        playerproclk_list=[]
        idx=0
        for line in lines:
            if text in line:
                playerproclk_list.insert(idx,line)
                idx+=1
        fileread.close()
        if len(playerproclk_list)==0:
            print("\nNO CLOCK\n")
        else:
            linelen=len(playerproclk_list)
            i=0
            while i <linelen:

                end=str(playerproclk_list[i]).strip()
                
                g=str(desarr[i])
                if inputclk_list!=None:
                    m=float(inputclk_list[i])
                    clkarr="<S2CCLKARR{} fre='{} MHz'>".format(i+1,m)
                    overall="{}  {}  {}".format(end,g,clkarr)
                    print("\t\t\t   {}".format(overall))
                else:
                    overall="\t\t{}  {}  ".format(end,g)
                    print("\t\t\t   {}".format(overall))
                i+=1
            print() 
     
    def clkchecking(self,listclk):
        interface="    CLOCKCHECKING MODULE"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        lisy=[]
        i=0
        with open(self.clktemp_path,"r")as f:
            lines=f.readlines()
            for row in lines:
                word='			<S2CCLK'
                if row.find(word) !=-1:
                    i+=1
                    row=re.sub(' MHz"/>','',row)
                    match i:
                        case 1:
                            row=re.sub('			<S2CCLK1 fre="','',row)
                        case 2:
                            row=re.sub('			<S2CCLK2 fre="','',row)
                        case 3:
                            row=re.sub('			<S2CCLK3 fre="','',row)   
                        case 4:
                            row=re.sub('			<S2CCLK4 fre="','',row) 
                        case 5:
                            row=re.sub('			<S2CCLK5 fre="','',row) 
                        case 6:
                            row=re.sub('			<S2CCLK6 fre="','',row) 
                        case 7:
                            row=re.sub('			<S2CCLK7 fre="','',row) 
                        case 8:
                            row=re.sub('			<S2CCLK8 fre="','',row)                       
                    lisy.append(row.strip())
        if (i==0):
            print("no found")
        i=0
        for x in range (len(lisy)):
            m=float(listclk[x])
            r=float(lisy[x])

            sub=r-m
            if sub<0:
                sub*=-1
            if sub<0.1:
                i+=1
            else:
                break
        if(i==8):
            print("\t"*6,"    CLOCK CHECKED SUCCESS")
            return 0
        else:
            print("\t"*6,"ERROR:CLOCK CHECKED FAILED")
            return 1


class autofunc_download(Parentvariable):
    def __init__(self):
        Parentvariable.__init__(self)

    def download(self,f1_bit,f2_bit):
        if fpga_powerstatus.check_powerstatus()==1:
            pass
        else:
            print("Error: Fpga J6 is Off>> Redirecting to TURN ON FPGA..")
            time.sleep(2)
            autofunc_onpow_fpga.fpga_onpower()
        interface="      DOWNLOAD MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        return_code=1
        print("<<FPGA1 is TURN ON>>") if f1_bit!=None else print("<<FPGA1 is TURN OFF>>")
        print("<<FPGA2 is TURN ON>>") if f2_bit!=None else print("<<FPGA2 is TURN OFF>>")   

        path=f"DOWNLOADTEMP.txt"
        with open(path,"w")as f:
            f.close()
       
        f1_onstatus=1
        f2_onstatus=1
        if f1_bit==None: 
            f1_onstatus=0
            f1_bit=''
        if f2_bit==None:
            f2_onstatus=0
            f2_bit=''
        return_code=self.ppro.download_bit(f1_bit, f2_bit,path)
        if return_code!=0:
            return return_code
        
        with open(self.downloadtemp_path,"r")as f:
            item=f.readlines()
            if f1_onstatus==1:
                if ("[INFO] f1 download successful.\n") in item:
                    print("F1 DOWNLOAD SUCCESS!")
                    return_code=0
                else:
                    print("ERROR:F1 DOWNLOAD FAILED!")
                    return_code=1
            if f2_onstatus==1:
                if ("[INFO] f2 download successful.\n") in item:
                    print("F2 DOWNLOAD SUCCESS!")
                    return_code=0
                else:
                    print("ERROR:F2 DOWNLOAD FAILED!")
                    return_code=1
        return return_code


class runcall:

    def subpcall(cmd,time_out):
        p=Util.call(exec=cmd, timeout=time_out)
        if p!=0:
            print("COMMAND FAILED!\n")
            return 1
        else:
            print("COMMAND SUCCESS!\n")
        return 0
