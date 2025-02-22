# This script stops any running Redis instance and starts a new Redis server in WSL, and opens a Python window from the backend directory.

# Stop the Redis service if it's running
wsl sudo systemctl stop redis

# Kill any running Redis processes
wsl sudo pkill redis

# Start the Python CLI in a separate window, from the backend directory
Start-Process "cmd.exe" -ArgumentList '/c cd backend && python.exe -m cli.main run'

# Start the frontend development server in a separate window
Start-Process "cmd.exe" -ArgumentList '/c cd frontend && npm run dev'

# Start the Redis server in a separate window
Start-Process "cmd.exe" -ArgumentList '/c wsl redis-server'

# Display a message indicating the script has run
Write-Host "Redis server has been started in WSL"
