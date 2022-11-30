#Sonicwall Object Extractor
takes a .mri tsr file from sonicwall and extracts network objects. The output is exported to 4 csv files sonicwallobjects.csv, sonicwallobjectgroups.csv , sonicwallserviceobjects.csv, and sonicwallservicegroups.csv. 

an example terminal usage  is 

python sonicwall_tsr_to_excel.py "filepath"

ie
python sonicwall_tsr_to_excel.py C:/Users/lucidity/Downloads/techSupport_8FF542_11-16.wri

We plan to also extract firewall rules and NAT rules. 
