import re

command = '100'

reg_ex = re.search(r'\d+', command)

if reg_ex:
    calories = reg_ex.group(0)

print(calories)