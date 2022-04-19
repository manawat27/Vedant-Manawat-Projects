## Name: Vedant Manawat
## VNumber: V00904582
## March 1, 2021
## CSC 361 Programming Assignment 2

import struct
import sys
from statistics import mean 

BIG_ENDIAN = ">"
LITTLE_ENDIAN = "<"

connections, complete_connections, reset_connections, all_4_tuples = [],[],[],[]
timestamp_list, SYN_list, FIN_list, RST_list, time = [],[],[],[],[]
packet_counter, window, complete_connections_window = [],[],[]
payload_list, RTT_time = [],[]

# Find information in the Global Header such as:
#   1. magic_number
#   2. Version_major and Version_minor
#   3. thiszone
#   4. sigfigs
#   5. snaplen
#   6. network 
def global_header_information(header):
    
    endianness = LITTLE_ENDIAN
    (magic_num,) = struct.unpack(">I",header[:4])
    if magic_num == 0xa1b2c3d4:
        endianness = LITTLE_ENDIAN
    elif magic_num == 0xd4c3b2a1:
        endianness = BIG_ENDIAN

    (version_maj,) = struct.unpack(endianness + "H",header[4:6])
    (version_min,) = struct.unpack(endianness + "H",header[6:8])
    (thiszone,) = struct.unpack(endianness + "I", header[8:12])
    (sigfigs,) = struct.unpack(endianness + "I", header[12:16])
    (snaplen,) = struct.unpack(endianness + "I", header[16:20])
    (network,) = struct.unpack(endianness + "I", header[20:24])

# Find information in the packet header such as:
#   1. incl_len
def packet_header_information(packet_header):
    (ts_sec,) = struct.unpack("I",packet_header[0:4])
    (ts_usec,) = struct.unpack("I",packet_header[4:8])
    (incl_len,) = struct.unpack("I",packet_header[8:12])

    return ts_sec,ts_usec,incl_len

# Find information in the IPv4 Header such as:
#   1. IPv4 Header Length
#   2. Source and Destination address
#   3. Total Length
#   4. Time to live 
def parse_packet_data_for_IPv4(IPv4_HEADER):
    
    (res,) = struct.unpack('B',IPv4_HEADER[0:1])
    IP_header_len = (res & 15)*4

    src_addr = struct.unpack('BBBB',IPv4_HEADER[12:16])
    dst_addr = struct.unpack('BBBB',IPv4_HEADER[16:20])
    s_ip = str(src_addr[0])+'.'+str(src_addr[1])+'.'+str(src_addr[2])+'.'+str(src_addr[3])
    d_ip = str(dst_addr[0])+'.'+str(dst_addr[1])+'.'+str(dst_addr[2])+'.'+str(dst_addr[3])

    num1 = ((IPv4_HEADER[2]&240)>>4)*16*16*16
    num2 = (IPv4_HEADER[2]&15)*16*16
    num3 = ((IPv4_HEADER[3]&240)>>4)*16
    num4 = (IPv4_HEADER[3]&15)

    total_length = num1+num2+num3+num4

    (time_to_live,) = struct.unpack('B',IPv4_HEADER[8:9])

    return s_ip,d_ip,IP_header_len,total_length

# Function to parse, calculate and return the source and destination port 
def get_port_number(TCP_HEADER):

    num1 = ((TCP_HEADER[0]&240)>>4)*16*16*16
    num2 = (TCP_HEADER[0]&15)*16*16
    num3 = ((TCP_HEADER[1]&240)>>4)*16
    num4 = (TCP_HEADER[1]&15)
    source_port = num1+num2+num3+num4

    num1 = ((TCP_HEADER[2]&240)>>4)*16*16*16
    num2 = (TCP_HEADER[2]&15)*16*16
    num3 = ((TCP_HEADER[3]&240)>>4)*16
    num4 = (TCP_HEADER[3]&15)
    dest_port = num1+num2+num3+num4

    return source_port,dest_port

