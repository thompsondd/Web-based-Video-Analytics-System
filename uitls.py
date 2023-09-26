import math
def convert_date_string(time):
    a_min =  60
    a_hour = a_min*60
    a_day = 24*a_hour
    output = []
    if int(time/a_day) !=0:
        d = int(time/a_day)
        time = max(0,time-d*a_day)
        output.append(f"{d}d")

    if int(time/a_hour) !=0:
        d = int(time/a_hour)
        time = max(0,time-d*a_hour)
        output.append(f"{d}h")

    if int(time/a_min) !=0:
        d = int(time/a_min)
        time = max(0,time-d*a_min)
        output.append(f"{d}m")
    
    if int(time) !=0:
        output.append(f"{int(math.ceil(time))}s")
    
    return " ".join(output)
