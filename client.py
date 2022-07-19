import requests
BASE = "http://127.0.0.1:5000/"

note_num = input()
response = requests.put(BASE + "cutoff/" + note_num, {"member": '0003', "channel": 'C2', "time": '00:01:50.683', "group": '01'})
print(response.json())
note_num = input()
response = requests.get(BASE + "cutoff/" + note_num)
print(response.json())