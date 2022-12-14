from overall import runcall
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
if __name__ == '__main__':
    return_code=autofunc_hardware.hardware()
    print(return_code)
    