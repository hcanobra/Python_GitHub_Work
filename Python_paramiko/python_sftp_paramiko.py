import paramiko
from getpass import getpass
import os
 
# ///////// BEGIN 
os.system('clear')

v_mec_path = "/Users/hcanobra/Documents/Dreamscape_pcap/"
os.chdir(v_mec_path)

username=''
password=''

if not username:
    username = 'sftpuser'
    
if not password:
    password = getpass("Password: ")
    
dir_list = os.listdir(v_mec_path)
dir_list = sorted(dir_list)

with paramiko.SSHClient() as ssh:
    
    ssh.load_system_host_keys()
        
    ssh.connect("15.181.163.0", username=username, password=password)

    sftp = ssh.open_sftp()
                
    for file in dir_list:
        if file.endswith(".pcap"):
            print ("#######################################")
            os.system('date')
            
            print ("1) Processing file: ",file)
            
            sftp.put(file, file)
                    
            print ("2) Done with file.....",file)    
            os.system('date')
            print ("#######################################")
            
# ///////// END