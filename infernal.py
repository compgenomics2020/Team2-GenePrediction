#!/usr/bin/env python3

def main():
    '''
    Insert argparse code that populates the following variables
     - reads directory
     
    '''
    # Argparse code

import argparse
import os 

parser=argparse.ArgumentParser()

parser.add_argument("-input","--file_directory",help="this is the input file directory")

args=parser.parse_args()

local = args.file_directory
os.chdir(local)
ff=os.listdir(os.getcwd())
#print(ff)
root=os.path.abspath(os.path.join(os.getcwd(), ".."))
#print(root)

def mkdir(result_folder):
    
    create= root+str("/")+result_folder
    f = os.path.exists(create)
    if not f:                 
        os.makedirs(create)

mkdir("infernal_results")

def run_infernal(input_file,output_file):

    os.system("cmscan -E 1e-06 --rfam --tblout result.tblout --noali --fmt 2 --clanin "+root+"/Rfam12.2.claninfo "+root+"/Rfam.cm "+input_file)
    
    os.system(root+"/./infernal2gff.pl --cmscan --fmt2 result.tblout --all > "+root+"/infernal_results/"+output_file+".gff3")


for input_contigs in ff:
    out=input_contigs.split(".")[0]
#    print(out)
    run_infernal(input_contigs,str(out))
#run_infernal(ff[0],"gg")


if __name__ == "__main__":
    main()

