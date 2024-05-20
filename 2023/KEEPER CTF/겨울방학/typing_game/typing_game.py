import random
import sys
from faker import Faker

FLAG = "KEEPER{faker_is_very_useful_library}"
STAGE_NUM = 200
faker = Faker(['it_IT', 'en_US', 'ja_JP', 'ko_KR', 'zh_CN'])

def print_stage(idx):
    print(f"[STAGE {idx} / {STAGE_NUM}]")

def make_answer(idx):
  if idx < 50:
    answer = faker.name()
  elif idx < 100:
    answer = faker.job()
  elif idx < 150:
    answer = faker.address().replace("\n", " ")
  else:
    answer = faker.sentence(idx)
  
  return answer

for i in range(1, STAGE_NUM+1):
  print_stage(i)
  answer = make_answer(i)
  print(f"answer: {answer}")
  input_data = input("Input: ")
  if input_data != answer:
    print("Wrong Input....")
    sys.exit(0)

print(FLAG)
