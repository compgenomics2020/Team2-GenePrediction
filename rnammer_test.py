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
print(ff)
root=os.path.abspath(os.path.join(os.getcwd(), ".."))
print(root)

def mkdir(result_folder):

    create= root+str("/")+result_folder
    f = os.path.exists(create)
    if not f:
        os.makedirs(create)

mkdir("rnammer_results")

def run_rnammer(input_file,output_file):


    os.system(root+"/./rnammer -S bac -m lsu,ssu,tsu -multi -gff rRNA.gff "+input_file)
    os.system(root+"/./convert_RNAmmer_to_gff3.pl --input rRNA.gff > "+root+"/rnammer_results/"+output_file+".gff3")

for input_contigs in ff:
    out=input_contigs.split(".")[0]
#   print(out)
    run_rnammer(input_contigs,str(out))
    
#run_rnammer(ff[0],"gg")

if __name__ == "__main__":
    main()

