#!/usr/bin/env python

from argparse import ArgumentParser
import os
import glob
import sys
import yaml


def obtain_repoloc():
    return os.path.dirname(os.path.abspath(__file__))

def get_absolute_path(path):
    return os.path.abspath(path)
LOCATIONREPO = obtain_repoloc()


def check_presence_fastq(SAMPLES):
    # exit statement if no fastq can be found
    if len(SAMPLES) == 0:
        print("\nNo fastq files found in subdirectories\n")
        print("Please give a input directory subdirectories with fastq files \nexiting now.")
        sys.exit()

def define_input(inputdir):
    inputdir = get_absolute_path(inputdir)
    # check if valid
    SAMPLES = glob.glob(f"{inputdir}/*/*fastq*")
    check_presence_fastq(SAMPLES)
    samplesdict = {"SAMPLES":{}}
    for i in SAMPLES:
        samplename = i.split("/")[-2]
        forward = glob.glob(f"{inputdir}/{samplename}/*1*f*q*")[0]
        reverse = glob.glob(f"{inputdir}/{samplename}/*2*f*q*")[0]

        samplesdict["SAMPLES"][str(samplename)] = {
        "forward": get_absolute_path(forward),
        "reverse": get_absolute_path(reverse)}

    samples_loc = yaml.dump(samplesdict, default_flow_style=False)
    os.system(f"mkdir -p {LOCATIONREPO}/samples")
    with open(f"{LOCATIONREPO}/samples/samples.yaml", 'w+') as f:
        f.write(samples_loc)

def launch(cores):
    #change to the location of the repo, this will make sure all envs, databases and other stuff sticks in the repocryptic
    os.chdir(f"{LOCATIONREPO}")
    os.system(f"snakemake  --use-conda --cores {cores} --snakefile Snakefile")

def main(command_line = None):
    #add main parser object
    parser = ArgumentParser(description = "input directory with subdirectories with reads")
    parser.add_argument("-i", required = True, dest = "input_dir")
    parser.add_argument("--cores", required = False, dest = "cores", default = 8, type = int)
    args = parser.parse_args(command_line)
    define_input(args.input_dir)
    launch(args.cores)

if __name__ == "__main__":
    main()

