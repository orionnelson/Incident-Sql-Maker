import os
import subprocess
class IncidentManager:
    """
    Initialize the IncidentManager with the given incident name and description.
    The incident name is used as is, and the description is modified by replacing spaces with underscores
    and capitalizing the first letter of each word.
    :param incident_name: The name of the incident.
    :type incident_name: str
    :param description: A short description of the incident.
    :type description: str
    """
 
 
    # Global Variables For the Top of SQL Documents with the Main Script Made
    global user
    #Subprocess to Get The Users Information From the System like a spy haha
    command = "wmic useraccount where name='%USERNAME%' get fullname"
    # Execute the command and capture the output
    full_name = subprocess.run(command, capture_output=True, text=True, shell=True)
    username = subprocess.run(["echo","%USERNAME%"], capture_output=True, text=True, shell=True)
    user = f"{username.stdout.strip().upper()} - {full_name.stdout.replace('FullName','').strip()}"
         
 
    def __init__(self, incident_name: str, description: str):
        self.incident_name = incident_name
        self.description = '_'.join(word.capitalize() for word in description.split())
        self.full_ticket = f"{self.incident_name}_{self.description}"
        self.generate_header() # Make Header
        assert (self.header)
 
    def generate_header(self):
        """
        Create the header for the top of the sql file that is used for the main script of the ticket.
        :return: str
        """
        sql_header  =f"""---------------------------------------------------
-- Requested by: {user}
-- Incident Description: {self.description.replace("_"," ")} 
-- Database Name: SMXP 
-- Ticket {self.incident_name}
-- -------------------------------------------------"""
        self.header = sql_header
         
    
 
    def create_structure(self) -> None:
        """
        Create the directory and file structure for the incident.
        :return: None
        """
        original_dir_name = self.full_ticket
        os.makedirs(f"{original_dir_name}/backup", exist_ok=True)
        with open(f"{original_dir_name}/{original_dir_name}.sql", 'w') as f:
            f.write(f"-- {self.header}\n")
        with open(f"{original_dir_name}/backup/SEL_{self.incident_name.upper()}.sql", 'w') as f:
            f.write(f"-- {self.header}\n")
 
    def create_backups(self, backup_count: int) -> None:
        """
        Create backup SQL templates based on user input.
        :param backup_count: The number of backups to create.
        :type backup_count: int
        :return: None
        """
        for _ in range(backup_count):
            backup_name = input("Enter the name for this backup: ")
            #BackUp Name Format 
            if backup_name.lower() == 'b':
                print("Going back one step.")
                return
            backup_name = '_'.join(word.capitalize() for word in backup_name.split())
 
            file_name = f"Backup_{self.incident_name.upper()}_{backup_name}.sql"
            with open(f"{self.full_ticket}/backup/{file_name}", 'w') as f:
                f.write(f"-- {backup_name}\n")
 
 
def main():
    while True:
        incident_name = input("Enter the Incident Number String: ")
        if incident_name.lower() == 'b':
            print("No previous step to go back to.")
            continue
        description = input("Enter a short description of the incident: ")
        if description.lower() == 'b':
            continue
        manager = IncidentManager(incident_name, description)
        manager.create_structure()
 
        try:
            backup_count = int(input("Enter the number of backups to be made: "))
        except ValueError:
            print("Invalid number. Please enter a valid integer.")
            continue
 
        manager.create_backups(backup_count)
        break
 
if __name__ == "__main__":
    ct = 'y'
    while ct not in 'n':
        main()
        ct = input('continue(y/n):')
        ct = next(iter(['y' if ct not in ['n',''] else 'n']),'n')
