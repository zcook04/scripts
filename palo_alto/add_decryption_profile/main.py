import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import argparse, sys

'''
## Creates set commands to update each decryption rule with a decryption profile specified.  The decryption profile needs to exist on the firewall.
## Sample command to run this script shown below.
## python3 main.py --config "/Users/username/Desktop/config.xml" --profile "Recommended-Decryption-Profile" --rulebase "pre-rulebase" --devicegroup "MyDG"
'''

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Source Panorama XML Configuration")
parser.add_argument("--profile", help="Name of the decryption profile you want to apply")
parser.add_argument("--rulebase", help="pre-rulebase or post-rulebase")
parser.add_argument("--devicegroup", help="device-group to configure")
parser.add_argument("--output", help="output filename to be created")
args = parser.parse_args()

## Validate Arguements
if not args.config:
    print('Panorama XML configuration is required.')
    sys.exit(1)

if not args.profile:
    print('Decryption profile name is required.')
    sys.exit(1)

if not args.rulebase:
    print('pre-rulebase or post-rulebase name is required.')
    sys.exit(1)

if not args.devicegroup:
    print('Device group is required.')
    sys.exit(1)

## Set CONSTANTS from the CLI arguments.
FILENAME = args.config
DECRYPTION_PROFILE = args.profile
RULE_BASE = args.rulebase
DEVICE_GROUP = args.devicegroup
OUTPUT = args.output or 'decryption-profile-output.txt'

## Parse XML
try:
    tree = ET.parse(FILENAME)
    root = tree.getroot()
except FileNotFoundError:
    print('File not found.  Panorama configuration not found, check filepath and filename given to the --config argument')
    sys.exit(1)
except ParseError as e:
    print('An error occured parsing the XML.  Validate that it is a valid Panorama XML configuration')
    print(e)
    sys.exit(1)


## Get the rules from the configuration
config = root.findall(f"devices/entry/device-group/*[@name='{DEVICE_GROUP}']/{RULE_BASE}/decryption/rules/")

## Perform additional checks on the inputs
## Check for rules in the rulebase
if len(config) < 1:
    print(f'No rules found in the decryption {RULE_BASE} for device-group: {DEVICE_GROUP}.\nExiting...')
    sys.exit(1)

## Loop through the rules of the configuration and get the name of each rule.
decryption_rule_names = [item.attrib['name'] for item in config]

## Append a set command to add profile per rule.
set_commands = [f'set device-group {DEVICE_GROUP} pre-rulebase decryption rules "{name}" profile {DECRYPTION_PROFILE}' for name in decryption_rule_names]

## Write set commands to file
with open(OUTPUT, 'w+') as f:
    for line in set_commands:
        f.write(line + '\n')