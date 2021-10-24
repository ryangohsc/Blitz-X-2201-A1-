# Blitz-X
ICT2202 Digital Forensics Team Project Assignment 1 - Team Panzerwerfer
- Jonathan Tan Yu Shen
- Koh Jun Jie 
- Ryan Goh Shao Chong 

# Description 
Blitz-eXtractor (Blitz-X) is a modular triage tool written in Python designed to access various forensic artefacts on Windows relating to user data exfiltration. The tool will parse the artefacts and present them in a format viable for analysis. The output may provide valuable insights during an incident response in a Windows environment while waiting for a full disk image to be acquired. The tool is meant to run on live systems on the offending User Account with administrative rights. 

# Key Features 
- Minimised footprint on the target’s system 
  Only “read” operations are performed on specific files specified by Blitz-X’s modules on the target system. 
- User friendly 
  Blitz-X’s command-line interface (CLI) only comprises two optional parameters, “--keydec” and “--keywords” and is easily understandable by a user of a non-technical nature. The “--keydec” parameter would run Blitz-X in “keydec” mode, described in Section VIII of the report. The “--keywords” parameter allows the user to specify a wordlist for Blitz-X to perform a keyword search on the extracted evidence files.
- Highly configurable 
- Provides chain of custody 
- HTML data representation of extracted artefacts data 
