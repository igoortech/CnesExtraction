# CnesExtraction

> Status: ready to homolog ⚠️

### This RPA Solution must open Cnes, search for 5 states from Brazil, get data from 5 tables,open each row and download its PDF saving  at folder output

## STEP-1 SET THE VARIABLES INPUT ON  main.py⚠️
+ ##### THE INPUT FILE MUST BE AT ./Input folder  
+  inputfile.csv is that with all 5 states
+ ##################################################
+ #BOT NAME
+ bot_name = "cnesExtraction"
+ #FOLDER OUTPUT AND FILE NAME
+ Output = fr".\Output\${estado}$_cnes.xlsx" 
+ #FOLDER OUTPUT AND FILE NAME 
+ caminho_arquivo = fr".\Output\${cnes}$.pdf"

## STEP-2 THE MAIN.PY 
+  it has all step by step from the process 
+ it will perform some validations,excptions and follow the process.


## STEP-3 FOLDERS STRUCTURES
+ common_funcoes has all basic most used function to help 
+ common_selenium has all most used and necessary logic from selenium
+ output is the folder where logs and outputs must be saves


### Technologies Used:
<table>
  <tr>
  <td>Python</td>
  <td> chromedriver-autoinstaller</td>
  </tr>
  <td>3.10.0</td>
  <td>0.2.2</td>
  <tr>
  </tr> 
</table>

## How to run the application:
#### Install: Python
#### Run create_env.bat (it will create the env necessary, activate it and install all necessary requeriments.txt)⚠️⚠️⚠️⚠️⚠️⚠️⚠️
