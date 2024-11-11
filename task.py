import pandas as pd 
import json

# Give the basic structure of the json 
def course_details(time_table):
    return ({
        "course_code" : int(time_table["COM COD"][1]),
        "course_title": time_table["COURSE TITLE"][1], 
        "credits": {
            "lecture" : time_table["CREDIT"][1] , 
            "practical": time_table["Unnamed: 4"][1], 
            "units": time_table["Unnamed: 5"][1],
         },
        "sections": section_details(time_table),
    })


def section_details(time_table): 

    current_sec = {} 
    sections = []
    count = 1
    
    #iterate through all the sections from the excel file. 
    #if finds NaN, then adds the instructor to the current section or else append the section to sections array and create a new section
    while(count != (time_table.shape[0])): 

        sec = time_table["SEC"][count]
        instr = time_table["INSTRUCTOR-IN-CHARGE / Instructor"]
        room = time_table["ROOM"]
        timings = time_table["DAYS & HOURS"]
       
       #if section is NaN 
        if not isinstance(sec, str): 
            current_sec["instructors"].append(instr[count])
            count += 1 

        else : 
            if (count != 1): 
                sections.append(current_sec.copy()) #Python call by reference, that is why .copy() is used

            current_sec = {
                "section_type": returnType(sec), 
                "section_number": sec, 
                "instructors": [instr[count]], 
                "room": int(room[count]),
                "timings": get_time_dict(timings[count])
            }
            count += 1
        
    sections.append(current_sec)
    return sections

def returnType(sec): 
    section_types = {
        "L": "Lecture",
        "T": "Tutorial",
        "P": "Practical"
    }
    return section_types.get(sec[0])

def get_time_dict(time): 
    all_slots = [] # contians differnet slot Eg. [['M', 'W', '3'], ['Th', '9']]
    arr = time.split()
    count = 0 

    for i in range(len(arr)): 
        if (arr[i].isdigit()): 

            # case for "M W 3 9" if ever existed
            if (i == count): 
                all_slots[-1].append(arr[i])
                count =  i + 1 
                continue
            
            #when find a time slot digit, we take the sub array
            all_slots.append(arr[count:(i + 1)])
            count = i + 1 

        
    formatted_data = []
    for entry in all_slots:
        days = []
        times = []
        
        for item in entry:
            try:
                times.append(int(item))  
            except ValueError:
                days.append(item) 

        for day in days:
            formatted_data.append({"day": day, "time": times})

    return formatted_data


#iterates through all the sheets of the excel file

courses = [] 

for i in range(1,7): 
    time_table = pd.read_excel("timetable.xlsx", sheet_name= ("S" + str(i)), header = 1) 
    course = json.dumps(course_details(time_table), indent=4)
    print(course)
    courses.append(course)





