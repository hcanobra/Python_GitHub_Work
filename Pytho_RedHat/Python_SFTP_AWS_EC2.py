import paramiko
from getpass import getpass
import os
 
# ///////// BEGIN 
os.system('clear')

path = "/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Dreamscape/NeckBand_proto/070123_1st_test/"

username=''
password=''

dir_list = os.listdir(path)
dir_list = sorted(dir_list)

if not username:
    username = 'sftpuser'
    
if not password:
    password = getpass("Password: ")
    
    
for file in dir_list:
    if file.__contains__("TCP_100M_070123"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)
                
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
                
            ssh.connect("15.181.163.0", username=username, password=password)
        
            sftp = ssh.open_sftp()

            sftp.chdir('/home/sftpuser/070123_1st_test')
            
            sftp.put(file_name, file)

        print ("2) Done with file.....")
        
        os.system('date')
        print ("#######################################")
            
# ///////// END
