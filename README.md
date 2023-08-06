# InvivoConvert
Converts invivo dental viewer (.inv) files to a sequence of 16-bit TIFF images. 
## Usage
1. Install Kakadu. Yeah, its proprietary, and I probably could've used PIL or any of the other python libs, but it was too finnicky trying to get the j2k components to stay seperate. Kakadu works, it's fast, it's free-ish, and I'm tired. You also need python and git, but I'm just gonna assume you have those. 
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
5. Done! The TIFF images are in the same folder as the python script. 
