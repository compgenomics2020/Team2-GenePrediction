"""
Merge GM-S2 and Prodigal gene prediction gff (union) and create subsequent 
union .fna and .faa files
    
    created by: Kara Keun Lee
    last edited: 01/03/2020
    
"""
#!/usr/bin/python3
import os
import subprocess as sp

def merge_predict(input_gms2_path,input_prod_path,input_contig_path1,input_contig_path2=None):

    # check the paths to directories provided contain prediction files and contig files:
    if not os.listdir(input_gms2_path) :
        print("There are no Genemark-S2 gff files in the given directory path. Please check and try again.")
        return False
    if not os.listdir(input_prod_path) :
        print("There are no Prodigal gff files in the given directory path. Please check and try again.")
        return False
    if not os.listdir(input_contig_path1) :
        print("There are no assembled contig fasta files in the given directory path. Please check and try again.")
        return False
    if input_contig_path2!= None:
        if not os.listdir(input_contig_path2) :
            print("There are no assembled contig fasta files in the given directory path. Please check and try again.")
            return False
    # create list of isolate sample numbers:
    sp.call(["ls",input_gms2_path,">","contigs_list.txt"])

    # check if output directories exist:
        # Yes --> empty the output directories for the new run
        # No --> make 3 new union output directories 

    # union gff    
    if os.path.exists("./union_gff") == False:
        sp.call(["mkdir","union_gff"])
    else:
        if os.listdir("./union_gff"):
            print("Output gff folder exists please delete the files before continuing")
            return False
    # union fna         
    if os.path.exists("./union_fna") == False:
        sp.call(["mkdir","union_fna"])
    else:
        if os.listdir("./union_fna"):
            print("Output fna folder exists please delete the files before continuing")
            return False
    # union faa 
    if os.path.exists("./union_faa") == False:
        sp.call(["mkdir","union_faa"])
    else:
        if os.listdir("./union_faa"):
            print("Output faa folder exists please delete the files before continuing")
            return False
    
    if os.path.exists("./temp") == False:
        sp.call(["mkdir","temp"])
    else:
        sp.call(["rm", "-rf", "./temp"])
        sp.call(["mkdir","temp"])

    # process prediction files from each sample to get union outputs:
    with open("contigs_list.txt",'r') as fn:
        for sample in fn:

            # specify paths & formats:
            gms2_gff=input_gms2_path+"/"+sample+"_output.gff"
            prod_gff=input_prod_path+"/"+sample+"_output.gff"
            if sample in os.listdir(input_contig_path1):
                contig_file=input_contig_path1+"/"+sample+"/contig.fasta"
            elif input_contig_path2!=None:
                if sample in os.listdir(input_contig_path2):
                    contig_file=input_contig_path2+"/"+sample+"/contig.fasta"
            else:
                print("{} not present in either or the directories mentioned".format(sample))
                continue
            intersect1_gff="temp/"+sample+"_1.txt"
            intersect2_gff="temp/"+sample+"_2.txt"
            intersect3_gff="temp/"+sample+"_3.txt"
            union_gff="union_gff/"+sample+"_union.gff"
            union_fna="union_fna/"+sample+"_union.fna"
            union_faa="union_faa/"+sample+"_union.faa"

            # generate 3 parts of the union using bedtools intersect:
            sp.call(["bedtools","intersect","-a",gms2_gff,"-b",prod_gff,"-wa","-v","-f","1.0","-r",">",intersect1_gff])
            sp.call(["bedtools","intersect","-b",gms2_gff,"-a",prod_gff,"-wa","-v","-f","1.0","-r",">",intersect2_gff])
            sp.call(["bedtools","intersect","-a",gms2_gff,"-b",prod_gff,"-f","1.0","-r",">",intersect3_gff])
            # combine all resulting intersections for union gff:
            sp.call(["cat",intersect1_gff,intersect2_gff,intersect3_gff,">",union_gff])

            # remove temporary directory with intersect files:
            sp.call(["rm","-r","temp"])

            # generate union fna files for blasting using union gff:
            sp.call(["samtools","faidx",contig_file])
            sp.call(["bedtools","getfasta","-fi",contig_file,"-bed",union_gff,"-fo",union_fna])

            # generate union faa files, maintain header format:
            sp.call(["transeq",union_fna,"-sformat", "pearson","-trim","-clean","-outseq",union_faa])
            sp.call(["sed","-i","'s/_[^_]*$//'",union_faa])
    return True

if __name__=="__main__":
    pass
