from xlsxwriter import Workbook
import os, sys, argparse
import xml.etree.ElementTree as ET

'''
## Looks through a security profile based on the supplied configuration, device-group and rulebase to find security rules that are not using a security
## profile group.  If the number of times a specific configuration is seen is greater than or equal to the threshold (defaults to 10) then it will be identified and
## placed into the output.  The script will create two worksheets.  The first worksheet will show a review of the findings and the second worksheet
## will include the set commands to create a grouping and configure the security rules to use that group.

## Sample command to run this script shown below.
## python3 main.py --config "/Users/username/Desktop/config.xml" --threshold 5 --rulebase "pre-rulebase" --devicegroup "MyDG"
'''

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Source Panorama XML Configuration")
parser.add_argument("--threshold", help="The number of times the security profile is seen (>=) to be included")
parser.add_argument("--rulebase", help="pre-rulebase or post-rulebase")
parser.add_argument("--devicegroup", help="device-group to configure")
args = parser.parse_args()

## Validate Arguements
if not args.config:
    print('Panorama XML configuration is required.')
    sys.exit(1)

if not args.rulebase:
    print('pre-rulebase or post-rulebase name is required.')
    sys.exit(1)

if not args.devicegroup:
    print('Device group is required.')
    sys.exit(1)

## Set CONSTANTS from the CLI arguments.
PANORAMA_CONFIGURATION = args.config
THRESHOLD = int(args.threshold) or 10
RULE_BASE = args.rulebase
DEVICE_GROUP = args.devicegroup

filename = f'{os.getcwd()}/output/recurring-sec-profiles.xlsx'
wb = Workbook(filename)
wb.set_size(2500,1600)

severity_color_map = {
    'critical': '#FF0000',
    'high': '#AA3300',
    'medium': '#883300',
    'low': '#0000AA',
    'best-practice': '#00FF00'
}

header_merge_format = wb.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_name': 'IBM Plex Sans',
    'font_size': '28'
})

header_format = wb.add_format({
    'border': 0,
    'align': 'left',
    'valign': 'vcenter',
    'font_name': 'IBM Plex Sans',
    'font_size': '14',
    'font_color': 'white',
    'bg_color': '#002060'
})

standard_format = wb.add_format({
    'border': 0,
    'align': 'left',
    'valign': 'vcenter',
    'font_name': 'IBM Plex Sans',
    'font_size': '12',
    'num_format': '@',
    'bottom': 1,
    'right': 1,
    'text_wrap': 'wrap'
})

count_format = wb.add_format({
    'border': 0,
    'align': 'center',
    'valign': 'vcenter',
    'font_name': 'IBM Plex Sans',
    'font_size': '12',
    'num_format': '@',
    'bottom': 1,
    'right': 1,
    'text_wrap': 'wrap'
})

set_format = wb.add_format({
    'align': 'left',
    'valign': 'vcenter',
    'font_name': 'IBM Plex Sans',
    'font_size': '12',
    'num_format': '@',
    'text_wrap': 'wrap'
})


## Parse XML
try:
    tree = ET.parse(PANORAMA_CONFIGURATION)
    root = tree.getroot()
except FileNotFoundError as e:
    print('File not found.  Panorama configuration not found, check filepath and filename given to the --config argument')
    print(e)
    sys.exit(1)
except ET.ParseError as e:
    print('An error occured parsing the XML.  Validate that it is a valid Panorama XML configuration')
    print(e)
    sys.exit(1)


## Get the rules from the configuration
config = root.findall(f"devices/entry/device-group/*[@name='{DEVICE_GROUP}']/{RULE_BASE}/security/rules/")

## Similiar configurations dictionary
profile_count = {}
for rule in config:
    profiles = rule.findall('./profile-setting/profiles/')

    rule_profile_configuration = ''
    for profile in profiles:
        rule_profile_configuration += profile.find('member').text
        rule_profile_configuration += '\n'
    if rule_profile_configuration not in profile_count:
        profile_count[rule_profile_configuration] = {
            'count': 1,
            'rules': [rule.attrib['name']],
            'config': profiles
        }
    else:
        profile_count[rule_profile_configuration]['count'] += 1
        profile_count[rule_profile_configuration]['rules'].append(rule.attrib['name'])

## Create WORKSHEET
ws_config_review = wb.add_worksheet('Recurring Profiles')
ws_config_review.hide_gridlines(2)
ws_config_review.set_tab_color('#8DC3FC')
ws_config_review.freeze_panes(2,0)
ws_config_review.set_default_row(40)

ws_set_commands = wb.add_worksheet('Set Commands')
ws_config_review.hide_gridlines(2)
ws_config_review.set_tab_color('#8DC3FC')
ws_config_review.freeze_panes(1,0)

## Create Headers
current_row = 1
ws_config_review.set_column('A:A', width=60) 
ws_config_review.set_column('B:B', width=8) 
ws_config_review.set_column('C:C', width=190) 
ws_config_review.merge_range('A1:C1','Recurring Security Profiles Not Grouped', header_merge_format)
ws_config_review.set_row(0, height=60)
ws_config_review.write(current_row,0, 'Config Grouping', header_format)
ws_config_review.write(current_row,1, 'Count', header_format)
ws_config_review.write(current_row,2, 'Rules Associated With Config Grouping', header_format)
ws_config_review.set_row(current_row, 30)

ws_set_commands.set_column('A:A', width=258) 
ws_set_commands.write(0,0,'Set Commands', header_merge_format)
ws_set_commands.set_row(0, height=60)

current_row+=1
## Write Worksheets
for k,v in profile_count.items():
    if v['count'] >= THRESHOLD:
        ws_config_review.write(current_row, 0, str(k).strip(), standard_format)
        ws_config_review.write(current_row, 1, v['count'], count_format)
        ws_config_review.write(current_row, 2, str(v['rules']), standard_format)
        ws_config_review.set_row(current_row, 115)
        current_row += 1

current_row = 1
current_grouping = 1
for k,v in profile_count.items():
    if v['count'] >= THRESHOLD:
        ## Set Commands To Create Profile
        profiles = ' '.join([f'{profile.tag} {profile.find("member").text}' for profile in v['config']])
        ws_set_commands.write(current_row, 0, f'set device-group {DEVICE_GROUP} profile-group sec_prof_{current_grouping} {profiles}', set_format)
        current_row +=1

        ## Set Commmands To Apply Profile To Rules
        for rule in v['rules']:
            ws_set_commands.write(current_row, 0, 
                f'set device-group {DEVICE_GROUP} {RULE_BASE} security rules "{rule}" profile-setting group sec_prof_{current_grouping}', set_format)
            current_row +=1
        current_row +=1
        current_grouping +=1

wb.close()