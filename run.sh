#!/bin/bash
python run.py tests/test6.vg -e &> cat > tests/output/test6_output.txt
python run.py tests/test5.vg -e &> cat > tests/output/test5_output.txt
python run.py tests/test4.vg -e &> cat > tests/output/test4_output.txt
python run.py tests/test3.vg -e &> cat > tests/output/test3_output.txt
python run.py tests/test2.vg -e &> cat > tests/output/test2_output.txt
python run.py tests/test1.vg -e &> tests/output/test1_output.txt
