# Scripts
A collection of simple, easy to use, networking scripts.

## Palo Alto
- ### Panorama
    - **Add Decryption Profile**
        - *Loops through all of the security policy rules in a given device group and returns the SET commands required to apply a decryption profile to them.*
    - **Check Reccuring Security Profiles**
        - *Loops through a a device-groups security policy and checks for instances where multiple rules have the same security profiles applied. If the number reaches the specified threshold then a recommendation is made to create a security profile group.  SET commands are generated to apply the security profile group to the rules.*
- ### PANOS