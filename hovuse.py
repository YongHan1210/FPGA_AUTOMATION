import subprocess,os,re,yaml,datetime,time
from threading import Thread
from s2cyh import S2cPlayerPro as S2cPlayerProyh

class yamld:

    def __init__(self,listvar,path):
        self.path=path
        self.yamlfilepath=r"{}\hello.yaml".format(path)
        self.listname=['name','power_FPGA1','power_FPGA2','power_1_8V','power_3_3V','power_5_0V','S2CCLK_1','S2CCLK_2','S2CCLK_3','S2CCLK_4','S2CCLK_5','S2CCLK_6','S2CCLK_7','S2CCLK_8','fpga1_bitfile','fpga2_bitfile']
        self.listvar=listvar
        

    def yaml_loader(self):
        with open(self.yamlfilepath,"r")as f:
            data=yaml.safe_load(f)
            return data
    
    def yamlcheck(self):
        if self.listvar[1]:
            pass
        else:
            self.listvar[14]=''
        if self.listvar[2]:
            pass
        else:
            self.listvar[15]=''

    def yamlpassvar(self):
        i=0
        data=yamld.yaml_loader()
        while i< len(self.listname):
            items=data.get(self.listname[i])
            self.listvar.append(items)
            i+=1
        self.yamlcheck()
        

class mkfolfildir:
    
    def __init__(self,bitfpga1,bitfpga2,path):
        self.bitfpga1=bitfpga1
        self.bitfpga2=bitfpga2
        self.path=path
            
    def mainff(self):
        print(self.bitfpga1)
        print(self.bitfpga2)
        if self.bitfpga1!='':
            fb1=self.getbit1(self.bitfpga1)
            fop1=self.mkfolderpath1(fb1)
            fpga1path=self.mkfilepath(fop1,fb1,fpgan=r'fpga1')
        else:fpga1path=''
        if self.bitfpga2!='':
            fb2=self.getbit1(self.bitfpga2)
            fop2=self.mkfolderpath1(fb2)
            fpga2path=self.mkfilepath(fop2,fb2,fpgan=r'fpga2')
        else:fpga2path=''
        return fpga1path,fpga2path
        
    def getbit1(self,lv):
        return lv[18:22]
    
    def mkfolderpath1(self,dir):
        def mkdira(path):
            try:
                os.mkdir(path)
            except OSError as error:
                print('file exists')
                return
        print(dir)
        path=r"{}\OUTPUT\{}".format(self.path,dir)
        mkdira(path)
        return path
    
    def mkfilepath(self,dir,bit,fpgan):
        td=datetime.datetime.now()
        timedate=r"[{}_{}_{}_{}_{}_{}]_[{}]_[{}]_output".format(td.year,td.month,td.day,td.hour,td.minute,td.second,bit,fpgan)
        path=r"{}\{}.txt".format(dir,timedate)
        with open(path,"w")as f:
            f.close()
        return path

class automationmain:
    def __init__(self,path1,path2,path,powermoduleip,listvar):
        self.path1=path1
        self.path2=path2
        self.path=path
        self.listvar=listvar
        self.J11power=self.listvar[3]
        self.J9power=self.listvar[4]
        self.J8power=self.listvar[5]
        self.fpga1bitfile=self.listvar[14]
        self.fpga2bitfile=self.listvar[15]
        self.powermoduleip=powermoduleip
        self.listclk=[self.listvar[6],self.listvar[7],self.listvar[8],self.listvar[9],self.listvar[10],self.listvar[11],self.listvar[12],self.listvar[13]]
        self.boardtype=self.listvar[0]

    

    def writeinterf(self,program_retry):
        interface=" TESTING RUN {}".format(program_retry)
        print("\t"*6,"-"*30)
        print("\t"*7,interface)
        print("\t"*6,"-"*30)
        writetof.wf(" TESTING RUN {}".format(program_retry),self.path1)
        writetof.wf(" TESTING RUN {}".format(program_retry),self.path2)
        
    
    def loopfunction(self,program_retry):
        self.writeinterf(program_retry)
        
        return_code=autofunc_onpow.onpower(self.J11power,self.J9power,self.J8power,self.powermoduleip,self.path1,self.path2)
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
        
        return_code=autofunc_clkdet.readcheckclkmain(boardtype,self.listclk,self.path1,self.path2)
        if return_code!=0:
            return return_code
        
        return return_code


class autofunc_offpow:
    def offpower(powermoduleip,path1=None,path2=None):
        interface="    POWER OFF FPGA & DCARD"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall(path1,path2)
        writetof.wf("ONPOWER",path1)
        writetof.wf("ONPOWER",path2)


        cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J11 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J11 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J9 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J8 3_3V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
    

        cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J8 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J8 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 

        cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J6 --setpwr off"
        print(f"\n[INFO] Turn off PowerModule {powermoduleip}, S2C_POWER_BASE ...")
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
    
    def onpower(powerJ11,powerJ9,powerJ8,powermoduleip,path1=None,path2=None):
        interface="    POWER ON FPGA & DCARD"
        print("\t"*4,"*"*60)
        print("\t"*6,interface)
        print("\t"*4,"*"*60)
        rc=runcall(path1,path2)
        writetof.wf("ONPOWER",path1)
        writetof.wf("ONPOWER",path2)
        
        
        
        cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J6 --setpwr on"
        print(f"\n[INFO] Turn on PowerModule {powermoduleip}, S2C_POWER_BASE ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        
        if powerJ11:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J11 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermoduleip}, J11 1_8V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J11 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J11 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        
        if powerJ9:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J9 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermoduleip}, J9 3_3V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J9 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J8 3_3V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        
        if powerJ8:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J8 --setpwr on"
            print(f"\n[INFO] Turn on PowerModule {powermoduleip}, J8 1_8V ...")
        else:
            cmd=f"S2C_stm32_lwip.exe --ip {powermoduleip} --port 8080 --pwr J8 --setpwr off"
            print(f"\n[INFO] Turn off PowerModule {powermoduleip}, J8 1_8V ...")
        return_code=rc.subpcall(cmd,timeout=30)
        if return_code!=0:
            return return_code 
        print("Warming up FPGA in [20 seconds]...")
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
        
        
        if f1_bit!='':
            print("<<FPGA1 is TURN ON>>")
            writetof.wf("BOARD INFO",path1)
            ppro.read_hwinfo(path1)
            writetof.wf("DOWNLOAD MODULE",path1)
            ppro.download_bit(f1_bit, '',path1)
        else: 
            print("<<FPGA1 is TURN OFF>>")
            
        if f2_bit!='':
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




if __name__ == '__main__':
    listvar=[]
    path=r"C:\jenkins\workspace\Automation"
    yamld=yamld(listvar,path)
    yamld.yamlpassvar()
    print(listvar)
    mk=mkfolfildir(listvar[14],listvar[15],path)
    fpga1outpath,fpga2outpath=mk.mainff()
    powermoduleip='192.168.152.254'
    boardtype='Dual VU19P Prodigy Logic System'
    program_retry=1
    auto=automationmain(fpga1outpath,fpga2outpath,path,powermoduleip,listvar)
    while(program_retry<4):
        return_code=auto.loopfunction(program_retry)
        if return_code==0:
            break
        else:
            autofunc_offpow.offpower(powermoduleip,fpga1outpath,fpga2outpath)
            
            program_retry+=1