# Function to find out the status of each connection that has been passed to this fucntion
# Return value will be in the form of SxFx where S is the SYN, F is FIN and the x denotes the number of times the flag was seen
# If the connection is a reset connection thent he return value will be of the form SxFx/R where R denotes that the connection had more than 1 RST flags
def get_status(connections):
    combination = (connections[1],connections[0],connections[3],connections[2])
    SYN = 0
    FIN = 0

    if connections in reset_connections:
        for item in SYN_list:
            if ((item[0] == connections and item[2] == 1) or (item[0] == combination and item[2] == 1)):
                SYN += 1
        
        for item in FIN_list:
            if ((item[0] == connections and item[2] == 1) or (item[0] == combination and item[2] == 1)):
                FIN += 1

        status = "S"+str(SYN)+"F"+str(FIN)+"/R"
        return status
    else:
        for item in SYN_list:
            if ((item[0] == connections and item[2] == 1) or (item[0] == combination and item[2] == 1)):
                SYN += 1
        
        for item in FIN_list:
            if ((item[0] == connections and item[2] == 1) or (item[0] == combination and item[2] == 1)):
                FIN += 1

        status = "S"+str(SYN)+"F"+str(FIN)
        return status

# Function to parse the packets and append all the TCP connections to a list
# After getting all the connections, parse the data again to get the connections that were complete (have at least 1 SYN and 1 FIN)
def check_completeness(syn,connection_4_tuple,combination,fin,rst):
    if (syn == 1 and (connection_4_tuple not in connections and combination not in connections)):
        connections.append(connection_4_tuple)

    for item in connections:
        if (fin == 1 and (connection_4_tuple not in complete_connections and combination not in complete_connections)):
            if (connection_4_tuple == item or combination == item):
                complete_connections.append(item)

    for item in connections:
        if (rst == 1 and (connection_4_tuple not in reset_connections and combination not in reset_connections)):
            if (connection_4_tuple == item or combination == item):
                reset_connections.append(item)    

# Function to count the number of packets sent/recieved for each complete connection that has been passed to the function 
# Returns the number of packets from source to destination and vice versa 
def count_packets(connections):
    temp = all_4_tuples
    combination = (connections[1],connections[0],connections[3],connections[2])
    src_to_dst_counter = 0
    dst_to_src_counter = 0

    for item in temp:
        if item == connections:
            src_to_dst_counter = temp.count(item)
        elif item == combination:
            dst_to_src_counter = temp.count(item)
    
    packet_counter.append(src_to_dst_counter+dst_to_src_counter)

    return src_to_dst_counter,dst_to_src_counter

# Function to count the number of data bytes sent/received for each complete connection that has been passed to the function
# Returns the number of bytes from source to destination and vice versa
def get_data_bytes(connections):
    src = 0
    dst = 0
    combination = (connections[1],connections[0],connections[3],connections[2])

    for item in payload_list:
        if item[0] == connections:
            src += item[1]
        elif item[0] == combination:
            dst += item[1]
    
    return src,dst

# Function to calculat the timestamp of each complete connection that is passed to the function
# Returns the timestamp back to the caller to use for other aspects 
def timestamp_set(ts_sec,ts_usec,orig_time):
    timestamp = round(ts_sec+ts_usec*0.000001-orig_time,6)
    return timestamp

