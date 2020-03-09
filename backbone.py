# !/usr/bin/env/python3
import argparse
import os
import subprocess
from genemarks2_wrapper import genemarks2_script
from prodigal_wrapper import prodigal_script
from union_outputs1 import merge_predict
############################### https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text/22157136#22157136 ########################################
# Helps to format the argparse options
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
#############################################################################################################################################################################################
#check whether input files folder is present and not empty or not
def check_input(folder_name):
    if os.path.isdir(folder_name):
        if len(os.listdir(folder_name))!=0:
            return True
        else:
            print("The folder {} is empty".format(folder_name))
            return False
    else:
        print("The folder {} is not present".format(folder_name))
        return False
#Check if the tool which needs to be run is present or not
def check_tools(run_tool):
    tools_to_run=[]
    if(run_tool==1):
        tools_to_run.append("gms2.pl")
    elif(run_tool==2):
        tools_to_run.append("prodigal")
    else:
        tools_to_run.extend(["gms2.pl","prodigal","bedtools","samtools","transeq"])
    for tools in tools_to_run:
        try:
            #Calling the genemarks2 by name.
            bash_output = subprocess.check_output([tools])
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            print("The tool {}, was not present on the system. Please check again".format(tool))
            return False
        return True
# Running GeneMarkS-2 and/or Prodigal based on the options given by the user, it takes in the input path to the files, output path, type of the species( either bacteria or auto for genemarks-2) and which tool to run or both to run
def running_tools(input_path,output_path,type_species,run_tool,flag,name="contigs.fasta"):
        #List all the directories present in the input path, where the wrapper goes into those directories and runs the contigs files
    for file in os.listdir(input_path):
        if (run_tool==1 or run_tool==3):
            genemarks2_output=genemarks2_script(input_path,file,output_path,type_species,name)
        if(run_tool==2 or run_tool==3):
            prodigal_output=prodigal_script(input_path,file,output_path,name)
############################################################################################################################################################################################
######## main of the script which takes in the input ###################################### 
def main():
    parser = argparse.ArgumentParser(description="Backbone script",formatter_class=SmartFormatter)
    parser.add_argument("-io","--input-option",default=1,help="R|Default Option is 1, options available\n"
    "1 Take input from the genome assembly results \n"
    "2 Input your own assembly files")
    parser.add_argument("-nc", "--name-contigs", default="contigs.fasta" ,help="Name of the contig files,called when option 2 for input-option is selected, default considered is contigs.fasta",required=False)
    parser.add_argument("-ia", "--input-assembly", help="Path to the directory that contains input file manually,called when option 2 for input-option is selected",required=False)
    parser.add_argument("-if77", "--input-files77", help="Path to the directory that contains input file for spades output of 21,33,55,77, called when default option for input-option is selected",required=False)
    parser.add_argument("-if99", "--input-files99", help="Path to the directory that contains input file for spades output of 21,33,55,77,99,127,called when default option for input-option is selected",required=False)
    parser.add_argument("-go", "--gene-output", help="Path to a directory that will store the output gff files, fna files and faa files.", required=True)
    parser.add_argument("-tr","--tools-to-run",default=3,help="R|Default Option is 3, options available\n"
    "1 Only GeneMarkS-2 \n"
    "2 Only Prodigal \n"
    "3 Both and getting a union of the genes")
    parser.add_argument("-ts", "--type-species", help="if running Gene_MarkS-2, mention species to be either bacteria or auto")
    args = vars(parser.parse_args())
    output_path=args['gene_output']
    run_tool=args['tools_to_run']
    type_species=args['type_species']
    flag=args['input_option']
    #checks whether genemarks2 and prodigal if either or both are called, are present or not.
    if not check_tools(run_tool):
        return False
    if flag == 2:
        input_path=args['input_assembly']
        name=args['name_contigs']
        if check_input(input_path):
            # checks the input folder for manual input, and then runs the tools. Considers input folder to contain specific sequence folder which in turn contains the name variable (name of the contigs)
            run_out=running_tools(input_path,output_path,type_species,run_tool,flag,name)
            if not run_out:
                return False
            if run_tool==3:
                genemarks2_output=output_path+"/genemarks2/"
                prodigal_output=output_path+"/prodigal/"
                merge=merge_predict(genemarks2_output,prodigal_output,input_path)
                if not merge:
                    return False
        else:
            return False
    else:
        input_folder77=args['input_files77']
        input_folder99=args['input_files99']
        if check_input(input_folder77) and check_input(input_folder99):
            # there are two input paths as there are two folders given to us by the genome assembly group according to the kmer count
            run_out=running_tools(input_folder77,output_path,type_species,run_tool,flag)
            if not run_out:
                return False
            run_out=running_tools(input_folder99,output_path,type_species,run_tool,flag)
            if not run_out:
                return False
            if run_tool==3:
                genemarks2_output=output_path+"/genemarks2/"
                prodigal_output=output_path+"/prodigal/"
                merge=merge_predict(genemarks2_output,prodigal_output,input_folder77,input_folder99)
                if not merge:
                    return False        
        else:
            return False
if __name__=="__main__":
    main()
