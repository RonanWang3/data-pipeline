""" 
EDIT 2/13/2024:
1. update data source: 2022 Zip code to ZCTA crosswalk (https://udsmapper.org/zip-code-to-zcta-crosswalk/)
2. change reading input data source file from csv to xlsx

instruction:
before running the script:
a zip folder has to be created, use path to the zip folder at sys.arg[1] for the command.

then run:
python zipgraph.py ZIPCodetoZCTACrosswalk2022UDS.xlsx ../../zip/

<path of zcta file. ex: timelines/prep/all/ZIPCodetoZCTACrosswalk2022UDS.xlsx> 
<path to zip folder. ex: timelines/zip>

the order CANNOT be switched, or else the script will fail.
"""
import warnings
warnings.simplefilter(action='ignore')
import os
import pandas as pd
import sys
import subprocess

def getZipCodeList(fileDir):
    df = pd.read_excel(fileDir)
    zipcode_list=[z for z in df['ZIP_CODE']]
    return zipcode_list

def zipCode_to_String(zipcode_list): #convert zip int format to string format
    zipcode_string_list=[]
    for z in zipcode_list:
        if len(str(z))==3:
            z="00"+str(z)
            zipcode_string_list.append(z)
        elif len(str(z))==4:
            z="0"+str(z)
            zipcode_string_list.append(z)
        else:
            z=str(z)
            zipcode_string_list.append(z)
    return zipcode_string_list

def createPath_old(mainPath,zip_list):
    zip_dict={} #key is zipcode Int), value is the path of where the output file is saved
    zip_string_list=zipCode_to_String(zip_list)
    for i in range(len(zip_list)):
        zip_string=zip_string_list[i]
        subPath=""
        for c in zip_string: #loop through each character
            subPath=os.path.join(subPath,c)
        fullPath=os.path.join(mainPath,subPath)
        zip_dict[zip_list[i]]=fullPath
    return zip_dict

def createPath(mainPath,zip_list):
    zip_dict={} #key is zipcode Int), value is the path of where the output file is saved
    zip_string_list=zipCode_to_String(zip_list)
    for zip_string in zip_string_list:
        subPath=""
        for c in zip_string: #loop through each character
            subPath=os.path.join(subPath,c)
        fullPath=os.path.join(mainPath,subPath)
        zip_dict[int(zip_string)]=fullPath
    return zip_dict

def createMDfile(mainPath,fileDir,zip_list):
    zip_dict=createPath(mainPath,zip_list)
    df=pd.read_excel(fileDir)
    for row in df.itertuples():
        zip_code=row.ZIP_CODE
        zipcode_=""
        if len(str(zip_code))==3:
            zipcode_="00{}".format(str(zip_code))
        if len(str(zip_code))==4:
            zipcode_="0{}".format(str(zip_code))
        if len(str(zip_code))==5:
            zipcode_=str(zip_code)
        outputDir=zip_dict[zip_code]
        if os.path.exists(outputDir):
            subprocess.call(["rm","-dr",outputDir])
        command="mkdir -p {}".format(outputDir)
        subprocess.call(command, shell=True)
        outFile=os.path.join(outputDir,"zipinfo.md")
        with open(outFile,"w") as fh:
            fh.write("# {}, {}, {} \n".format(row.PO_NAME,row.STATE,zipcode_))
            fh.write("ZCTA {} \n".format(row.zcta))
            fh.write("<!-- {} -->".format(row.ZIP_TYPE))

def main():
    fileDir=os.path.abspath(sys.argv[1])
    mainPath=os.path.abspath(sys.argv[2])
    zipcode_list=getZipCodeList(fileDir)
    createMDfile(mainPath,fileDir,zipcode_list)
if __name__ == "__main__":
    main()