# Find information in the TCP/UDP Header such as:
#   1. Source and destination port number
#   2. Sequence number and acknowledgement number
#   3. Which flags are set
# Makes function calls such as:
#   1. check_completeness: to check if the connection is complete or not
#   2. timestamp_set: to get the timestamp of each packet
def parse_packet_data_for_TCP(TCP_HEADER,src_address,dst_address,ts_sec,ts_usec,incl_len,IP_header_len,total_length):

    orig_time = 0

    source_port,dest_port = get_port_number(TCP_HEADER)
    (seq,) = struct.unpack(">I",TCP_HEADER[4:8])
    (ack_num,) = struct.unpack(">I",TCP_HEADER[8:12])

    (value,) = struct.unpack('B',TCP_HEADER[13:14])
    fin = value & 1
    syn = (value & 2)>>1
    rst = (value & 4)>>2
    ack = (value & 16)>>4 

    buffer = TCP_HEADER[15:16]+TCP_HEADER[14:15]
    (window_size,) = struct.unpack('H',buffer)

    (value,) = struct.unpack('B',TCP_HEADER[12:13])
    TCP_header_len = ((value & 240)>>4)*4
    payload = total_length - IP_header_len - TCP_header_len

    connection_4_tuple = (src_address,dst_address,source_port,dest_port)
    combination = (dst_address,src_address,dest_port,source_port)

    all_4_tuples.append(connection_4_tuple)
    window.append((connection_4_tuple,window_size))

    check_completeness(syn,connection_4_tuple,combination,fin,rst)
    timestamp = timestamp_set(ts_sec,ts_usec,orig_time)

    timestamp_list.append(timestamp)
    SYN_list.append((connection_4_tuple,timestamp,syn))
    FIN_list.append((connection_4_tuple,timestamp,fin))
    payload_list.append((connection_4_tuple,payload,seq,ack_num,syn,fin,timestamp))


# Function which calculates the start and end time of the complete_connection that has been passed to the fucntion
# Returns the start and end time for each connection 
def get_start_and_end_time(connections):
    
    first_occurance = 0
    last_occurance = 0
    combination = (connections[1],connections[0],connections[3],connections[2])

    for item in SYN_list:
        if ((connections == item[0] or combination == item[0]) and item[2] == 1):
            first_occurance = SYN_list.index(item)
            break
    

    for item in FIN_list:
        if ((connections == item[0] or combination == item[0]) and item[2] == 1):
            last_occurance = len(FIN_list) - 1 - FIN_list[::-1].index(item)
            break
    

    start = timestamp_list[first_occurance]
    end = timestamp_list[last_occurance]
    
    if ((end-start) not in time):
        time.append(end-start)

    return start,end

# Function to get the window sizes for each complete connection that has been passed to the function
# The function doesn't return the window size, rather appends the size to a list for future use
def window_size_calculation(connections):
    combination = (connections[1],connections[0],connections[3],connections[2])

    for item in window:
        if ((item[0] == connections or item[0] == combination)):
            complete_connections_window.append(item[1])
    

# Function to get the RTT for each complete connection that has been passed to this function
# This function doesn't return the RTT, rather appends it to a list for future use
def get_RTT(connections):
    combination = (connections[1],connections[0],connections[3],connections[2])

    for i in range((len(payload_list))):
        for j in range(i+1,len(payload_list)):
            if ((payload_list[i][1] == 0) and (payload_list[i][4] == 1 or payload_list[i][5] == 1)):
                if (payload_list[i][0] == connections):
                    seq_payload_sum = payload_list[i][2] + 1
                    if (payload_list[j][0] == combination):
                        ack = payload_list[j][3]
                        if (seq_payload_sum == ack):
                            RTT = payload_list[j][6] - payload_list[i][6]
                            RTT = round(RTT,6)
                            RTT_time.append(RTT)
                            break
            else:
                if payload_list[i][0] == connections:
                    seq_payload_sum = payload_list[i][2] + payload_list[i][1]
                    if (payload_list[j][0] == combination):
                        ack = payload_list[j][3]
                        if (seq_payload_sum == ack):
                            RTT = payload_list[j][6] - payload_list[i][6]
                            RTT = round(RTT,6)
                            RTT_time.append(RTT)
                            break

