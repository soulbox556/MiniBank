class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def header(message):
    print(bcolors.HEADER+message+bcolors.ENDC)

def menu(message):
    print(bcolors.OKCYAN + bcolors.BOLD+message+bcolors.ENDC)

def warning(message):
    print(bcolors.WARNING+message+bcolors.ENDC)

def error(message):
    print(bcolors.FAIL+message+bcolors.ENDC)

def success(message):
    print(bcolors.OKGREEN+message+bcolors.ENDC)