import requests

# def func():

#     token_res = requests.post("http://192.168.1.226:2680/api/auth/login", json = {
#         "username": "tenant@thingsboard.org",
#         "password": "tenant"
#     })

#     token = token_res.json()["token"]

#     list_device_rep = requests.get("http://192.168.1.226:2680/api/tenant/devices?deviceName=OMNI_LOCK_862205053707503", headers = {"Authorization": f"Bearer {token}"})

#     list_device = list_device_rep.json()

#     if (list_device_rep.status_code == 200):
#         return list_device["id"]["id"]
#     else:
#         return None
# print(func())

a = {"a":1}
def func(dict):
    dict["a"] = 3

func(a)
print(a)