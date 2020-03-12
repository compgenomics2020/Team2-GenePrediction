"""
Mark union_fna and union_faa files with KNOWN (K) or UNKNOWN (U) according to hits in
its corresponding blast file.

    created by: Danielle Temples
    last edited: March 11, 2020 @ 7:45PM

"""

#!/usr/bin/python
import os, subprocess

def rename(union_input_path, blast_input_path, input_file, type):
    #blast_input_path = the folder that the formatted blast files are in (ex: blast/formatted_)
    #union_input_path = the folder that the union files are in (ex: union_faa, union_fna)
    #input_file = the specific file number in the folders (ex: CGT2049, CGT2211)
    #type = faa or fna
    #blast_input_file = the specific blast file that correlates to the input file (ex: CGT2049_union.fna_blast)
    blast_input_file = blast_input_path+"/"+input_file+"_union.fna_blast"
    #union_input_file = the specific union file that correlates to the input file (ex: CGT2049_union.fna/faa)
    union_input_file = union_input_path+"/"+input_file+"_union."+type
    #output_folder= the folder that the known/unknown files will be placed in (folder in input_path named kn_union_fna/faa)
    output_folder = union_input_path+"ku_union2_"+type+"/"
    #output_file = the ku file in the ku folder under the union folders (ex: ku_union_faa/CGT2049_union.faa)
    #output_file = output_folder+"/"+input_file+"_union."+type

    if input_file+"_union."+type not in os.listdir(union_input_path):       #if CGT2049_union.fna/faa does not exist in union_fna/faa
        print("Union Directory does not contain inputted union file {}. Please check before running tool for same file").format(input_file+"_union."+type)
        return False
    if input_file+"_union.fna_blast" not in os.listdir(blast_input_path):       #if CGT2049_union.fna_blast does not exist in blast directory
        print("Blast Directory does not contain corresponding file to union file {}. Please check before running tool for same file").format(input_file+"_union."+type)
        return False

    if "ku_union2_"+type in os.listdir(union_input_path):    #if ku_union_faa/fna already exists in union_faa/fna folder
        if input_file+"_union."+type in os.listdir(output_folder):  #if CGT2049_union.faa/fna already exists in ku_union_faa/fna folder
            print("Output Directory {} contains file. Please delete it before running the tool for the same file").format(output_folder)
            return False
    else:
        os.mkdir(output_folder)     #make ku_union_fna/faa folder if it does not exist
        output_file = output_folder+"/"+input_file+"_union."+type   #make file in ku_union_fna/faa folder called CGT2049_union.faa/fna
        subprocess.call(["cp", union_input_file, output_file])  #copy contents from input file to output file (union_faa/CGT2049_union.faa -> union_faa/ku_union_faa/CGT_union_faa)


    original = open(output_file, 'r').readlines()
    hits = open(blast_input_file, 'r').readlines()
    data = []
    for line in hits:
            data.append(line.split('\t')[0])
    write_output=open(output_file,"w")
    for l in original:
            if l.startswith(">"):
                    #print("header")
                    match = l.split(">")[1]
                    match=match.strip("\n")
                    #print(match)
                    if match in data:
                            l=l.strip("\n")
                            write_output.write(l + " K".format(1)+"\n")
                            #print("known")
                    else:
                            l=l.strip("\n")
                            write_output.write(l + " U".format(1)+"\n")
                            #print("unknown")a
            else:
                    write_output.write(l)
    write_output.close()

if __name__=="__main__":
    pass

