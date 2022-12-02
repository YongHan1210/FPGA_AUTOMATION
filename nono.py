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



class mkfolfildir:
    
    def __init__(self,bitfpga1,bitfpga2):
        self.bitfpga1=bitfpga1
        self.bitfpga2=bitfpga2
            
    def mainff(self):
        if self.bitfpga1!=None:
            fop1=self.mkfolderpath1(self.bitfpga1[18:22])
            fpga1path=self.mkfilepath(fop1,self.bitfpga1[18:22],fpgan=r'fpga1')
        else:fpga1path=''
        
        if self.bitfpga2!=None:
            fop2=self.mkfolderpath1(self.bitfpga2[18:22])
            fpga2path=self.mkfilepath(fop2,self.bitfpga2[18:22],fpgan=r'fpga2')
        else:fpga2path=''
        return fpga1path,fpga2path
        
    
    def mkfolderpath1(self,dir):
        def mkdira(path):
            try:
                os.mkdir(path)
            except OSError as error:
                return
        path=r"{}\OUTPUT\{}".format(os.getcwd(),dir)
        mkdira(path)
        return path
    
    def mkfilepath(self,dir,bit,fpgan):
        td=datetime.datetime.now()
        path=r"{}\{}.txt".format(dir,r"[{}_{}_{}_{}_{}_{}]_[{}]_[{}]_output".format(td.year,td.month,td.day,td.hour,td.minute,td.second,bit,fpgan))
        with open(path,"w")as f:
            f.close()
        return path

class automationmain:
    def __init__(self,modulename,boardtype,powermodule_ip,listvar,fpga1outpath=None,fpga2outpath=None):
        self.modulename=modulename
        self.boardtype=boardtype
        self.powermodule_ip=powermodule_ip
        self.listvar=listvar
        self.J11power=self.listvar[0]
        self.J9power=self.listvar[1]
        self.J8power=self.listvar[2]
        self.fpga1bitfile=self.listvar[11]
        self.fpga2bitfile=self.listvar[12]
        
        self.listclk=[self.listvar[3],self.listvar[4],self.listvar[5],self.listvar[6],self.listvar[7],self.listvar[8],self.listvar[9],self.listvar[10]]
        
        self.path1=fpga1outpath
        self.path2=fpga2outpath

    

    def writeinterf(self,program_retry):
        interface="    TESTING RUN {} [{}]".format(program_retry,self.modulename)
        print("\t"*6,"-"*30)
        print("\t"*6,interface)
        print("\t"*6,"-"*30)
        writetof.wf(" TESTING RUN {}".format(program_retry),self.path1)
        writetof.wf(" TESTING RUN {}".format(program_retry),self.path2)
        
    
    def loopfunction(self,program_retry):
        self.writeinterf(program_retry)
        
        return_code=autofunc_onpow.fpga_onpower(self.powermodule_ip,self.path1,self.path2)
        if return_code!=0:
            return return_code  
          
        return_code=autofunc_clk.clockgenmain(self.listclk,self.path1,self.path2)
        if return_code!=0:
            return return_code

        return_code=autofunc_hardware.hardware(self.path1,self.path2)
        if return_code!=0:
            return return_code
         
        return_code=autofunc_download.download(self.fpga1bitfile,self.fpga2bitfile,self.boardtype,self.path1,self.path2)
        if return_code!=0:
            return return_code
        
        return_code=autofunc_clkdet.readcheckclkmain(self.boardtype,self.listclk,self.path1,self.path2)
        if return_code!=0:
            return return_code
        
        return_code=autofunc_onpow.daughthercard_onpower(self.J11power,self.J9power,self.J8power,self.powermodule_ip,self.path1,self.path2)
        if return_code!=0:
            return return_code  
        
        return return_code


class autofunc_offpow:
    def offpower(powermodule_ip,path1=None,path2=None):
        interface="    POWER OFF FPGA & DCARD"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall(path1,path2)
        writetof.wf("OFFPOWER",path1)
        writetof.wf("OFFPOWER",path2)


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
        

        return return_code
    
class countd():
    def countdown(t):
        while t:
            time.sleep(1)
            t-=1

class autofunc_onpow:
    
    def fpga_onpower(powermodule_ip,path1=None,path2=None):
        interface="    POWER ON FPGA"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall(path1,path2)
        writetof.wf("ONPOWER",path1)
        writetof.wf("ONPOWER",path2)
        
        cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J6 --setpwr on"
        print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, S2C_POWER_BASE ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        print("Warming up FPGA in [20 seconds]...")
        countd.countdown(20)
        return return_code
    
    def daughthercard_onpower(powerJ11,powerJ9,powerJ8,powermodule_ip,path1=None,path2=None):  
        interface="  POWER ON DAUGHTHER CARD"
        print("\n","\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall(path1,path2)
        writetof.wf("ONPOWER",path1)
        writetof.wf("ONPOWER",path2)
        
        if powerJ11:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J11 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J11 1_8V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J11 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J11 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        
        if powerJ9:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J9 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J9 3_3V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J9 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J8 3_3V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        
        if powerJ8:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J8 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermodule_ip}, J8 5_0V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermodule_ip} --port 8080 --pwr J8 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermodule_ip}, J8 5_0V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        print("Warming up DAUGHTER CARD in [20 seconds]...")
        countd.countdown(20)
        return return_code



