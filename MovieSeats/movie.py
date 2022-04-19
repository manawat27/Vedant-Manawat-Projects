import random
from termcolor import colored

LO_L = 1
LO_R = 2
HI_L = 3
HI_R = 4
MI_L = 5
MI_R = 6

theatre = {}
for_seats = []

def create_theatre():
    rows = int(input("Enter number of rows: "))

    for i in range(rows):
        seats = int(input("Enter number of seats for row " + chr(i+65) + ": "))
        theatre[chr(i+65)] = seats

def show_theatre():
    global theatre_temp
    print("\n  ************************* SCREEN ***************************\n")
    theatre_temp = theatre.copy()
    theatre.clear()

    for k,v in theatre_temp.items():
        row_list = {}
        for i in range(v):
            seat_num = str(k) + str(i+1)
            occupied = random.choice([True,False])
            row_list[seat_num] = occupied
            for_seats.append(occupied)
        theatre[k] = row_list
    
    for k,v in theatre.items():
        if (k == 'A'):
            row = [k] + ["\t"] + list(v)[0:1] + ["\t"] + list(v)[1:9] + ["\t"] + list(v)[9:] + ["\t"]
            for i in row:
                if (i in v and v[i] == True):
                    print(colored(i,'red'), end=" ")
                else:
                    print(i,end=" ")
            print()
        elif (k == 'F'):
            row = [k] + ["\t"] + list(v)[0:2] + ["\t"] + list(v)[2:11] + ["\t"] + list(v)[11:13] + ["   "] + list(v)[13:]
            for i in row:
                if (i in v and v[i] == True):
                    print(colored(i,'red'), end=" ")
                else:
                    print(i,end=" ")
            print()
        else:
            row = [k] + ["\t"] + list(v)[0:2] + ["\t"] + list(v)[2:11] + ["\t"] + list(v)[11:]
            for i in row:
                if (i in v and v[i] == True):
                    print(colored(i,'red'), end=" ")
                else:
                    print(i,end=" ")
            print()

def find_middle(input_list):

    if (len(input_list)%2 == 0):
        middle1 = int(len(input_list) / 2) - 1
        middle2 = int(len(input_list) / 2) 
        return(input_list[0:middle1],[input_list[middle1],input_list[middle2]],input_list[middle2+1:])
    else:
       middle = int(len(input_list) / 2)
       return (input_list[0:middle],input_list[middle],input_list[middle+1:])

def find_empty(row,num_seats,side):
    seats = []
    empty = []
    temp_dict = {}

    for item in theatre_temp.keys():
        begin = 0
        seats.append(for_seats[begin:theatre_temp[item]])
        begin = theatre_temp[item]

    # for i in range(len(seats)):
    #     temp_dict[chr(i+65)] = seats[i]
    # print(ord(row) - 65)

    if (num_seats < len(seats[ord(row)-65])):
        if (side == 0):
            side_pref = seats[ord(row)-65]
            print(side_pref)
            for j in range(len(side_pref)-num_seats+1):
                try:
                    if not side_pref[j]:
                        if not side_pref[j+num_seats]:
                            start = j
                            for q in range(num_seats):
                                empty.append(chr(row + 65) + str(start + q + 1))
                                # theatre[row][start + q] = True
                            return empty
                except:
                    break

    return -1

def seat_selection():
    '''
    1. Lower left: smallest row letter and smallest number
    2. Lower right: smallest row letter and highest number
    3. Higher left: largest row letter and smallest number 
    4. Higher right: largest row letter and highest number 
    5. Middle left: middle row letter and lowest number
    6. Middle right: middle row letter and highest number
    '''

    num_seats = int(input("\nEnter number of seats you want: "))
    print("\n  1.Lower Left(LO_L)\n  2.Lower Right(LO_R)\n  3.Higher Left(HI_L)\n  4.Higest Right(HI_R)\n  5.Middle Left(MI_L)\n  6.Middle Right(MI_R)")
    preference = int(input("Select a preference of seats as shown above: "))

    low,middle,high = find_middle(list(theatre.keys()))
    
    if (preference == 1 or preference == 2):
        if (preference == 1):
            for item in low:
                side = 0
                possible_seats = find_empty(item,num_seats,side)
                print(possible_seats)
                exit(0)
        # elif (preference == 2):
            #hi
    elif (preference == 3 or preference == 4):
        print(high)
    elif (preference == 5 or preference == 6):
        print(middle)
    
def main():
    create_theatre()
    show_theatre()
    seat_selection()

if __name__ == "__main__":
    main()