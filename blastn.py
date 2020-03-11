"""
Run BLASTn for each union_fna file against
custom BLAST database.

    created by: Danielle Temples
    last edited: March 11, 2020 @ 7:45PM

"""

#!/usr/bin/python
import os, subprocess

def blastn(union_input_path, blastdb_input_path, input_file, db_name, output_path):
    #blastdb_input_path = the folder that the blast database is in
    #union_input_path = the folder that the union_fna files are in (ex: union_gff)
    #input_file = the specific file number in the folders (ex: CGT2049, CGT2211)
    #output_path = path where the blast output folder will be
    #db_name = name of the BLAST custom database
    #blast_db = the location of the blast custom database
    blast_db = blastdb_input_path+"/"+db_name+".fna"
    #union_input_file = the specific union file that correlates to the input file (ex: CGT2049_union.fna/faa)
    union_input_file = union_input_path+"/"+input_file+"_union.fna"
    #output_folder= the folder that the known/unknown files will be placed in (folder in input_path named kn_union_fna/faa)
    output_folder = output_path+"blast/"
    output_file = output_folder+input_file+"_union.fna_blast"

    if input_file+"_union.fna" not in os.listdir(union_input_path):       #if CGT2049_union.fna does not exist in union_fna
        print("Union Directory does not contain inputted union file {}. Please check before running tool for same file").format(input_file+"_union.fna")
        return False
    if db_name not in os.listdir(blastdb_input_path):       #if no database exists in blast database directory
        print("BLAST database {} does not exists in specified directory. Please make a BLAST database before running script").format(db_name)
        return False

    if "blast" in os.listdir(output_path):    #if blast folder already exists in output path
        if output_file in os.listdir(output_folder):  #if CGT2049_union.fna_blast already exists in blast output folder
            print("Output Directory {} contains file. Please delete it before running BLASTn for the same file").format(output_folder)
            return False

    else:
        os.mkdir(output_folder)     #make blast output folder if it does not exist
        subprocess.call(["blastn", "-db", blast_db, "-query", union_input_file, "-out", output_file, "-max_hsps", "1", "-max_target_seqs", "1", "-outfmt", "6", "-perc_identity", "100", "-num_threads", "5"])

if __name__=="__main__":
    pass

