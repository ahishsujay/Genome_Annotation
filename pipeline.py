#!/usr/bin/env python3

import os
import subprocess
import argparse

######################################################################## Make directories #############################################################################
def makeDir():

    subprocess.run("mkdir tool_output", shell=True)
    subprocess.run("mkdir temp", shell=True)

    subprocess.run("mkdir tool_output/org_cds_db", shell=True)
    subprocess.run("mkdir tool_output/MergedBLAST", shell=True)

    subprocess.run("mkdir tool_output/prodigal_fasta_result", shell=True)
    subprocess.run("mkdir tool_output/prodigal_gff_result", shell=True)
    subprocess.run("mkdir tool_output/gms2_fasta_result", shell=True)
    subprocess.run("mkdir tool_output/gms2_gff_result", shell=True)

    subprocess.run("mkdir tool_output/prodigal_gms2_intersection", shell=True)
    subprocess.run("mkdir tool_output/prodigal_bedtools", shell=True)
    subprocess.run("mkdir tool_output/gms2_bedtools", shell=True)

    subprocess.run("mkdir tool_output/MergedGFF", shell=True)
    subprocess.run("mkdir tool_output/MergedFASTA", shell=True)

############################################################ Creating database of organism CDS for BLAST ##############################################################
def blastDatabase(org_cds):

    make_database = "makeblastdb -in "+str(org_cds)+" -dbtype nucl -blastdb_version 5 -out tool_output/org_cds_db/blast"
    make_database_subprocess = subprocess.check_output(make_database.split())

######################################################################### Run Prodigal ################################################################################
def runProdigal(input_file):

    run_prodigal = "prodigal -i "+str(input_file)+" -d tool_output/prodigal_fasta_result/prodigal_fasta_"+str(input_file.split("/")[-1])+" -f gff -o tool_output/prodigal_gff_result/prodigal_gff_"+str(input_file.split("/")[-1].replace(".fasta",""))
    run_prodigal_subprocess = subprocess.check_output(run_prodigal.split())

    #prodigal -i data/genome_assembly/CGT3002contigs.fasta -d nucl_test -f gff -o gff_test

####################################################################### Run GeneMarkS-2 ###############################################################################
def runGMS2(input_file):

    run_gms2 = "gms2.pl --seq "+str(input_file)+" --genome-type auto --fnn tool_output/gms2_fasta_result/gms2_fasta_"+str(input_file.split("/")[-1])+" --output tool_output/gms2_gff_result/gms2_gff_"+str(input_file.split("/")[-1].replace(".fasta",""))+" --format gff"
    run_gms2_subprocess = subprocess.check_output(run_gms2.split())

    subprocess.run("mv GMS2.mod temp", shell=True)
    subprocess.run("mv log temp", shell=True)
    subprocess.run("rm -rf temp", shell=True)

    #gms2.pl --seq sample_data/genome_assembly/CGT3002contigs.fasta --genome-type auto --output yes --format gff

    #export PATH=/Users/ahishsujay/ahishbin/gms2_macos:$PATH
    #alias genemarks2="/Users/ahishsujay/ahishbin/gms2_macos/gms2.pl"

################################################################### Run BEDTools intersection #########################################################################
def runBedtoolsIntersect(input_file):

    gms2_file = subprocess.run("ls tool_output/gms2_gff_result/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    #print(gms2_file)
    prodigal_file = subprocess.run("ls tool_output/prodigal_gff_result/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    #print(prodigal_file)

    for i,j in zip(gms2_file,prodigal_file):
        #print(i,"\t",j)
        #run_bedtools_intersect = subprocess.run("bedtools intersect -f 1,0 -r -a tool_output/gms2_gff_result/"+i+" -b tool_output/prodigal_gff_result/"+j+" > tool_output/prodigal_gms2_intersection/"+i+"_"+j,shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip("\n").split()

        subprocess.run("bedtools intersect -f 1,0 -r -a tool_output/gms2_gff_result/"+i+" -b tool_output/prodigal_gff_result/"+j+" > tool_output/prodigal_gms2_intersection/"+i+"_"+j, shell=True)
        #bedtools intersect -f 1,0 -r -a ../tool_output/gms2_gff_result/gms2_gff_CGT3002contigs -b ../tool_output/prodigal_gff_result/prodigal_gff_CGT3002contigs > 3002both
        #run_bedtools_intersect_subprocess = subprocess.run(run_bedtools_intersect, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

        subprocess.run("bedtools intersect -f 1,0 -r -v -a tool_output/gms2_gff_result/"+i+" -b tool_output/prodigal_gff_result/"+j+" > tool_output/gms2_bedtools/"+i+"_"+j, shell=True)
        #run_bedtools_intersect_gms2_subprocess = subprocess.run(run_bedtools_intersect_gms2, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

        subprocess.run("bedtools intersect -f 1,0 -r -v -a tool_output/prodigal_gff_result/"+j+" -b tool_output/gms2_gff_result/"+i+" > tool_output/prodigal_bedtools/"+i+"_"+j, shell=True)
        #run_bedtools_intersect_prodigal_subprocess = subprocess.run(run_bedtools_intersect_prodigal, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

    files1 = subprocess.run("ls tool_output/prodigal_gms2_intersection/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files2 = subprocess.run("ls tool_output/gms2_bedtools/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files3 = subprocess.run("ls tool_output/prodigal_bedtools/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    #print(files1,"\t", files2,"\t", files3)
    for i,j,k in zip(files1,files2,files3):
        subprocess.run("cat tool_output/prodigal_gms2_intersection/"+i+" tool_output/gms2_bedtools/"+j+" tool_output/prodigal_bedtools/"+k+" > tool_output/MergedGFF/final_merged_gff_"+i+j+k, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

######################################################################### Get FASTA files #############################################################################
def runGetFASTA(input_file):

    files4 = subprocess.run("ls tool_output/MergedGFF/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files5 = subprocess.run("ls "+input_file+"/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    #print(files4)
    #print(files5)

    for i,j in zip(files5,files4):
        print(i,"\t",j)
        subprocess.run("bedtools getfasta -fi "+input_file+"/"+i+" -bed tool_output/MergedGFF/"+j+" > tool_output/MergedFASTA/merged_fasta_"+i, shell=True)
        subprocess.run("rm "+input_file+"*.fai", shell=True)

########################################################################## Run BLASTN ##################################################################################
def runBLAST():
    files6 = subprocess.run("ls tool_output/MergedFASTA/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

    for i in files6:
        print(i)
        subprocess.run("blastn -db tool_output/org_cds_db/blast -query tool_output/MergedFASTA/"+i+ " -outfmt 6 -max_hsps 1 -max_target_seqs 1 -num_threads 8 > tool_output/MergedBLAST/"+i+".out", shell = True)



def main():

    #Argparse code:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help = "Input directory containing FASTA files to be analyzed.")
    parser.add_argument("-org_cds", help = "Organism of interest's CDS FASTA file.")
    args = parser.parse_args()

    #Populating variables:
    input_file = args.i
    org_cds = args.org_cds

    #filename1 = "ls "+input_file+"*.fasta"
    filename1 = subprocess.run("ls "+input_file+"*.fasta", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip("\n").split()
    print(filename1)

    make_tool_output_dir = "mkdir tool_output"
    subprocess.call(make_tool_output_dir.split())

    #Calling functions:
    makeDir()
    blastDatabase(org_cds)
    '''
    for files in filename1:
        print(files)
        #runProdigal(files)
        #runGMS2(files)
    '''
    runBedtoolsIntersect(input_file)
    runGetFASTA(input_file)
    runBLAST()

if __name__ == "__main__":
    main()