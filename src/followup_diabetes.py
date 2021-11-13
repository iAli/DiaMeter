def weight_control(weight, height):
    bmi = weight / ((height/100)**2)
    if bmi < 18.5:
        return 1
    elif 18.5 <= bmi < 25:
        return 0
    elif 25 <= bmi < 30:
        return 2
    else:
        return 3


def pressure_control(systolic, diastolic):
    if systolic > 140 or diastolic > 90:
        return 1
    else:
        return 0


def sugar_control(sugar, time):
    if sugar < 70:
        return 1
    elif time == "F" and sugar > 130:
        return 2
    elif time == "PP" and sugar > 180:
        return 2
    else:
        return 0
