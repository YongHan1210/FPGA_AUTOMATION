import sys, os, subprocess, threading
from utilsyh import Decorator, Util

class S2cFpga:
	LS_VU19P  = 'SINGLE_VU19P'
	LS_2VU19P = 'DUAL_VU19P'

	class Board:
		def __init__(self, targetFamily, module, fpga_cnt, s2cdownload, power_main='J6', power_front_5v='J8'):
			self.targetFamily   = targetFamily
			self.module         = module
			self.fpga_cnt       = fpga_cnt
			self.s2cdownload    = s2cdownload
			self.power_main     = power_main
			self.power_front_5v = power_front_5v
	CONFIGS = {
		LS_VU19P :Board('VU Prodigy Logic System', 'Single VU19P Prodigy Logic System', 1, 's2cdownload_vuls'),
		LS_2VU19P:Board('VU Prodigy Logic System', 'Dual VU19P Prodigy Logic System'  , 2, 's2cdownload_vuls'),
	}

	def __init__(self, hostname, hostip, boardtype, connection='USB', ip='', pwrctrl_ip=''):
		self.hostname   = hostname
		self.hostip     = hostip
		self.boardtype  = boardtype
		self.connection = connection
		self.ip         = ip
		self.pwrctrl_ip = pwrctrl_ip
		self.board      = S2cFpga.CONFIGS[boardtype]

	def get_hostname(self):
		return self.hostname
	
	def get_hostip(self):
		return self.hostip
	
	def get_boardtype(self):
		return self.boardtype
	
	def get_connection(self):
		return self.connection

	def get_ip(self):
		return self.ip
	
	def get_pwrctrl_ip(self):
		return self.pwrctrl_ip

	def get_fpga_cnt(self):
		return self.board.fpga_cnt

	def get_targetFamily(self):
		return self.board.targetFamily
	
	def get_module(self):
		return self.board.module
	
	def get_s2cdownload(self):
		return self.board.s2cdownload

S2C_FPGAS = {
	# name(=hostname): hostname, hostip, boardtype, connection='USB', ip='', pwrctrl_ip=''
	'2VU19P-120-24': S2cFpga('2VU19P-120-24', '', S2cFpga.LS_2VU19P),
	'2VU19P-120-25': S2cFpga('2VU19P-120-25', '', S2cFpga.LS_2VU19P),
	'VU19P-120-26' : S2cFpga('VU19P-120-26' , '', S2cFpga.LS_VU19P ),
	'VU19P-120-27' : S2cFpga('VU19P-120-27' , '', S2cFpga.LS_VU19P ),
	'2VU19P-120-29': S2cFpga('2VU19P-120-29', '', S2cFpga.LS_2VU19P),
	'2VU19P-120-30': S2cFpga('2VU19P-120-30', '', S2cFpga.LS_2VU19P),
	'Dual VU19P Prodigy Logic System': S2cFpga('Dual VU19P Prodigy Logic System', '192.168.152.253', S2cFpga.LS_2VU19P),
}

