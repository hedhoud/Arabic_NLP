#!/bin/bash

input=$1
output=$2

cat $input | sort | uniq | shuf > $output/shufl_all.txt 

mkdir -p $output/all $output/train $output/val $output/test
cp $input $output/all/all.text

split -l $[ $(wc -l $output/shufl_all.txt | xargs| cut -d" " -f1) * 70/100 ] $output/shufl_all.txt $output/segment
mv $output/segmentaa $output/train/train.txt
split -l $[ $(wc -l $output/segmentab | xargs| cut -d" " -f1) * 70/100 ] $output/segmentab $output/seg

mv $output/segaa $output/test/test.txt
mv $output/segab $output/val/val.txt

rm $output/seg*
rm $output/shufl_all.txt