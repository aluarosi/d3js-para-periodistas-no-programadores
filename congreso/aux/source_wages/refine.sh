#!/usr/bin/env bash

# Feed the raw .cvs file into stdin
#   $ cat raw/Congreso\ -\ Congreso\ \(segundo\ chequeo\ nosotros\).csv | ./refine.sh > congreso_refine.sh

# (1) Select only lines that start with double quotes
# (2) Remove Parlamentary Group from MP Name
# (3) Sort in alphabetical order

grep '^"' |\
 sed 's/..([^)]*)//' |\
 sort
