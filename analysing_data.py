
import pickle


with open('info_list_2', 'rb') as il2:
    info_list_2 = pickle.load(il2)

info_list_2_descriptions = []

for info in info_list_2:
    info_list_2_descriptions.append(info[4]) 

print(len(info_list_2_descriptions))
count = 0

for desc in info_list_2_descriptions:
    desc = desc.lower()
    if 'api' in desc:
            count += 1

print(count)
