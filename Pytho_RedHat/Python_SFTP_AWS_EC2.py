import paramiko
from getpass import getpass
import os
 
# ///////// BEGIN 
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"

username=''
password=''

dir_list = os.listdir(path)
dir_list = sorted(dir_list)

if not username:
    username = 'sftpuser'
    
if not password:
    password = getpass("Password: ")
    
    
for file in dir_list:
    if file.endswith(".pcap"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)
                
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
                
            ssh.connect("15.181.163.0", username=username, password=password)
        
            sftp = ssh.open_sftp()

            sftp.chdir('/home/sftpuser')
            
            sftp.put(file_name, file)

        print ("2) Done with file.....")
        
        os.system('date')
        print ("#######################################")
            
# ///////// END