# Function to print out the data that has been parsed into a desireable format 
def print_output():
    print("\nA) Total number of connections:",len(connections))
    print("_"*100,"\n")

    print("B) Connection Details:")

    for i in range (0,len(connections)):
        print("\nConnection:",i+1)
        data = list(connections[i])
        status = get_status(connections[i])
        print("Source Address:",data[0],"\nDestination Address:",data[1],"\nSource Port:",data[2],"\nDestination Port:",data[3],"\nStatus:",status)
        if connections[i] in complete_connections:
            window_size_calculation(connections[i])
            start_time,end_time = get_start_and_end_time(connections[i])
            src_to_dst,dst_to_src = count_packets(connections[i])
            data_from_src,data_from_dst = get_data_bytes(connections[i])
            get_RTT(connections[i])
            print("Start Time:",round(start_time-timestamp_list[0],6),"\nEnd Time:",round(end_time-timestamp_list[0],6),"\nDuration:",round(end_time-start_time,4))
            print("Number of packets sent from Source to Destination:",src_to_dst)
            print("Number of packets sent from Destination to Source:",dst_to_src)
            print("Total number of packets:",src_to_dst+dst_to_src)
            print("Number of data bytes sent from Source to Destination:",data_from_src)
            print("Number of data bytes sent from Destination to Source:",data_from_dst)
            print("Total number of data bytes:",data_from_src+data_from_dst)
            print("END")
    
    if len(complete_connections) != 0:
        print("_"*100,"\n")
        print("C) General\n")
        print("Total number of complete TCP connections:",len(complete_connections),"\nNumber of reset TCP connections:",len(reset_connections),"\nNumber of TCP connections that were still open when the trace capture ended:",(len(connections)-len(complete_connections)))
        print("_"*100,"\n")
        print("D) Complete TCP connections\n")
        print("Minimum time duration:",round(min(time),6),"seconds","\nMean time duration:",round(mean(time),6),"seconds","\nMaximum time duration:",round(max(time),6),"seconds")
        print("\nMinimum RTT value:",min(RTT_time),"seconds","\nMean RTT value:",round(mean(RTT_time),6),"seconds","\nMaximum RTT value:",max(RTT_time),"seconds")
        print("\nMinimum number of packets including both sent/received:",min(packet_counter),"packets","\nMean number of packets including both sent/received:",mean(packet_counter),"packets","\nMaximum number of packets including both sent/received:",max(packet_counter),"packets")
        print("\nMinimum receive window size including both send/received:",min(complete_connections_window),"bytes","\nMean receive window size including both send/received:",round(mean(complete_connections_window),6),"bytes","\nMaximum receive window size including both send/received:",max(complete_connections_window),"bytes")
        print("_"*100,"\n")
    else:
        print("_"*100,"\n")
        print("C) General\n")
        print("Total number of complete TCP connections:",0,"\nNumber of reset TCP connections:",0,"\nNumber of TCP connections that were still open when the trace capture ended:",0)
        print("_"*100,"\n")
        print("D) Complete TCP connections\n")
        print("Minimum time duration:",0,"seconds","\nMean time duration:",0,"seconds","\nMaximum time duration:",0,"seconds")
        print("\nMinimum RTT value:",0,"seconds","\nMean RTT value:",0,"seconds","\nMaximum RTT value:",0,"seconds")
        print("\nMinimum number of packets including both sent/received:",0,"packets","\nMean number of packets including both sent/received:",0,"packets","\nMaximum number of packets including both sent/received:",0,"packets")
        print("\nMinimum receive window size including both send/received:",0,"bytes","\nMean receive window size including both send/received:",0,"bytes","\nMaximum receive window size including both send/received:",0,"bytes")
        print("_"*100,"\n")


# Function that reads the file and splits into segments for each protocol
# This function calls the print_output function as well as other functions that are required to parse the data correctly
def read_file():
    fname = sys.argv[1]

    packet_data = []

    with open(fname, "rb") as f:
        header = f.read(24)
        global_header_information(header)

        packet_header = f.read(16)
        incl_len = packet_header_information(packet_header)
        while packet_header != b"":
            ts_sec,ts_usec,incl_len = packet_header_information(packet_header)
            packet_data = f.read(incl_len)

            IPv4_HEADER = packet_data[14:34]
            src_address,dst_address,IP_header_len,total_length = parse_packet_data_for_IPv4(IPv4_HEADER)

            TCP_HEADER = packet_data[34:incl_len]
            parse_packet_data_for_TCP(TCP_HEADER,src_address,dst_address,ts_sec,ts_usec,incl_len,IP_header_len,total_length)

            packet_header = f.read(16)
    f.close()

    print_output()

def main():
    read_file()
    

if __name__ == "__main__":
    main()
