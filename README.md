# InvivoConvert
Converts invivo dental viewer (.inv) files to a sequence of 16-bit TIFF images. 
## Usage

 1. Install Kakadu.
 Yeah, its proprietary, and I probably could've used PIL or any of the other python libs, but it was too finnicky trying to get the j2k components to stay seperate. Kakadu works, it's fast, it's free-ish, and I'm tired. You also need python and git, but I'm just gonna assume you have those. 
 2. (Optional) Make sure Kakadu's installed and working fine:
 ```
 kdu_jp2info -version
 ```
 > this should print the version you have installed. If you get something like "command not found" you either don't have it installed, or it's not in PATH. Fix that.
 3. Git this amazing repository
 ```
 git clone https://github.com/metaprotium/InvivoConvert.git && cd InvivoConvert
 ```
 4. Convert
 ```
 python convert.py {location of your .inv file}
 ```
 5. Done!
 The TIFF images are in the same folder as the python script.

If you ran into any issues with this script, feel free to try and fix them yourself. I don't plan to maintain this repo. I just made it to solve a problem I faced where the Bostwickenator/InvivoExtractor repo wasn't extracting all the images from my file, possibly due to an update in the file format. It says it's a version 2 INV file in the metadata. The code is loosely based on that repo, I just had ChatGPT refactor the original to python and used that as a starting point. 