class autofunc_clk:

    def clockgenmain(listclk,path1=None,path2=None):
        exefileclk=r"C:\S2C\PlayerPro_Runtime\firmware\bin\s2cclockgen_vuls.exe"
        s2chome=r"C:\Users\mdc_fpga_2\.s2chome\/"
        boardtype=r"DUAL_VU19P"
        returncode=autofunc_clk.clockgen1(listclk,exefileclk,s2chome,boardtype,path1,path2)
        if returncode!=0:
            return returncode
        returncode=autofunc_clk.clockgen2(listclk,exefileclk,s2chome,boardtype,path1,path2)
        if returncode!=0:
            return returncode
        return returncode

        
    def clockgen1(listclk,exefileclk,s2chome,boardtype,path1=None,path2=None):
        writetof.wf("CLOCKGEN",path1)
        writetof.wf("CLOCKGEN",path2)
        rc=runcall(path1,path2)
        interface="      CLOCKGEN MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        cmd=r'{} -q --ind  --file {}  -r 112 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(exefileclk,s2chome,str(listclk[0]),str(listclk[1]),str(listclk[2]),str(listclk[6]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return rc.subpcall(cmd,timeout=30)

    def clockgen2(listclk,exefileclk,s2chome,boardtype,path1=None,path2=None):
        rc=runcall(path1,path2)
        cmd=r'{} -q --ind  --file {}  -r 113 -i 50 -a {} -b {} -c {} -d {} -t {}'.format(exefileclk,s2chome,str(listclk[3]),str(listclk[4]),str(listclk[5]),str(listclk[7]),boardtype)
        print("\nRUNNING CMD: {} \n".format(cmd))
        return rc.subpcall(cmd,timeout=30)

class autofunc_hardware:

    def hardware(path1=None,path2=None):
        exefilehardware=r"C:\S2C\PlayerPro_Runtime\bin\tools\S2C_HardWare.exe"
        s2chome=r"C:\Users\mdc_fpga_2\.s2chome\/"
        boardtype=r"DUAL_VU19P"
        writetof.wf("HARDWARE",path1)
        writetof.wf("HARDWARE",path2)
        rc=runcall(path1,path2)
        interface="      HARDWARE MODULE"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        cmd= r'{} -f {} --mode clk -b {}'.format(exefilehardware,s2chome,boardtype)
        print("\nRUNNING CMD:{}".format(cmd))
        return rc.subpcall(cmd,timeout=30)

class writetof:
    def wf(interfacex,path=None):
        if path!="" and path!=None:
            with open (path, "a")as f:
                f.write("-"*30)
                f.write("\n")
                f.write(interfacex)
                f.write("\n")
                f.write("-"*30)
                f.write("\n")
                f.close()

class autofunc_download:
    
    def download(f1_bit,f2_bit,boardtype,path1=None,path2=None):
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
            writetof.wf("BOARD INFO",path1)
            ppro.read_hwinfo(path1)
            writetof.wf("DOWNLOAD MODULE",path1)
            ppro.download_bit(f1_bit, '',path1)
        else: 
            print("<<FPGA1 is TURN OFF>>")
            
        if f2_bit!=None:
            print("<<FPGA2 is TURN ON>>")
            writetof.wf("BOARD INFO",path2)
            ppro.read_hwinfo(path2)
            writetof.wf("DOWNLOAD MODULE",path2)
            ppro.download_bit('', f2_bit,path2)
        else: 
            print("<<FPGA2 is TURN OFF>>")
            # ppro.download_bit(f2_flag,f2_bit,self.path2,'2')
        #C:\project\Jh8100\0047 JH8100_P1V0P8P3SEP9_SCP_EXPORT\bit\JH8100_P1V0P8P3SEP9_SCP_rtlcedd25e_fpga2c3fa3f_P1_UV19P_2209100705.bit
        #f1_bit = f'C:\\project\\Jh8100\\0047 JH8100_P1V0P8P3SEP9_SCP_EXPORT\\bit\\JH8100_P1V0P8P3SEP9_SCP_rtlcedd25e_fpga2c3fa3f_P1_UV19P_2209100705.bit'
        return 0


