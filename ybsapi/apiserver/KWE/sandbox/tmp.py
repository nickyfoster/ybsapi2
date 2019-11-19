from ybsapi.apiserver.KWE import UDPipeKeywordsExtractorProcess
from ybsapi.apiserver.resources import UDPIPE_MODEL, USERS_GROUPS_DATA
import json
import time

ts1 = time.time()


with USERS_GROUPS_DATA.open(encoding='utf-8') as file:
    users_groups_data = json.load(file)

groups_names = []
groups_descriptions = []

for user, groups in users_groups_data.items():
    for group in groups:
        try:
            groups_names.append(group['name'])
            groups_descriptions.append(group['description'])
        except Exception as e:
            pass

print(groups_descriptions)
exctractor = UDPipeKeywordsExtractorProcess(str(UDPIPE_MODEL))
result = exctractor.process_task(groups_descriptions)

parsed_result = [i for i in result if i]

print(parsed_result)

ts2 = time.time()
ts3 = ts2 - ts1
print(f"ELAPSED TIME: {ts3}")