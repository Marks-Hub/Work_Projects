@This script adds windows devices to Domain
 # Define the variables
$domain = "REDACTED.local" # Replace with your domain name
#$ouPath = "OU=Computers,DC=yourdomain,DC=local" # Replace with the Organizational Unit (OU) path where you want to place the computer
$computerName = $env:COMPUTERNAME
$domainUsername = "REDACTED\REDACTED" # Replace with a domain admin username
$domainPassword = "REDACTED" # Replace with the password of the domain admin

# Create a secure password object
$securePassword = ConvertTo-SecureString $domainPassword -AsPlainText -Force

# Create a PSCredential object
$credential = New-Object System.Management.Automation.PSCredential($domainUsername, $securePassword)

# Add the computer to the domain
Add-Computer -DomainName $domain -Credential $credential -Restart  #-OUPath $ouPath

# If you want to specify a new computer name, you can use the -NewName parameter
# Add-Computer -DomainName $domain -OUPath $ouPath -Credential $credential -NewName "NewComputerName" -Restart


