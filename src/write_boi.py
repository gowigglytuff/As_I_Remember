import json

# data = {"Germany" : "Berlin",
#         "UK" : "London"
#         }

# with open("test_data.txt", "w") as test_file:
#         json.dump(data, test_file)

with open("test_data.txt") as test_file:
        data = json.load(test_file)

for entry in data:
        print(entry)