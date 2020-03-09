# !/usr/bin/env/ python3
import argparse
import os
import subprocess
from genemarks2_wrapper import genemarks2_script
from prodigal_wrapper import prodigal_script
import threading
############################### https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text/22157136#22157136 ########################################
# Helps to format the argparse options
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
#############################################################################################################################################################################################
#check whether input files are present or not

# Running GeneMarkS-2 and/or Prodigal based on the options given by the user, it takes in the input path to the files, output path, type of the species( either bacteria or auto for genemarks-2) and which tool to run or both to run
def running_tools(input_path,output_path,type_species,run_tool):
	#List all the directories present in the input path, where the wrapper goes into those directories and runs the contigs files
    for file in os.listdir(input_path):
        if (run_tool==1 or run_tool==3):
            genemarks2_output=genemarks2_script(input_path,file,output_path,type_species)
            if not genemarks2_output:
                print("GeneMarkS-2 failed to run for {}".format(file))
        if(run_tool==2 or run_tool==3):
            prodigal_output=prodigal_script(input_path,file,output_path)
            if not prodigal_output:
                print("Prodigal failed to run for {}".format(file))
############################################################################################################################################################################################
######## main of the script which takes in the input ###################################### 
def main():
    parser = argparse.ArgumentParser(description="Backbone script",formatter_class=SmartFormatter)
    parser.add_argument("-iaf1", "--assembly-files1", help="Path to a directory that contains input directory that contains contigs files 1.", required=True)
    parser.add_argument("-iaf2", "--assembly-files2", help="Path to a directory that contains input directory that contains contigs files 2.", required=True)
    parser.add_argument("-go", "--gene-output", help="Path to a directory that will store the output gff files, fna files and faa files.", required=True)
    parser.add_argument("-tr","--tools-to-run",default=3,help="R|Default Option is 3, options available\n"
    "1 Only GeneMarkS-2 \n"
    "2 Only Prodigal \n"
    "3 Both and getting a union of the genes")
    parser.add_argument("-ts", "--type-species", help="if running Gene_MarkS-2, mention species to be either bacteria or auto")
    args = vars(parser.parse_args())
# there are two input paths as there are two folders given to us by the genome assembly group according to the kmer count
    input_path1=args['assembly_files1']
    input_path2=args['assembly_files2']
    output_path=args['gene_output']
    run_tool=args['tools_to_run']
    type_species=args['type_species']
    running_tools(input_path1,output_path,type_species,run_tool)
    running_tools(input_path2,output_path,type_species,run_tool)    

if __name__== "__main__":
    main()
