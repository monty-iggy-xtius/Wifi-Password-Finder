import sys
import subprocess
import re
import threading

# pattern to match wifi names i.e a colon then space then the name of the wifi network on the windows coomand line
valid_names = re.compile(": [a-zA-Z0-9\\\@\_\#\!\\?\,\.\>\<\%\&\-\$\^\(\)\ ]+")

# password combination
passwds = re.compile(
    "Key Content            : [a-zA-Z0-9\\\@\_\#\!\\?\,\.\>\<\%\&\-\$\^\(\)\ ]+")

# command prompt commands
get_all_networks = "netsh wlan show profile"


def check_compatibility():
	# get the current platform the script is being run on
    machine_version = sys.platform

    # if it's not a windows OS quit
    if "win" not in machine_version:
        print("[Error]: Please run this script on a windows operating system")
        sys.exit(0)
    else:
        result = find_passwords()

        print(" WIFI NAME ", "\t \t",  " PASSWORD ")
        print(43*"=")
        for wifi_name, wifi_pass in result.items():
            print(wifi_name, "\t \t", wifi_pass)


def find_passwords() -> dict:
    # dictionary to store the final results
    final_results = {}

    # get the output of the command and store it in a variable
    get_output = subprocess.run(
        get_all_networks, capture_output=True).stdout.decode()

    # use the regex to find all matching strings
    result = valid_names.findall(get_output)

    # remove the colon in the final results
    new_result = [value.replace(": ", "").strip() for value in result]

    # for each network try to find it's password
    for network in new_result:
        try:
            passwd_output = subprocess.run(f'netsh wlan show profile "{network}" key=clear', capture_output=True, shell=False).stdout.decode()

            passwd_result = passwds.findall(passwd_output)
            new_passwd_result = [pass_value.replace(
                "Key Content            : ", "").strip() for pass_value in passwd_result]
            # create a dictionary with the wifi name as the key and the wifi password as the value
            final_results[network] = new_passwd_result[0]
        except Exception as err:
            # if an error occurs the value of the wifi name is set to ERROR
            final_results[network] = " ---- "
            continue

    return final_results


if __name__ == '__main__':
    target = threading.Thread(target=check_compatibility)
    target.start()
