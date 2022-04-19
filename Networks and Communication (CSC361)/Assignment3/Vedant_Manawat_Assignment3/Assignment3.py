## Name: Vedant Manawat
## VNumber: V00904582
## April 4, 2021
## CSC 361 Programming Assignment 3

import struct
import sys
import statistics as stat
import math
from collections import OrderedDict

UDP_packets,ICMP_packets,ICMP_type_8,routers,Proto,Identification,all_Identification = [],[],[],[],[],[],[]
fragments = {}

# Find information in the packet header such as:
#   1. incl_len
#   2. time in seconds and microseconds 
def packet_header_information(packet_header):
    (ts_sec,) = struct.unpack('I',packet_header[0:4])
    (ts_usec,) = struct.unpack('<I',packet_header[4:8])
    (incl_len,) = struct.unpack("I",packet_header[8:12])

    return ts_sec,ts_usec,incl_len

# This function returns the source port and destination port that is being unpacked from specific bytes of the packet
def get_ports(HEADER):
    num1 = ((HEADER[0]&240)>>4)*16*16*16
    num2 = (HEADER[0]&15)*16*16
    num3 = ((HEADER[1]&240)>>4)*16
    num4 = (HEADER[1]&15)
    source_port = num1+num2+num3+num4

    num1 = ((HEADER[2]&240)>>4)*16*16*16
    num2 = (HEADER[2]&15)*16*16
    num3 = ((HEADER[3]&240)>>4)*16
    num4 = (HEADER[3]&15)
    dest_port = num1+num2+num3+num4

    return source_port,dest_port

# This function is to get the sequence number of the packets for trace files captured on windows
# The sequence number has two parts, so this function returns a tuple with both parts
def get_seqnum(datagram):
    seq = struct.unpack('BB',datagram[6:8])[1]
    (seq2,) = struct.unpack("H",datagram[6:8])
    seq_num = (seq,seq2)

    return seq_num

# This function is to get the type and code of the packet
# It returns the type and code along with the remainig datagram which is used to get more information 
def parse_ICMP(ICMP):
    (type,) = struct.unpack('B',ICMP[0:1])
    (code,) = struct.unpack('B',ICMP[1:2])

    ICMP_part = ICMP[28:]
    return type,ICMP_part,code

# This function gets calculates the timetsamp for each packet and returns the value to the caller
def timestamp_set(ts_sec,ts_usec,orig_time):
    timestamp = round((ts_sec+(ts_usec*0.000000001))-orig_time,9)
    return timestamp

