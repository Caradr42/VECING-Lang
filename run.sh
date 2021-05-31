#!/bin/bash
echo running tests...
python run.py tests/factorial.vg -e &> tests/output/factorial_output.txt &
python run.py tests/fibonacci.vg -e &> tests/output/fibonacci_output.txt &
python run.py tests/test11.vg -e &> tests/output/test11_output.txt &
python run.py tests/test10.vg -e &> tests/output/test10_output.txt &
python run.py tests/test9.vg -e &> tests/output/test9_output.txt &
python run.py tests/test8.vg -e &> tests/output/test8_output.txt &
python run.py tests/test7.vg -e &> tests/output/test7_output.txt &
python run.py tests/test6.vg -e &> tests/output/test6_output.txt &
python run.py tests/test5.vg -e &> tests/output/test5_output.txt &
python run.py tests/test4.vg -e &> tests/output/test4_output.txt &
python run.py tests/test3.vg -e &> tests/output/test3_output.txt &
python run.py tests/test2.vg -e &> tests/output/test2_output.txt &
python run.py tests/test1.vg -e &> tests/output/test1_output.txt &
wait
echo finished tests!