class autofunc_clkdet:
 
    
    def getpath():
        return os.getcwd()

    def readcheckclkmain(boardtype,listclk=None,path1=None,path2=None):
        autofunc_clkdet.readclock(boardtype,listclk,path1,path2)
        if listclk!=None:
            clkdetret=autofunc_clkdet.clkchecking(listclk,path1,path2)
            return clkdetret
        else:
            return 0


    def readclock(boardtype,inputclk_list=None,path1=None,path2=None):
        writetof.wf("READ CLOCK",path1)
        writetof.wf("READ CLOCK",path2)
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
                    if path1!='' and path1!=None:
                        with open(path1,"a") as f:
                            f.write(overall)
                            f.write("\n")
                            f.close()
                    if path2!='' and path2!=None:
                        with open(path2,"a") as f:
                            f.write(overall)
                            f.write("\n")
                            f.close()
                else:
                    overall="\t\t{}  {}  ".format(end,g)
                    print("\t\t\t   {}".format(overall))
                    if path1!='' and path1!=None:
                        with open(path1,"a") as f:
                            f.write(overall)
                            f.write("\n")
                            f.close()
                    if path2!='' and path2!=None:
                        with open(path2,"a") as f:
                            f.write(overall)
                            f.write("\n")
                            f.close()
                i+=1
            print() 
     
    def clkchecking(listclk,path1=None,path2=None):
        pathx=f"{autofunc_clkdet.getpath()}/CLKTEMP.txt"
        writetof.wf("CHECK CLOCK",path1)
        writetof.wf("CHECK CLOCK",path2)
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
            if path1!='' and path1!=None:
                with open(path1,"a") as f:
                    f.write("CLOCK CHECKED SUCCESS")
                    f.close()
            if path2!=''and path2!=None:
                with open(path2,"a") as f:
                    f.write("CLOCK CHECKED SUCCESS")
                    f.close()
            return 0
        else:
            print("\t"*6,"ERROR:CLOCK CHECKED FAILED")
            if path1!='' and path1!=None:
                with open(path1,"a") as f:
                    f.write("CLOCK CHECKED FAILED")
                    f.close()
            if path2!='' and path2!=None:
                with open(path2,"a") as f:
                    f.write("CLOCK CHECKED FAILED")
                    f.close()
            return 1


class runcall:
    def __init__(self,path1=None,path2=None):
        self.path1=path1
        self.path2=path2
        
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
                    if self.path1!='' and self.path1!=None:
                        with open(self.path1,"a") as f:
                            f.write(f'{line}')
                            f.write("\n")
                            f.close()
                    if self.path2!='' and self.path2!=None:
                        with open(self.path2,"a") as f:
                            f.write(f'{line}')
                            f.write("\n")
                            f.close()
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
                if self.path1!='':
                    with open(self.path1,"a") as f:
                        f.write("ERROR:TIMEOUT")
                        f.write("\n")
                        f.close()
                if self.path2!='':
                    with open(self.path2,"a") as f:
                        f.write("ERROR:TIMEOUT")
                        f.write("\n")
                        f.close()
                return TIMEOUT
            return SUCCESS if process.returncode==0 else FAILURE
        return process





# if __name__ == '__main__':
    
#     parser = argparse.ArgumentParser()
#     parser.add_argument("modulename", help="check for the module name in yaml file",type=str)
#     args = parser.parse_args()
#     modulename=args.modulename

#     yamld=yamld(modulename)
#     hostname=yamld.gethostname()
#     powermoduleip=yamld.getpowermodule_ip()
#     print(powermoduleip)
#     listvar=[yamld.getpower_1_8V(),yamld.getpower_3_3V(),yamld.getpower_5_0V(),yamld.getS2CCLK_1(),yamld.getS2CCLK_2(),yamld.getS2CCLK_3(),yamld.getS2CCLK_4(),yamld.getS2CCLK_5(),yamld.getS2CCLK_6(),yamld.getS2CCLK_7(),yamld.getS2CCLK_8(),yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile()]
# #     # mk=mkfolfildir(yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile())
# #     # fpga1outpath,fpga2outpath=mk.mainff()
    
# #     # program_retry=1
# #     # auto=automationmain(modulename,hostname,powermoduleip,listvar,fpga1outpath,fpga2outpath)
# #     # #auto=automationmain(powermoduleip,hostname,yamld.getpower_1_8V(),yamld.getpower_3_3V(),yamld.getpower_5_0V(),yamld.getS2CCLK_1(),yamld.getS2CCLK_2(),yamld.getS2CCLK_3(),yamld.getS2CCLK_4(),yamld.getS2CCLK_5(),yamld.getS2CCLK_6(),yamld.getS2CCLK_7(),yamld.getS2CCLK_8(),yamld.getfpga1_bitfile(),yamld.getfpga2_bitfile(),fpga1outpath,fpga2outpath)
# #     # while(program_retry<4):
# #     #     return_code=auto.loopfunction(program_retry)
# #     #     if return_code==0:
# #     #         break
# #     #     else:
# #     #         autofunc_offpow.offpower(powermoduleip,fpga1outpath,fpga2outpath)
# #     #         program_retry+=1