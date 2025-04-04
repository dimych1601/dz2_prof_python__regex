# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

fio_list = []
phone_pattern = r"(\+7|8)[\s-]*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(?(доб.)?\s*(\d+)?\)?"
phone_substitution = r"+7(\2)\3-\4-\5 \6 \7"
remove_indexes = []
for i, contact in enumerate(contacts_list):
    if i == 0:
        continue
    lastname = contact[0].split()
    firstname = contact[1].split()

    if len(firstname) > 1:
        contact[1] = firstname[0]
        contact[2] = firstname[1]
    if len(lastname) == 2:
        contact[0] = lastname[0]
        contact[1] = lastname[1]
    elif len(lastname) == 3:
        contact[0] = lastname[0]
        contact[1] = lastname[1]
        contact[2] = lastname[2]

    fullname = " ".join([contact[0], contact[1]])

    if i > 1 and " ".join([contact[0], contact[1]]) in fio_list:
        repeating_name_index = fio_list.index(fullname)
        remove_indexes.append(i)
        if contacts_list[repeating_name_index+1][2] == "":
            contacts_list[repeating_name_index+1][2] = contact[2]
        if contacts_list[repeating_name_index+1][3] == "":
            contacts_list[repeating_name_index+1][3] = contact[3]
        if contacts_list[repeating_name_index+1][4] == "":
            contacts_list[repeating_name_index+1][4] = contact[4]
        if contacts_list[repeating_name_index+1][5] == "":
            contacts_list[repeating_name_index+1][5] = contact[5]
        if contacts_list[repeating_name_index+1][6] == "":
            contacts_list[repeating_name_index+1][6] = contact[6]

    fio_list.append(fullname)
    fixed_phone_number = re.sub(phone_pattern,  phone_substitution, contacts_list[i][5])
    contacts_list[i][5] = fixed_phone_number.strip()

for i in reversed(remove_indexes):
    contacts_list.pop(i)

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)