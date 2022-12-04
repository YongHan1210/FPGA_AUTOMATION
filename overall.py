import subprocess,os,re,yaml,datetime,time,s2cyh,argparse
from threading import Thread
from s2cyh import S2cPlayerPro as S2cPlayerProyh

class yamld:

    def __init__(self,modulename):
        self.modulename=modulename
        
        self.hostname=self.getdata()[self.modulename]["fpga"]["hostname"]
        self.powermodule_ip=self.def_powermodule_ip()
        self.power_1_8V=self.getdata()[self.modulename]["fpga"]["power_1_8V"]
        self.power_3_3V=self.getdata()[self.modulename]["fpga"]["power_3_3V"]
        self.power_5_0V=self.getdata()[self.modulename]["fpga"]["power_5_0V"]
        self.S2CCLK_1=self.getdata()[self.modulename]["fpga"]["S2CCLK_1"]
        self.S2CCLK_2=self.getdata()[self.modulename]["fpga"]["S2CCLK_2"]
        self.S2CCLK_3=self.getdata()[self.modulename]["fpga"]["S2CCLK_3"]
        self.S2CCLK_4=self.getdata()[self.modulename]["fpga"]["S2CCLK_4"]
        self.S2CCLK_5=self.getdata()[self.modulename]["fpga"]["S2CCLK_5"]
        self.S2CCLK_6=self.getdata()[self.modulename]["fpga"]["S2CCLK_6"]
        self.S2CCLK_7=self.getdata()[self.modulename]["fpga"]["S2CCLK_7"]
        self.S2CCLK_8=self.getdata()[self.modulename]["fpga"]["S2CCLK_8"]
        self.fpga1_bitfile=self.getdata()[self.modulename]["fpga"]["fpga1_bitfile"]
        self.fpga2_bitfile=self.getdata()[self.modulename]["fpga"]["fpga2_bitfile"]
        
    def getdata(self):
        with open("hello.yaml","r") as f:
            data=yaml.safe_load(f)
            return data
    def def_powermodule_ip(self):
        fpga=s2cyh.S2C_FPGAS[self.hostname]
        return(fpga.get_pwrctrl_ip())
    def getlistvar(self):
        listvar=[self.getpower_1_8V(),self.getpower_3_3V(),self.getpower_5_0V(),self.getS2CCLK_1(),self.getS2CCLK_2(),self.getS2CCLK_3(),self.getS2CCLK_4(),self.getS2CCLK_5(),self.getS2CCLK_6(),self.getS2CCLK_7(),self.getS2CCLK_8(),self.getfpga1_bitfile(),self.getfpga2_bitfile(),self.gethostname(),self.getpowermodule_ip()]
        return listvar
    def getmodulename(self): return (self.modulename)
    def gethostname(self): return (self.hostname)
    def getpowermodule_ip(self): return (self.powermodule_ip)
    def getpower_1_8V(self): return (self.power_1_8V)
    def getpower_3_3V(self): return (self.power_3_3V)
    def getpower_5_0V(self): return (self.power_5_0V)
    def getS2CCLK_1(self): return (self.S2CCLK_1)
    def getS2CCLK_2(self): return (self.S2CCLK_2)
    def getS2CCLK_3(self): return (self.S2CCLK_3)
    def getS2CCLK_4(self): return (self.S2CCLK_4)
    def getS2CCLK_5(self): return (self.S2CCLK_5)
    def getS2CCLK_6(self): return (self.S2CCLK_6)
    def getS2CCLK_7(self): return (self.S2CCLK_7)
    def getS2CCLK_8(self): return (self.S2CCLK_8)
    def getfpga1_bitfile(self): return (self.fpga1_bitfile)
    def getfpga2_bitfile(self): return (self.fpga2_bitfile)