# Find information in the IPv4 Header such as: 
#   1. Source and Destination address
#   2. Identification
#   3. MF bit
#   4. Fragment offset
#   5. Protocol
#   6. Timestamp
#   7. Time to live
#  
# The purpose of this function is to gather all the necessary information from the packet and identify whether it is UDP or ICMP
# then it will add the tuple containing the necessary information to the respective list which will be used in later
def parse_packet_data_for_IPv4(IPv4_HEADER,packet_data,incl_len,ts_sec,ts_usec):
    orig_time = 0

    src_addr = struct.unpack('BBBB',IPv4_HEADER[12:16])
    dst_addr = struct.unpack('BBBB',IPv4_HEADER[16:20])
    s_ip = str(src_addr[0])+'.'+str(src_addr[1])+'.'+str(src_addr[2])+'.'+str(src_addr[3])
    d_ip = str(dst_addr[0])+'.'+str(dst_addr[1])+'.'+str(dst_addr[2])+'.'+str(dst_addr[3])

    num1 = ((IPv4_HEADER[4]&240)>>4)*16*16*16
    num2 = (IPv4_HEADER[4]&15)*16*16
    num3 = ((IPv4_HEADER[5]&240)>>4)*16
    num4 = (IPv4_HEADER[5]&15)
    id = num1+num2+num3+num4
    
    (value,) = struct.unpack("B",IPv4_HEADER[6:7])
    bit = value & 32
    mf = 0
    if bit == 32:
        mf = 1

    frag = struct.unpack("BB",IPv4_HEADER[6:8])
    frag_offset = frag[1] * 8

    (protocol,) = struct.unpack('B',IPv4_HEADER[9:10])

    timestamp = timestamp_set(ts_sec,ts_usec,orig_time)

    (ttl,) = struct.unpack('B',IPv4_HEADER[8:9])

    if (protocol == 1):
        if (protocol not in Proto):
            Proto.append((protocol,"ICMP"))
    elif (protocol == 17):
        if (protocol not in Proto):
            Proto.append((protocol,"UDP"))

    datagram = packet_data[34:incl_len]

    src_port,dst_port = get_ports(datagram)

    all_Identification.append((id,frag_offset,timestamp))

    if (protocol == 17 and ((dst_port >= 33434) and (dst_port <=33529))):
        my_UDP_tuple = (s_ip,d_ip,protocol,src_port,dst_port,timestamp,ttl)
        if my_UDP_tuple not in UDP_packets:
            UDP_packets.append(my_UDP_tuple)
        if id not in Identification:
            if mf == 1:
                frag_offset = 0
                Identification.append((id,mf,frag_offset,timestamp))
    elif (protocol == 1):
        type,ICMP_part,code = parse_ICMP(datagram)
        if (type == 11):
            seq_num = get_seqnum(ICMP_part)
            src_port,dst_port = get_ports(ICMP_part)
            my_ICMP_tuple = (s_ip,d_ip,protocol,src_port,dst_port,timestamp,type,seq_num,code,id,ttl)
            if my_ICMP_tuple not in ICMP_packets:
                ICMP_packets.append(my_ICMP_tuple)
        elif (type == 8):
            seq_num = get_seqnum(datagram)
            src_port,dst_port = get_ports(ICMP_part)
            my_ICMP_type_8 = (s_ip,d_ip,protocol,src_port,dst_port,timestamp,type,seq_num,code,id,ttl)
            if my_ICMP_type_8 not in ICMP_packets:
                ICMP_type_8.append(my_ICMP_type_8)
        elif (type == 3 and code == 3):
            seq_num = get_seqnum(ICMP_part)
            src_port,dst_port = get_ports(ICMP_part)
            ICMP_packets.append((s_ip,d_ip,protocol,src_port,dst_port,timestamp,type,seq_num,code,id,ttl))
        elif (type == 0 and code == 0):
            seq_num = get_seqnum(datagram)
            src_port,dst_port = get_ports(ICMP_part)
            ICMP_packets.append((s_ip,d_ip,protocol,src_port,dst_port,timestamp,type,seq_num,code,id,ttl))

# This function is to look through the list of UDP packets and ICMP packets and find a match where the source ports for both packets is the same
# if the source port is the same then calcualte the difference in the two timestamps and add a tuple containing ip,difference in time and ttl to a
# list called routers (this is essentially the list of all intermediate routers). 
def get_intermediate_routers():
    for item in UDP_packets:
        for hop in ICMP_packets:
            if item[3] == hop[3]:
                diff_time = hop[5] - item[5]
                tup = (hop[0],diff_time,item[6])
                if tup not in routers:
                    routers.append(tup)

# This function works the same way as the one above, the only difference is that this is called in the pcap file is caputred on windows and
# instead of checking for a source port match it looks for the same sequence number. 
def get_intermediate_routers_widows():
    for item in ICMP_type_8:
        for hop in ICMP_packets:
            if item[7] == hop[7]:
                if hop[0] not in routers:
                    diff_time = hop[5] - item[5]
                    routers.append((hop[0],diff_time))


# This function finds out the number of fragments for a specific ID and then adds all instances of that ID to a dictionary 
def get_fragments():
    temp = []
    frag = False

    if (len(Identification) == 0):
        frag = False
    elif (len(Identification) != 0):
        frag = True

    for item in all_Identification:
        for match in Identification:
            if ((item[0] == match[0]) and (item not in temp)):
                temp.append(item)
    
    for item in temp:
        if item[0] in fragments:
            fragments[item[0]].append(item[1])
        else:
            fragments[item[0]] = [item[1]]

    return frag

# Credit for some snippets of code in this function goes to the following:
#   - https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
#   - https://stackoverflow.com/questions/29563953/most-pythonic-way-to-remove-tuples-from-a-list-if-first-element-is-a-duplicate
#   - https://stackoverflow.com/questions/3199171/append-multiple-values-for-one-key-in-a-dictionary

