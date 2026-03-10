Import-CSV "C:\Users\USERNAME\Documents\AD employees\Extra People AD.csv" | ForEach-Object {
    $firstName = $_.FirstName
    $lastName = $_.LastName
    $fullName = "$firstName $lastName"
    $userName = $_.UserName
    $userPrincipalName = "$userName@REDACTED.LOCAL"
    
    New-ADUser -GivenName $firstName `
               -Surname $lastName `
               -Name $fullName `
               -UserPrincipalName $userPrincipalName `
               -SamAccountName $userName `
               -AccountPassword (ConvertTo-SecureString $_.Password -AsPlainText -Force) `
               -Enabled $true `
               -Path "OU=Domain Users,OU=Accounts,OU=Commerce,OU=REDACTED,DC=REDACTED,DC=local" `
               -PasswordNeverExpires $false `
               -ChangePasswordAtLogon $true `
               -PassThru
}

