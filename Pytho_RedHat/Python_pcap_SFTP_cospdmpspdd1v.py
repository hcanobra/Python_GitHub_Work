import paramiko
from getpass import getpass
import os
 
# ///////// BEGIN 
os.system('clear')

v_cs_path = "/home/canobhu/Files/pcap_resources"
os.chdir(v_cs_path)

username=''
password=''

if not username:
    username = 'sftpuser'
    
if not password:
    password = getpass("Password: ")
    

with paramiko.SSHClient() as ssh:
    
    ssh.load_system_host_keys()
        
    ssh.connect("15.181.163.0", username=username, password=password)

    sftp = ssh.open_sftp()
    #sftp.chdir('/home/canobhu/Files/pcap_resources')

    dir_list = sftp.listdir()
                
    for file in dir_list:
        if file.endswith(".pcap"):
            print ("#######################################")
            os.system('date')
            
            sftp.get(file, file)
                    
            print ("2) Done with file.....",file)    
            os.system('date')
            print ("#######################################")
            
# ///////// END

