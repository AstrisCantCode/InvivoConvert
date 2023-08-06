#gotta have kakadu installed for this script to work. 
import sys
import os
import xml.etree.ElementTree as ET

JPEG_2000_HEADER = bytes.fromhex("FF4FFF51")

def main():
    global fileindex
    fileindex = 0
    if len(sys.argv) <= 1:
        print("Usage:", sys.argv[0], "filename.inv")
        sys.exit(-1)

    param = sys.argv[1]
    print("Extracting:", param)

    with open(param, "rb") as file:
        whole_file = file.read()

    index = 0
    start = whole_file.find(JPEG_2000_HEADER)
    while start != -1:
        end = whole_file.find(JPEG_2000_HEADER, start + len(JPEG_2000_HEADER))
        write_file(index, start, end, whole_file)
        index += 1
        start = end

def write_file(index, start, end, whole_file):
    global fileindex
    with open(f"image{index}.j2k", "wb") as ws:
        ws.write(whole_file[start:end])   
    imageinfostream = os.popen(f"kdu_jp2info -i image{index}.j2k") #use kdu_jp2info command to check # of components (sub-images). invivo stacks several mono into 1 jpeg2000. I found 11 is typical, but last file may have less. 
    imgxml = ET.fromstring(imageinfostream.read()) #kdu_jp2info returns data in xml
    imglnum = int(imgxml.find('components').text) #from what I can tell, width, height, components, and tiles (normally 1) are given. we only need components info.
    output_names = ""
    for i in range(imglnum):
        output_names += f"image{str(fileindex).zfill(4)}.tiff,"
        fileindex += 1
    print(output_names)
    convertstreamholder = os.popen(f"kdu_expand -i image{index}.j2k -o {output_names}").read() #run .read() and set output to convertstreamholder so that the convert command is blocking, and we don't delete intermediate while converstion is still happening. necessary? idk.
    os.remove(f"image{index}.j2k") #delete j2k file extracted from .inv, we don't it anymore.

if __name__ == "__main__":
    main()