# Function to print out the data that has been parsed into a desireable format 
# Additionally, this function also calculates the average RTT for each intermediate node as well as standard deviation for it. 
def print_output():
    temp = list(set(Proto))
    temp = sorted(temp, key=lambda tup: tup[0])

    before_diff = 0
    sum_of_d = 0

    final_router_list = {}
    avg_sd_list = {}

    for item in routers:
        if item[0] in final_router_list:
            final_router_list[item[0]].append(item[1])
        else:
            final_router_list[item[0]] = [item[1]]

    for ip,time in final_router_list.items():
        mean = stat.mean(time)
        if (len(time) == 1):
            sd = 0
        else:
            for item in time:
                before_diff += (item - round(mean,6))
                diff = math.pow(before_diff,2)
                sum_of_d += diff
            var = sum_of_d/len(time)
            sd = math.sqrt(var)
        avg_sd_list[ip] = [mean,sd]
    

    if (len(ICMP_type_8) == 0):
        print("The IP address of the source node:", UDP_packets[0][0])
        print("The IP address of ultimate destination node:", UDP_packets[0][1])
        print("The IP address of the intermediate destination nodes:")
        for item in final_router_list:
            if item != UDP_packets[0][1]:
                print("\tRouter " + str(list(final_router_list.keys()).index(item) + 1) + ":",item)

        print("\nThe values in the protocol field of IP headers:")
        for item in temp:
            print("\t" + str(item[0]) + ":",item[1])

        isFrag = get_fragments()
        if (len(fragments) != 0):
            for id,frags in fragments.items():
                print("\nThe number of fragments created from the original datagram with id",id,"is:",len(frags))
                print("The offset of the last fragment is:",frags[-1])

        print()

        if (isFrag):
            for ip in avg_sd_list:
                print("The avg RTT between",UDP_packets[0][0],"and",ip,"is:",round(avg_sd_list[ip][0]*1000,6),"ms, the s.d. is:",round(avg_sd_list[ip][1]*1000,6))
        elif (not isFrag):
            for ip in avg_sd_list:
                print("The avg RTT between",UDP_packets[0][0],"and",ip,"is:",round(avg_sd_list[ip][0]*1000,6),"ms, the s.d. is:",round(avg_sd_list[ip][1]*1000,6))

    elif(len(ICMP_type_8) != 0):
        print("The IP address of the source node:",ICMP_type_8[0][0])
        print("The IP address of ultimate destination node:",ICMP_type_8[0][1])
        print("The IP address of the intermediate destination nodes:")
        for item in final_router_list:
            if item != ICMP_type_8[0][1]:
                print("\tRouter " + str(list(final_router_list.keys()).index(item) + 1) + ":",item)

        print("\nThe values in the protocol field of IP headers:")
        for item in temp:
            print("\t" + str(item[0]) + ":",item[1])

        isFrag = get_fragments()
        if (len(fragments) != 0):
            for id,frags in fragments.items():
                print("\nThe number of fragments created from the original datagram with id",id, "is:",len(frags))
                print("The offset of the last fragment is:",frags[-1])

        print()

        if (isFrag):
            print()
        elif (not isFrag):
            for ip in avg_sd_list:
                print("The avg RTT between",ICMP_type_8[0][0],"and",ip,"is:",round(avg_sd_list[ip][0]*1000,6),"ms, the s.d. is:",round(avg_sd_list[ip][1]*1000,6))

# Function that reads the file and splits into segments for each protocol
# This function calls the print_output function as well as other functions that are required to parse the data correctly
def read_file():
    fname = sys.argv[1]

    packet_data = []

    with open(fname, "rb") as f:
        header = f.read(24)

        packet_header = f.read(16)
        incl_len = packet_header_information(packet_header)
        while packet_header != b"":
            ts_sec,ts_usec,incl_len = packet_header_information(packet_header)
            packet_data = f.read(incl_len)

            IPv4_HEADER = packet_data[14:34]
            parse_packet_data_for_IPv4(IPv4_HEADER,packet_data,incl_len,ts_sec,ts_usec)
            packet_header = f.read(16)
    f.close()

    if (len(ICMP_type_8) == 0):
        get_intermediate_routers()
    elif(len(ICMP_type_8) != 0):
        get_intermediate_routers_widows()
    print_output()

def main():
    read_file()
    

if __name__ == "__main__":
    main()
