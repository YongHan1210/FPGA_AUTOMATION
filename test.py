class FPGA_param:
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
                self.bitfile_fpga1 = data['fpga1_bitfile']
                self.bitfile_fpga2 = data['fpga2_bitfile']


import yaml
if __name__ == '__main__':

        module='test_1'
        with open("hello.yaml") as file:
                data = yaml.load(file, yaml.SafeLoader)
        fpga = FPGA_param(data, module)
        