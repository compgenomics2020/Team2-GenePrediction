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
print(root)

def mkdir(result_folder):

    create= root+str("/")+result_folder
    f = os.path.exists(create)
    if not f:
        os.makedirs(create)

mkdir("aragorn_results")

def run_aragorn(input_file,output_file):


    os.system("aragorn -l -t -gc1 -w  "+input_file+ " -o output.fasta")
    os.system(root+"/./cnv_aragorn2gff.pl -i output.fasta> "+root+"/aragorn_results/"+output_file+".gff3 -gff-ver=3")

for input_contigs in ff:
    out=input_contigs.split(".")[0]
#   print(out)
    run_aragorn(input_contigs,str(out))
    
#run_aragorn(ff[0],"gg")

if __name__ == "__main__":
    main()

