# FPGA_AUTOMATION

## Variable Storing
  By using Yaml File, with scheme format shown in Figure below and Ctrl+Space and press Enter to obtain the shortpaste of the all the variable needed.
  
  The *(modulename) of the test would be test_4 as an example in the figure shown
  
  ![Screenshot (7)](https://user-images.githubusercontent.com/119376600/210708654-df2d08a9-705e-46e4-9a52-c2c95ba2b8aa.png)  

## Run Whole Automation progress
1) run restructTesting.py by using command [python restructTesting.py (modulename) ] 

    *(modulename) needed to be insert by user which direct to the modulename in yaml file
  
2) execute the runtesthdw.bat with the modulename stated in the batch file 

## Run specific function in automation
### 1) ON OFF FPGA
        TURN ON FPGA: run argparsefunction.py by using command [python argparsefunction.py -f1]
        TURN OFF FPGA: run argparsefunction.py by using command [python argparsefunction.py -f0]
### 2) ON OFF DAUGHTER CARD
        TURN ON DC for 5V: run argparsefunction.py by using command [python argparsefunction.py -dc1 -5_0]
        TURN OFF DC for 5V: run argparsefunction.py by using command [python argparsefunction.py -dc0 -5_0]
        ####note: 5_0 status can be changed to 3_3 or 1_8 for 3.3V or 1.8V respectively
### 3) DOWNLOAD BITFILE
        run argparsefunction.py by using command [python argparsefunction.py -d --m (modulename)]
    
### 4) CLOCK GENERATION
        run argparsefunction.py by using command [python argparsefunction.py -c --m (modulename)]

### 5) MAIN AUTOMATION FLOW
        run argparsefunction.py by using command [python argparsefunction.py -a --m (modulename)]
        
## MORE INFORMATION
   a) Format checking for variable in yaml file is in json schema
   
   b) Functions for automation progress is coded in rT_function.py
   
   c) CLKTEMP.txt is for data checking of clock generation function
   
   d) DOWNLOADTEMP.txt is for data checking of download function
   
   e) readEth.txt is for data checking of ON OFF of FPGA & Daughtercard
