# Apply Decryption Profiles To All Decryption Rules
Quickly generate set commands to apply a decryption profile to all decryption rules in a Panorama device-group decryption rule-set.

## Getting Started
Run this script from the command line.  Four arguments are required, optionally change the output filename.  A file will be generated where the script is run that contains the set commands.

--config
    Required (str): the relative or full path to the Panorama XML configuration

--profile
    Required (str): the decryption profile you want to apply to the decryption rules.  Must exist.

--devicegroup
    Required (str): the device-group containing the rule-set you want to modify.

--rule-set
    Required (str): pre-rulebase | post-rulebase

--output
    Optional (str): output filename to modify. defaults to decryption-profile-output.txt

### Example execution from command line:
```
python3 main.py \
--config "/Users/username/Desktop/config.xml" \
--profile "Recommended-Decryption-Profile" \
--rulebase "pre-rulebase" \
--devicegroup "MyDG"
```

## Todos
 - Additional error checking
 - Add testing
 - Consider adding an option to create decryption profile from iron_skillet

## Changelog
9.28.22     
    Add try block to Panorama XML import.
    Updated readme to include getting started and a brief description.