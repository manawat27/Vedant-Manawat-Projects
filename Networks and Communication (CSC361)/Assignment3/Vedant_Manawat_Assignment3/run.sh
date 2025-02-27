#!/bin/sh
FILE_NAME=Assignment3.py
DIRECTORY=./
echo "--------------------------------------------------------------------------------"
echo "Group 1 trace 1 (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group1-trace1.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 1 trace 2 (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group1-trace2.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 1 trace 3 (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group1-trace3.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 1 trace 4 (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group1-trace4.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 1 trace 5 (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group1-trace5.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 2 trace 1 (Windows)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group2-trace1.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 2 trace 2 (Windows)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group2-trace2.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 2 trace 3 (Windows)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group2-trace3.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 2 trace 4 (Windows)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group2-trace4.pcap
echo "--------------------------------------------------------------------------------"
echo "Group 2 trace 5 (Windows)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/group2-trace5.pcap
echo "--------------------------------------------------------------------------------"
echo "Fragmented trace (Linux)"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/traceroute-frag.pcap
echo "--------------------------------------------------------------------------------"
echo "Long windows tracefile 1"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/win_trace1.pcap
echo "--------------------------------------------------------------------------------"
echo "Long windows tracefile 2"
echo "--------------------------------------------------------------------------------"
python3 $FILE_NAME $DIRECTORY/win_trace2.pcap