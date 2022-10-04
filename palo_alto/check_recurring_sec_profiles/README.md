# Find Reccuring Security Profiles Not Grouped
Parse through a security profile rulebase and find rules that are not using security group profiles.  If that same configuration is seen in another rule then create a group and apply those rules to that group based on the defined THRESHOLD.  The default threshold is 10 recurrances.

## Requirements
XlsxWriter==3.0.3

## Getting Started
Run this script from the command line.  three arguments are required, optionally change the output filename.  A file will be generated where the script is run that contains the set commands.

--config
    Required (str): the relative or full path to the Panorama XML configuration

--threshold
    Optional (str): Number of recurring configurations found in all security rules to include in output.

--devicegroup
    Required (str): the device-group containing the rule-set you want to modify.

--rule-set
    Required (str): pre-rulebase | post-rulebase

### Example execution from command line:
```
python3 main.py \
--config "/Users/username/Desktop/config.xml" \
--threshold 5 \
--rulebase "post-rulebase" \
--devicegroup "MyDG"
```

## Todos
 - Additional error checking
 - Add testing
 - Consider adding an option to create security profiles from iron_skillet
 - Add option to check both post and pre rule-base's simultaniously.

## Changelog
9.28.22     
    Initial Commit