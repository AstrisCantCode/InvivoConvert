import sys
import os
import xml.etree.ElementTree as ET

JPEG_2000_HEADER = bytes.fromhex("FF4FFF51")

class BadMetadataOptionException(Exception):
    "Bad Metadata selection."
    pass

def main():
    global fileindex
    fileindex = 0
    if len(sys.argv) <= 1:
        print("Usage:", sys.argv[0], "filename.inv")
        sys.exit(-1)

    param = sys.argv[1]
    head, tail = os.path.split(param) #split input file location into directory and file name
    head += "/"
    tail = tail.split(".", 1)[0]
    tail += "/"
    param2 = head + tail #define param2 as the same directory as input, and same filename but with no extensions

    try: TextMode = sys.argv[2]
    except IndexError: TextMode = 'None' #if no text mode is specified, it defaults to partial.

    print("Extracting:", param)
    print("To:", param2)

    with open(param, "rb") as file:
        whole_file = file.read()

    try:
        print_metadata(whole_file, TextMode)
    except BadMetadataOptionException:
        print("Bad metadata verbosity setting, must be either Full, Partial, or None")
        exit()
    except: 
        print('encountered issues printing metadata, proceeding')

    os.mkdir(param2)

    index = 0
    start = whole_file.find(JPEG_2000_HEADER)
    while start != -1:
        end = whole_file.find(JPEG_2000_HEADER, start + len(JPEG_2000_HEADER))
        write_file(index, start, end, whole_file, param2)
        index += 1
        start = end
    print(f'Wrote {fileindex + 1} TIFF images')


def write_file(index, start, end, whole_file, location):
    global fileindex
    with open(f"{location}image{index}.j2k", "wb") as ws:
        ws.write(whole_file[start:end])   
    imageinfostream = os.popen(f"kdu_jp2info -i {location}image{index}.j2k") #use kdu_jp2info command to check # of components (sub-images). invivo stacks several mono into 1 jpeg2000. I found 11 is typical, but last file may have less. 
    imgxml = ET.fromstring(imageinfostream.read()) #kdu_jp2info returns data in xml
    imglnum = int(imgxml.find('components').text) #from what I can tell, width, height, components, and tiles (normally 1) are given. we only need components info.
    output_names = ""
    for i in range(imglnum):
        output_names += f"{location}image{str(fileindex).zfill(4)}.tiff,"
        fileindex += 1
    #print(f'decompressing chunk {index} into {imglnum} TIFFs')
    convertstreamholder = os.popen(f"kdu_expand -i {location}image{index}.j2k -o {output_names}").read() #run .read() and set output to convertstreamholder so that the convert command is blocking, and we don't delete intermediate while converstion is still happening. necessary? idk.
    os.remove(f"{location}image{index}.j2k") #delete j2k file extracted from .inv, we don't it anymore.

def print_metadata(whole_file, mode):
    if mode == "Partial" or mode == "Full":
        start_search = bytes("<AppendedData encoding='raw'>", 'utf-8')
        end_search = bytes("</AppendedData>", 'utf-8')
        ds_index = whole_file.find(start_search) + len(start_search)
        de_index = whole_file.rfind(end_search)
        smol_doc = whole_file[:ds_index] + whole_file[de_index:]
        docxml = ET.fromstring(smol_doc)
        if mode == "Partial":
            print("Pixels: " + docxml.find("Volume").get('Dimensions'))
            print("Spacing: " + docxml.find("Volume").get('Spacing'))
            print("Name (unformatted): " + docxml.find("CaseInfo").find("Patient").find("PatientName").attrib['Value'])
            print("DOB (year,month,day?): " + docxml.find("CaseInfo").find("Patient").find("PatientBirthDay").attrib['Value'])
            print("Patient ID (unk format): " + docxml.find("CaseInfo").find("Patient").find("PatientID").attrib['Value'])
            print("Modality: " + docxml.find("CaseInfo").find("IdentifyInfo").find("Modality").attrib['Value'])
            print("Machine Manufacturer: " + docxml.find("CaseInfo").find("IdentifyInfo").find("Manufacture").attrib['Value'])
            print("Machine Model: " + docxml.find("CaseInfo").find("IdentifyInfo").find("MaufacturModelName").attrib['Value'])
            print("Machine KV (?): " + docxml.find("CaseInfo").find("AcquisitionInfo").find("KV").attrib['Value'])
            print("Image Date (year,month,day?): " + docxml.find("CaseInfo").find("IdentifyInfo").find("ImageDate").attrib['Value'])
        elif mode == "Full":
            print(" ")
            for lvl1 in docxml:
                print(lvl1.tag, lvl1.attrib)
                for lvl2 in lvl1:
                    print('\t', lvl2.tag, lvl2.attrib)
                    for lvl3 in lvl2:
                        print('\t\t', lvl3.tag, lvl3.attrib)
            print(" ")
    elif mode == "None":
        print("")
    else:
        raise BadMetadataOptionException

if __name__ == "__main__":
    main()
