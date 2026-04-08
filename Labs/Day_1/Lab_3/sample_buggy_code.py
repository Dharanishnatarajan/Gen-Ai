def find_average(values):
    total = 0
    for i in range(len(values)):
        total += values[i]
    return total / len(values)


def append_user(users=[]):
    users.append("new-user")
    return users


def load_config(path):
    file = open(path, "r")
    data = file.read()
    return eval(data)
