# Set execution policy for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Email configuration
$smtpServer = "smtp-relay.gmail.com"
$smtpPort = 25
$emailFrom = "it@rushordertees.com"
$emailTo = "d.patel@printfly.com"
$subject = "High Disk Usage Alert"
$logFilePath = "C:\Users\Public\DiskErrorLog.txt"
$hostname = hostname

# Calculate 24 hours ago
$timeThreshold = (Get-Date).AddHours(-24)

try {
    # Retrieve disk errors from the last 24 hours
    $errors = Get-EventLog -LogName System -Source "Microsoft-Windows-Ntfs" | Where-Object {
        $_.EntryType -eq "Error" -and
        $_.EventID -in 7,11,15,51,55,153,157,52,129,132,133 -and
        $_.TimeGenerated -ge $timeThreshold
    }

    # If errors are found, send an email
    if ($errors) {
        $body = "A disk error has been detected in the last 24 hours:`n" + $hostname
        $body += ($errors | Format-List -Property TimeGenerated,Message | Out-String)
        Send-MailMessage -From $emailFrom -To $emailTo -Subject $subject -Body $body -SmtpServer $smtpServer -Port $smtpPort -UseSsl
        $body | Out-File $logFilePath -Append
        Write-Host "Email Sent"
    } else {
        Write-Host "No Disk Error in the Last 24 Hours"
    }
} catch {
    $_ | Out-File $logFilePath -Append
    Write-Error "An error occurred: $_"
}

# Exit script properly
exit 0
