from pathlib import Path
import openpyxl

class EventDecision:
    def __init__(self, row):
        self.time = row[0].value
        self.decision = row[1].value
        self.user = row[2].value
        self.confidence = row[3].value
        self.event_id = row[4].value
        self.decision_id = row[5].value

    def __repr__(self):
        return f'({self.user},{self.event_id},{self.decision},{self.confidence})'
    
    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.user == other.user and self.event_id == other.event_id and self.decision == other.decision and self.confidence == other.confidence
    
    def __hash__(self):
        return hash((self.user, self.event_id, self.decision, self.confidence))

    def __lt__(self, value):
        return self.time < value.time


file = Path('backups') / 'cry-wolf_20200125_14-35-09_patched.xlsx'
wb = openpyxl.load_workbook(file)
event_sheet = wb['EventDecision']

users = {}
resubmit_count = 0
row_count = 0
for row in event_sheet.iter_rows(min_row=2):
    row_count += 1
    ed = EventDecision(row)
    if ed.user not in users:
        users[ed.user] = { ed.event_id : {ed} }
    else:
        if ed.event_id in users[ed.user]:
            users[ed.user][ed.event_id].add(ed)
            resubmit_count += 1
        else:
            users[ed.user][ed.event_id] = {ed}

print(f"Number of unique event decisions: {row_count}")
print(f"Number of resubmitted event decisions: {resubmit_count}")
print(f"Number of unique users: {len(users.keys())}")
print("Users+event ids with changes on resubmit:")        

count_changed = 0
count_changed_events = 0

change_counts_by_user = {}

for user, v in users.items():
    for event_id, decisions in v.items():
        if len(decisions) > 1:
            if user in change_counts_by_user:
                change_counts_by_user[user] += 1
            else:
                change_counts_by_user[user] = 1
            count_changed += len(decisions)-1
            count_changed_events += 1
            print(sorted(decisions))

print(f"Number of changes on resubmit: {count_changed}")
print(f"Number of unique events that were changed: {count_changed_events}")
print(f"Users who changed their answers: {change_counts_by_user}")


