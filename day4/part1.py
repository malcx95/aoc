import numpy as np


class Night:

    def __init__(self, guard_id):
        self.guard_id = guard_id
        self.shift_start = None
        self.sleeps = []

    def num_minutes_sleeping(self):
        res = 0
        for start, end in self.sleeps:
            res += end - start
        return res

    def __str__(self):
        return 'Guard:{}, Shift:{}, Sleeps:{}, Wakes:{}'\
                .format(self.guard_id, self.shift_start, self.sleep_start,
                       self.sleep_end)

    def __repr__(self):
        return 'Guard:{}, Shift:{}, Sleeps:{}, Wakes:{}'\
                .format(self.guard_id, self.shift_start, self.sleep_start,
                       self.sleep_end)

def extract_id(rest_string):
    split = rest_string.split(" ")
    return int(split[1].replace("#", ""))


def get_minute(date):
    _, time = date.split(" ")
    return int(time.split(":")[1])

night_lines = []

with open("input.txt") as f:
    night_lines = f.readlines()

night_lines.sort(key=lambda l: l[:18])
with open("input.txt", 'w') as f:
    f.writelines(night_lines)


nights = []
curr_night = None
curr_sleep_start = 0

for line in night_lines:
    timestamp = line[:18].replace("[", "").replace("]", "")
    # date, time = timestamp.split(" ")
    rest = line[19:].replace("\n", "")
    if "Guard" in rest:
        if curr_night is not None:
            nights.append(curr_night)
        curr_night = Night(extract_id(rest))
        curr_night.shift_start = timestamp
    elif "falls" in rest:
        curr_sleep_start = get_minute(timestamp)
    elif "wakes" in rest:
        sleep_end = get_minute(timestamp) - 1
        curr_night.sleeps.append((curr_sleep_start, sleep_end))

nights.append(curr_night)
        
guards_sleep = {}
for night in nights:
    sleep_time = night.num_minutes_sleeping()
    if night.guard_id not in guards_sleep:
        guards_sleep[night.guard_id] = (0, 0)
    sltime, num = guards_sleep[night.guard_id]
    guards_sleep[night.guard_id] = (sltime + sleep_time, num + 1)

print(guards_sleep)

longest_sleep = 0
most_sleepy_guard = None
for guard_id, (sleep_time, num) in guards_sleep.items():
    if longest_sleep < sleep_time:
        longest_sleep = sleep_time
        most_sleepy_guard = guard_id

print("Sleepiest:", most_sleepy_guard)

nights_with_guard = list(filter(lambda g: g.guard_id == most_sleepy_guard, nights))

sleep_times = np.zeros(60)

for night in nights_with_guard:
    for (start, end) in night.sleeps:
        sleep_times[start:end+1] += 1

print(sleep_times)
print("Time at most asleep", np.argmax(sleep_times))


guard = None
minute = None
max_minute = 0

for guard_id in guards_sleep:
    nights_with_guard = list(filter(lambda g: g.guard_id == guard_id, nights))
    sleep_times = np.zeros(60)
    for night in nights_with_guard:
        for (start, end) in night.sleeps:
            sleep_times[start:end+1] += 1
    maximum = np.max(sleep_times)
    if maximum > max_minute:
        guard = guard_id
        minute = np.argmax(sleep_times)
        max_minute = maximum

print("Guard:", guard)
print("minute:", minute)
print("mult:", guard*minute)
