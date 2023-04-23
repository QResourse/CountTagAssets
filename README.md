# Qualys count assets based on tag

This python code is used to deactivate (move agent to CSAM mode - inventory only)
This will allow qualys to track the host and update the agent while not consuming a VM license. 
## Requirments

1. python 3.8+
2. [pip package manager](https://pip.pypa.io/en/stable/installation/)


### Edit config
Rename the file config.xml.sample to config.xml
Change the **BASE_URL** to the correct platfrom. See [platform-identification](https://www.qualys.com/platform-identification/)
Change the **USERNAME** and **PASSWORD** information
Change the **TAG**  information to reflect the tags you which to use for grouping the agents



## Release Notes
1.0.0 - Innitial release;
#### For more information please see
<https://www.qualys.com/docs/qualys-ca-api-user-guide.pdf>