class automationmain:
    def __init__(self,modulename,listvar):
        self.modulename=modulename
        self.listvar=listvar
        self.J11power=self.listvar[0]
        self.J9power=self.listvar[1]
        self.J8power=self.listvar[2]
        self.fpga1bitfile=self.listvar[11]
        self.fpga2bitfile=self.listvar[12]
        self.boardtype=self.listvar[13]
        self.powermodule_ip=self.listvar[14]
        
        self.listclk=[self.listvar[3],self.listvar[4],self.listvar[5],self.listvar[6],self.listvar[7],self.listvar[8],self.listvar[9],self.listvar[10]]
        
    def writeinterf(self,program_retry):
        interface="    TESTING RUN {} [{}]".format(program_retry,self.modulename)
        print("\t"*6,"-"*30)
        print("\t"*6,interface)
        print("\t"*6,"-"*30)
        
    def loopfunction(self,program_retry):
        self.writeinterf(program_retry)
        
        return_code=autofunc_onpow.fpga_onpower(self.powermodule_ip)
        if return_code!=0:
            return return_code  
          
        return_code=autofunc_clk.clockgenmain(self.listclk)
        if return_code!=0:
            return return_code

        return_code=autofunc_hardware.hardware()
        if return_code!=0:
            return return_code
         
        return_code=autofunc_download.download(self.fpga1bitfile,self.fpga2bitfile,self.boardtype)
        if return_code!=0:
            return return_code
        
        return_code=autofunc_clkdet.readcheckclkmain(self.boardtype,self.listclk)
        if return_code!=0:
            return return_code
        
        return_code=autofunc_onpow.daughthercard_onpower(self.J11power,self.J9power,self.J8power,self.powermodule_ip)
        if return_code!=0:
            return return_code  
        
        return return_code



class autofunc_offpow:
    def offpower(powermodule_ip):
        interface="      POWER OFF FPGA & DCARD"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall()

        cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J11 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J11 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J9 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J8 3_3V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J8 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J8 5_0V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 

        cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J6 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, S2C_POWER_BASE ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 

        print("Cooling down FPGA in 10 seconds...")
        countd.countdown(10)
        os.system('S2C_stm32_lwip.exe --ip ' + f'{powermodule_ip}' + ' --port 8080 --readEth > readEth.txt')
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


class countd():
    def countdown(t):
        while t:
            time.sleep(1)
            t-=1



class autofunc_onpow:
    
    def fpga_onpower(powermodule_ip):
        interface="    POWER ON FPGA"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall()

        j6status=0
        os.system('S2C_stm32_lwip.exe --ip ' + f'{powermodule_ip}' + ' --port 8080 --readEth > readEth.txt')
        with open(r"readEth.txt","r") as f:
            item=f.readlines()
            if 'J6:on\n' in item:
                j6status=1
        if j6status==1:
            print("S2C_POWER_BASE is already on.")
            return 0
        else:
            print("S2C_POWER_BASE is off.")
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J6 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, S2C_POWER_BASE ...")
            return_code=rc.subpcall(cmd,timeout=30)
            if return_code!=0:
                return return_code 
            print("Warming up FPGA in [20 seconds]...")
            countd.countdown(20)
            return return_code
    
    def daughthercard_onpower(powerJ11,powerJ9,powerJ8,powermodule_ip):  
        interface="  POWER ON DAUGHTHER CARD"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall()
        j11status=0
        j9status=0
        j8status=0
        run=0
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
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J11 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J11 1_8V ...")
                return_code=rc.subpcall(cmd,timeout=30)
                run+=1
        else:
            if j11status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J11 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J11 1_8V ...")
                return_code=rc.subpcall(cmd,timeout=30)
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
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J9 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J9 3_3V ...")
                return_code=rc.subpcall(cmd,timeout=30)
                run+=1
        else:
            if j9status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J9 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J9 3_3V ...")
                return_code=rc.subpcall(cmd,timeout=30)
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
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J8 --setpwr on"
                print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J8 5_0V ...")
                return_code=rc.subpcall(cmd,timeout=30)
                run+=1
        else:
            if j8status==1:
                cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J8 --setpwr off"
                print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J8 5_0V ...")
                return_code=rc.subpcall(cmd,timeout=30)
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



class autofunc_clk:

    def clockgenmain(listclk):
        exefileclk=r"C:\S2C\PlayerPro_Runtime\firmware\bin\s2cclockgen_vuls.exe"
        s2chome=r"C:\Users\mdc_fpga_2\.s2chome\/"
        boardtype=r"DUAL_VU19P"
        returncode=autofunc_clk.clockgen1(listclk,exefileclk,s2chome,boardtype)
        if returncode!=0:
            return returncode
        returncode=autofunc_clk.clockgen2(listclk,exefileclk,s2chome,boardtype)
        if returncode!=0:
            return returncode
        return returncode


    def clockgen1(listclk,exefileclk,s2chome,boardtype):
        rc=runcall()
        interface="      CLOCKGEN MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        cmd=r'{} -q --ind  --file {}  -r 112 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(exefileclk,s2chome,str(listclk[0]),str(listclk[1]),str(listclk[2]),str(listclk[6]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return rc.subpcall(cmd,timeout=30)

    def clockgen2(listclk,exefileclk,s2chome,boardtype):
        rc=runcall()
        cmd=r'{} -q --ind  --file {}  -r 113 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(exefileclk,s2chome,str(listclk[3]),str(listclk[4]),str(listclk[5]),str(listclk[7]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return rc.subpcall(cmd,timeout=30)

