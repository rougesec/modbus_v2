#!/bin/bash

# Function to print the header with an attractive CLI interface
function print_header() {
    clear
    echo -e "\e[1;34m=====================================================\e[0m"
    echo -e "\e[1;36m#          Welcome to the MODBUS LAB                #\e[0m"
    echo -e "\e[1;34m=====================================================\e[0m"
    echo -e "\n\e[32mDeveloped by RougeSec Academy\e[0m"
    echo -e "\n"
}

# Function to display the About section
function show_about() {
    print_header
    echo -e "\e[1;32mAbout this Tool:\e[0m"
    echo -e "This is a simple lab manager for controlling and monitoring your system lab setup."
    echo -e "It can start and stop the server, HMI, and simulation services."
    echo -e "You can also check the status of the lab and view the log files."
    echo -e "\n\e[1;33mUsage:\e[0m"
    echo -e "  ./start_lab.sh {start|stop|status|help}"
    echo -e "\n\e[1;33mOptions:\e[0m"
    echo -e "  \e[32mstart\e[0m   - Start the lab (server, HMI, and simulation)"
    echo -e "  \e[31mstop\e[0m    - Stop the running lab"
    echo -e "  \e[33mstatus\e[0m  - Check if the lab is running"
    echo -e "  \e[1;34mhelp\e[0m    - Show help information"
    echo -e "\n\e[32mDeveloped by RougeSec Academy\e[0m"
    echo -e "\n"
}

# Function to start the lab
function start_lab() {
    print_header
    echo -e "\e[32mStarting Lab...\e[0m"
    source modbus_env/bin/activate
    # Start server, HMI, and simulation in the background with nohup
    nohup python3 server.py > server.log 2>&1 & echo $! > server.pid
    nohup python3 hmi.py > hmi.log 2>&1 & echo $! > hmi.pid
    nohup python3 simulation.py > simulation.log 2>&1 & echo $! > simulation.pid

    # Wait a bit to ensure the services have started
    sleep 3

    echo -e "\e[32mLab Started Successfully!\n- HMI: http://localhost:5001\n- Simulation: http://localhost:5002\e[0m"
    echo -e "Check the logs for any errors:"
    echo -e "- server.log\n- hmi.log\n- simulation.log"
}

# Function to stop the lab
function stop_lab() {
    print_header
    echo -e "\e[31mStopping Lab...\e[0m"
    
    if [[ -f server.pid && -f hmi.pid && -f simulation.pid ]]; then
        kill $(cat server.pid) $(cat hmi.pid) $(cat simulation.pid) 2>/dev/null
        rm -f *.pid
        echo -e "\e[31mLab Stopped Successfully.\e[0m"
    else
        echo -e "\e[33mLab is not running.\e[0m"
    fi
}

# Function to check the status of the lab
function check_status() {
    print_header
    echo -e "\e[33mChecking Lab Status...\e[0m"
    
    if [[ -f server.pid && -f hmi.pid && -f simulation.pid ]]; then
        echo -e "\e[32mLab is running:\n- HMI: http://localhost:5001\n- Simulation: http://localhost:5002\e[0m"
    else
        echo -e "\e[31mLab is not running.\e[0m"
    fi
}

# Function to display help
function show_help() {
    print_header
    echo -e "\e[1;33mUsage:\e[0m"
    echo -e "  $0 {start|stop|status|help}"
    echo -e "\n\e[1;33mOptions:\e[0m"
    echo -e "  \e[32mstart\e[0m   - Start the lab (server, HMI, and simulation)"
    echo -e "  \e[31mstop\e[0m    - Stop the running lab"
    echo -e "  \e[33mstatus\e[0m  - Check if the lab is running"
    echo -e "  \e[1;34mhelp\e[0m    - Show this help message"
    echo -e "\n\e[32mDeveloped by RougeSec Academy\e[0m"
    echo -e "\n"
}

# Check if the script is run with any argument
if [ -z "$1" ]; then
    # If no argument is passed, show the about and help section
    show_about
    exit 0
fi

# Main control flow based on the user input
case $1 in
    start) start_lab ;;
    stop) stop_lab ;;
    status) check_status ;;
    help) show_help ;;
    *) echo -e "\e[31mInvalid option. Please use {start|stop|status|help}.\e[0m" ;;
esac

