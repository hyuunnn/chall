import random
import sys

FLAG = "KEEPER{math_masTeR_MasTeR_mAsTeR_masTER_MaSTeR_MASTER}"
STAGE_NUM = 250
arithmetic_list = ["+", "-", "*"]

def get_random_number():
    number_count = random.randrange(5, 10)
    expression = ""
    num_list = []

    for i in range(0, number_count):
        num_list.append(str(random.randrange(1000, 50000)))
        expression += num_list[i]
        expression += random.choice(arithmetic_list)

    num_list.append(str(random.randrange(1000, 50000)))
    expression += num_list[-1]
    expression += "="
    expression += str(eval(expression[:-1]))
    
    erase_num = random.choice(num_list)
    expression = expression.replace(erase_num, "?", 1)

    print(expression)
    return int(erase_num)

def check_num(input_num, erase_num):
    try:
        input_num = int(input_num)
    except:
        print("Wrong Input....")
        sys.exit(0)

    if input_num != erase_num:
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
