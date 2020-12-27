import random

members = []
member = {
    "Member ID": "",
    "Surname": "",
    "Year joined": 0,
    "Member status": "Silver",
    "Nights booked": 0,
    "Points balance": 0,
}

def blank_member():
    member = {
        "Member ID": "",
        "Surname": "",
        "Year joined": 0,
        "Member status": "Silver",
        "Nights booked": 0,
        "Points balance": 0,
    }
#end def

def write_to_file(file_name, to_write, mode):
    try:
        file = open(file_name, mode)
        file.writelines(to_write)
    except:
        print("An error occured while opening the file")
#end def

def open_file_read(file_name):
    global members
    members = []
    try:
        file = open(file_name, "r")
    except:
        print("An error occured while opening the file")
    data = file.readlines()
    for line in data:
        split_line = parse_line(line)
        if split_line is not None:
            members.append(split_line)
    
    #end for
#end def

def parse_line(line):
    try:
        stripped_line = line.strip()
        split_line = stripped_line.split(",")
        return split_line
    except:
        return None
#end def

def add_member():
    for attribute in member:
        if attribute == "Member ID" or attribute == "Member status":
            pass
        else:
            member[attribute] = input("Enter the " + attribute + ": ")
    member["Member ID"] = member["Surname"][0:3] + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + member["Year joined"][2:4]
    string = dict_to_string(member)
    write_to_file("SampleData2017.txt", string, "a")
    blank_member()
#end def

def dict_to_string(dict):
    string = ""
    for attribute in dict:
        string += str(dict[attribute]) + ","
    string = string [:-1] + "\n"
    return string
#end def

def twoD_array_to_string(array):
    string = ""
    for item in array:
        for data in item:
            string += str(data) + ","
        string = string[:-1] + "\n"
    return string
#end def

def update_status(selected_index):
    if members[selected_index][4] >= 100:
        members[selected_index][3] = "Platinum"
    elif members[selected_index][4] >= 30:
        members[selected_index][3] = "Gold"
    else:
        pass
#end def

def update_points(selected_index, nights, redeem_or_add):
    #nights = int(nights)
    if redeem_or_add == "add":
        status = members[selected_index][3]
        if status == "Silver":
            members[selected_index][5] = int(members[selected_index][5]) + nights * 2500
        elif status == "Gold":
            members[selected_index][5] = int(members[selected_index][5]) + nights * 3000
        else:
            members[selected_index][5] = int(members[selected_index][5]) + nights * 4000
    else:
        if int(members[selected_index][5]) - nights * 25000 >= 0:
            members[selected_index][5] = int(members[selected_index][5]) - nights * 25000
            return "Points deducted"
        else:
            return "Not enough points"
        
#end def

def edit_member():
    edit_member_menu()
#end def

def print_edit_member_menu():
    print("---------------------------")
    print("|           Menu          |")
    print("| 1.Record nights booked  |")
    print("| 2.Redeem pionts         |")
    print("| 3.Quit                  |")
    print("---------------------------")
#end def

def edit_member_menu():
    print_edit_member_menu()
    edit_member_menu_choice()
#end def

def record_nights_booked(selected_index):
    valid_amount = False
    while valid_amount != True:
        nights = int(input("Enter the number of nights you want to add: "))
        if nights <= 14:
            valid_amount = True
        else:
            print("Too many nights you can only add a maximum of 14")
    members[selected_index][4] = int(members[selected_index][4]) + nights
    update_points(selected_index, nights, "add")
    update_status(selected_index)
    string = twoD_array_to_string(members)
    write_to_file("SampleData2017.txt", string, "w")
    
#end def

def redeem_points(selected_index):
    nights = int(input("How many nights do you want to redeem: "))
    redeemed = update_points(selected_index, nights, "redeem")
    print(redeemed)
    if redeemed == "Points deducted":
        members[selected_index][4] = int(members[selected_index][4]) + nights
        update_status(selected_index)
        string = twoD_array_to_string(members)
        write_to_file("SampleData2017.txt", string, "w")        
        
    else:
        return
#edn def

def edit_member_menu_choice():
    valid_choice = False
    choice = None
    while choice != 3:
        valid_choice = False
        choice = None        
        while valid_choice != True:
            choice = input("Enter the option you want: ")
            valid_choice = validate_choice(choice, 3)
        if choice == "1":
            record_nights_booked(select_member())
        elif choice == "2":
            redeem_points(select_member())
        else:
            print("Back to main menu")
            return
        print_edit_member_menu()
#end def

def select_member():
    open_file_read("SampleData2017.txt")
    member_found = False
    while member_found != True:
        selected_index = 0
        selected_member_ID = input("Enter the member ID of the member you want to edit: ")
        for member in members:
            if member[0] == selected_member_ID:
                return selected_index
            else:
                selected_index += 1
        print("Member ID not found")
#edn def

def view_bookings():
    open_file_read("SampleData2017.txt")
    print("-------------------------------------------------------------------------------------------------")
    print("|Member ID      |Surname        |Year joined    |Member status  |Nights booked  |Points balance |")
    print("-------------------------------------------------------------------------------------------------")
    for member in members:
        for attribute in member:
            num_of_spaces = 15 - len(attribute)
            print("|" + attribute + " " * num_of_spaces, end = "")
        print("|")
    print("-------------------------------------------------------------------------------------------------")
#end def

def validate_choice(choice, maximum):
    try:
        choice = int(choice)
        if choice >= 1 and choice <= maximum:
            valid_choice = True
        else:
            print("invalid choice")
            valid_choice = False
    except:
        print("invalid choice")
        valid_choice = False
    return valid_choice
#end def

def menu_choice():
    valid_choice = False
    choice = None
    while choice != 4:
        valid_choice = False
        choice = None        
        while valid_choice != True:
            choice = input("Enter the option you want: ")
            valid_choice = validate_choice(choice, 4)
        if choice == "1":
            add_member()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            edit_member()
        else:
            print("Program ended")
            return
        print_menu()
#end def

def menu():
    print_menu()
    menu_choice()
#end def
    
def print_menu():
    print("---------------------")
    print("|        Menu       |")
    print("| 1.Add member      |")
    print("| 2.View bookings   |")
    print("| 3.Edit member     |")
    print("| 4.Quit            |")
    print("---------------------")
#end def

def main():
    open_file_read("SampleData2017.txt")
    menu()
    #end if
#end def

main()