class S2cPlayerPro:
	@Decorator.logit
	def __init__(self, pprohome, workdir):
		self.s2chome  = os.path.join(workdir, '.s2chome')
		self.pprohome = pprohome
		Util.append_env('PATH', os.path.join(pprohome,'bin','tools'))
		Util.append_env('PATH', os.path.join(pprohome,'firmware', 'bin'))
		self.S2C_HardWare = 'S2C_HardWare'
		self.S2C_CPanel   = 'S2C_CPanel'
		self.s2cdownload  = None
		self.fpga         = None
		print(f'pproHome: {self.pprohome}')
		print(f's2chome:  {self.s2chome}')

	@Decorator.logit
	def select_target_hardware(self, hostname):
		r'''
		Create C:\Users\mdc_fpga_2\.s2chome\\mb_config.xml
		%USERPROFILE%\.s2chome

		mb_config.xml:
		<?xml version="1.0" encoding="UTF-8"?>
		<MB config="Standalone" connection="ETH" ip="" nm="Runtime" num="1"
			port="8080" targetFamily="VU Prodigy Logic System">
			<Board boardNo="1" connection="USB" ip=""
				module="Single VU19P Prodigy Logic System" port="8080" slot=""/>
		</MB>
		'''
		fpga = S2C_FPGAS[hostname]
		mb_config_xml = os.path.join(self.s2chome, 'mb_config.xml')
		with open(mb_config_xml, 'w') as f:
			f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
			f.write(f'<MB config="Standalone" connection="ETH" ip="" nm="Runtime" num="1"\n')
			f.write(f'	port="8080" targetFamily="{fpga.get_targetFamily()}">\n')
			f.write(f'	<Board boardNo="1" connection="ETH" ip="{fpga.get_hostip()}"\n')
			f.write(f'		module="{fpga.get_module()}" port="8080" slot="">\n')
			fpga_cnt = fpga.get_fpga_cnt()
			if fpga_cnt > 1:
				for i in range(1, fpga_cnt+1):
					f.write(f'		<Fpga fpgaNm="F{i}"/>\n')
			f.write(f'	</Board>\n')
			f.write(f'</MB>')
		self.fpga = fpga

	@Decorator.logit
	def set_main_power(self, on):
		r'''
		arg - which power to power on
		'''
		on_or_off = 'on' if on else 'off'
		return 0

	@Decorator.logit
	def is_main_power_on(self):
		return True

	@Decorator.logit
	def set_front_panel_power(self, voltage, on):
		return 0

	@Decorator.logit
	def is_front_panel_power_on(self, voltage):
		return True

	@Decorator.logit
	def read_hwinfo(self,path=None):
		r'''
		C:\S2C\PlayerPro_Runtime\bin\tools\S2C_HardWare.exe -d "C:\Users\mdc_fpga_2\.s2chome\\boardinfo_board1.xml" -b SINGLE_VU19P 
		%RTHome%\bin\tools\S2C_HardWare.exe
		'''
		output=os.path.join(self.s2chome, 'boardinfo_board1.xml')
		boardtype = self.fpga.get_boardtype()
		ret = Util.call(self.S2C_HardWare, ['-d', output, '-b', boardtype],path, timeout=10)
		#t = RunnableTask(self.S2C_HardWare, ['-d', output, '-b', self.boardtype], timeout=10)
		#ret = t.run()
		if ret==0:
			Util.cat(output,path)
			if(output.find("                        <S2CCLK1 fre=")!=-1):
				print(output)
		return ret

	@Decorator.logit
	def download_bit(self, f1, f2,path=None):

		def gen_download_xml(xml, f1, f2):
			with open(xml, 'w') as f:
				f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
				f.write(f'<Download project="Runtime">\n')
				f.write(f'	<Module idx="0">\n')
				f.write(f'		<Fpga file="" flag="off" idx="1"/>\n')
				f.write(f'	</Module>\n')
				f.write(f'	<Module boardType="DUAL160" idx="1">\n')
				f1_flag = 'off' if f1=='' else 'on'
				f.write(f'		<Fpga file="{f1}" flag="{f1_flag}" idx="1"/>\n')
				if f2 != None:
					f2_flag = 'off' if f2=='' else 'on'
					f.write(f'		<Fpga file="{f2}" flag="{f2_flag}" idx="2"/>\n')
				f.write(f'	</Module>\n')
				f.write(f'</Download>\n')
			Util.cat(xml,path)
		
		if self.fpga is None:
			print(f'Error: call select_target_hardware() first')
			return 1

		# generate download script
		download_xml = os.path.join(self.s2chome, 'board1_download_test.xml')
		gen_download_xml(download_xml, f1, f2)

		# download process
		boardtype = self.fpga.get_boardtype()
		#ret = RunnableTask(self.S2C_CPanel, ['--bus_mode  -b', self.boardtype], timeout=10).run()
		ret = Util.call(self.S2C_CPanel, ['--bus_mode', '-b', boardtype],path, timeout=10)
		if ret != 0:
			return 1
		#ret = RunnableTask(self.s2cdownload, ['-b', self.boardtype, '-f', download_xml], timeout=600).run()
		s2cdownload = self.fpga.get_s2cdownload()
		print("HERE")
		print(s2cdownload)
		ret = Util.call(s2cdownload, ['-b', boardtype, '-f', download_xml],path, timeout=600)
		if ret != 0:
			return 1

		return 0
	
	def set_clock(self):
		r'''
		C:\S2C\PlayerPro_Runtime\bin\tools\S2C_CPanel.exe --checkFpgaLock #mdc_fpga_2@@reserve@#1##1##0##0# -b DUAL_VU19P
		C:\S2C\PlayerPro_Runtime\bin\tools\S2C_CPanel.exe -b DUAL_VU19P -k 0
		C:\S2C\PlayerPro_Runtime\bin\tools\S2C_CPanel.exe --firmwareinfo -b DUAL_VU19P
		# depends on Board1_genClk.xml and will update boardinfo.xml
		C:\S2C\PlayerPro_Runtime\bin\tools\S2C_HardWare.exe -f "C:\Users\mdc_fpga_2\.s2chome\\" --mode clk  -b DUAL_VU19P
		

		Board1_genClk.xml:

		'''


if __name__ == '__main__':
	pprohome = os.getenv('RTHome')
	workdir = os.getenv('USERPROFILE')
	print(pprohome)
	print(workdir)
	ppro=S2cPlayerPro(pprohome, workdir)
	ppro.select_target_hardware('Dual VU19P Prodigy Logic System')
	ppro.read_hwinfo()
	ppro.set_main_power(on=True)
	if not ppro.is_main_power_on():
		print('failed to set main power on')
		exit(1)
	f1_bit = f'C:\\project\\Jh8100\\0047 JH8100_P1V0P8P3SEP9_SCP_EXPORT\\bit\\JH8100_P1V0P8P3SEP9_SCP_rtlcedd25e_fpga2c3fa3f_P1_UV19P_2209100705.bit'
	ppro.download_bit(f1=f1_bit,f2=f1_bit)
	ppro.set_front_panel_power('5', on=False)
	ppro.is_front_panel_power_on('5')