class autofunc_hardware:

    def hardware():
        exefilehardware=r"C:\S2C\PlayerPro_Runtime\bin\tools\S2C_HardWare.exe"
        s2chome=r"C:\Users\mdc_fpga_2\.s2chome\/"
        boardtype=r"DUAL_VU19P"
        rc=runcall()
        interface="      HARDWARE MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        cmd= r'{} -f {} --mode clk -b {}'.format(exefilehardware,s2chome,boardtype)
        print("\nRUNNING CMD:{}".format(cmd))
        return rc.subpcall(cmd,timeout=30)


class autofunc_download:
    
    def download(f1_bit,f2_bit,boardtype):
        interface="      DOWNLOAD MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        pprohome = os.getenv('RTHome')
        workdir = os.getenv('USERPROFILE')
        ppro=S2cPlayerProyh(pprohome, workdir)
        ppro.select_target_hardware(boardtype)
        
        
        if f1_bit!=None:
            print("<<FPGA1 is TURN ON>>")
            ppro.download_bit(f1_bit, '')
        else: 
            print("<<FPGA1 is TURN OFF>>")
            
        if f2_bit!=None:
            print("<<FPGA2 is TURN ON>>")
            ppro.download_bit('', f2_bit)
        else: 
            print("<<FPGA2 is TURN OFF>>")
        return 0


class autofunc_clkdet:
 
    
    def getpath():
        return os.getcwd()

    def readcheckclkmain(boardtype,listclk=None):
        autofunc_clkdet.readclock(boardtype,listclk)
        if listclk!=None:
            clkdetret=autofunc_clkdet.clkchecking(listclk)
            return clkdetret
        else:
            return 0


    def readclock(boardtype,inputclk_list=None):
        desarr=[" << A1 >>"," << A2 >>"," << A3 >>","<< B1 >>","<< B2 >>","<< B3 >>","<< A4 >>","<< B4 >>"]
        interface="    READCLOCK MODULE"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        pprohome = os.getenv('RTHome')
        workdir = os.getenv('USERPROFILE')
        ppro=S2cPlayerProyh(pprohome, workdir)
        ppro.select_target_hardware(boardtype)
        pathx=f"{autofunc_clkdet.getpath()}/CLKTEMP.txt"
        with open(pathx,"w")as f:
            f.close()
        ppro.read_hwinfo(pathx)
        if inputclk_list!=None:
            print("\t\t\t         PLAYER PRO CLOCK\t                   INPUT CLOCK")
        else:
             print("\t"*6,"    PLAYER PRO CLOCK")
        fileread=open(pathx,"r")
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
     
    def clkchecking(listclk,path1=None,path2=None):
        pathx=f"{autofunc_clkdet.getpath()}/CLKTEMP.txt"
        interface="    CLOCKCHECKING MODULE"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        lisy=[]
        i=0
        with open(pathx,"r")as f:
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




class runcall:

        
    def subpcall(self,cmd,timeout):
        p=self.call(cmd, timeout)
        if p!=0:
            print("COMMAND FAILED!\n")
            return 1
        else:
            print("COMMAND SUCCESS!\n")
        return 0
    
    def call(self, exec, timeout=None ):
        SUCCESS=0
        FAILURE=1
        TIMEOUT=2
        args=exec
        process = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        def runa(process, args):
            while process.poll() is None:
                line = process.stdout.readline()
                try:
                    line = line.strip().decode('ansi')
                except:
                    line = line.strip().decode('utf-8')
                if line!='':
                    print(f'{line}')
            if process.returncode!=0:
                error=process.stderr
                print("ERROR:: {}".format(error))
        daemon = False if timeout is None else True
        t = Thread(target=runa, args=(process, args), daemon=daemon)
        t.start()
        if daemon:
            t.join(timeout)
            # kill the process if timeout
            if process.poll() is None:
                process.kill()
                print("TIMEOUT!!")
                return TIMEOUT
            return SUCCESS if process.returncode==0 else FAILURE
        return process




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