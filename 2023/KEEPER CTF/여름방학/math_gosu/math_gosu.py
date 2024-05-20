import random
import sys

FLAG = "KEEPER{Math_maTh_mAtH_g0su_GoSu_g0sU}"
STAGE_NUM = 250
arithmetic_list = ["+", "-"]

def get_random_number():
    number_count = random.randrange(5, 10)
    expression = ""

    for i in range(0, number_count):
        expression += str(random.randrange(1000, 50000))
        expression += random.choice(arithmetic_list)

    expression += str(random.randrange(1000, 50000))
    expression += "="
    print(expression)

    return eval(expression[:-1])

def check_num(input_num, cal_num):
    try:
        input_num = int(input_num)
    except:
        print("Wrong Input....")
        sys.exit(0)

    if input_num != cal_num:
        print("Fail....")
        sys.exit(0)

def print_stage(idx):
    print(f"[STAGE {idx} / {STAGE_NUM}]")
    
for i in range(1, STAGE_NUM+1):
    print_stage(i)
    cal_num = get_random_number()
    input_num = input("Input: ")
    check_num(input_num, cal_num)

print(FLAG)
