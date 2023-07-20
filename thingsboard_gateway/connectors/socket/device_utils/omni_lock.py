from thingsboard_gateway.connectors.socket.socket_uplink_converter import SocketUplinkConverter, log
from thingsboard_gateway.gateway.statistics_service import StatisticsService

import time

def findKey(arr, key):
    for i, k in enumerate(arr):
        if key in k:
            return i
    return -1

class OMNI_LOCK():
    def __init__ (self):
        self.device_info = {
            "deviceName": "OMNI_LOCK_",
            "deviceType": "lock",
            "header": "CMDR",
            "manu_code": "",
            "imei": "",
            "time_start": "",
            "lastcmd": "",
            "data": "",
            "status": -1,
            "userid": "",
            "timestamp": "",
            "cycle": "",
            "voltage": 0,
            "sigval": 0,
            "reset": 0,
            "ring_time": 5,
            "tracking_identification": "",
            "utc_time": "",
            "loc_status": "",
            "lat": 11,
            "lon": 106,
            "hem": "",
            "num_satellites": "",
            "hdop": "",
            "utc_date": "",
            "altitude": 0,
            "height_unit": "",
            "mode_indication": "",
            "unlock_res": -1,
            "customerID": "",
        }
        self.format_str = {
            "cmd_format": "header,manu_code,imei,time_start,lastcmd,data",
            "L1": "userid,timestamp,cycle",
            "H0": "status,voltage,sigval",
            "Q0": "voltage",
            "D0": "tracking_identification,utc_time,loc_status,lat,lon,hem,num_satellites,hdop,utc_date,altitude,height_unit,mode_indication",
            "L0": "unlock_res,customerID,timestamp",
            "S5": "voltage,sigval,num_satellites,status,retention"
        }

    @StatisticsService.CollectStatistics(start_stat_type='receivedBytesFromDevices',
                                         end_stat_type='convertedBytesFromDevice')
    
    def convert(self, data):
        if data is None:
            return {}

        # data_parsed = json.loads(data)
        data_decoded = data.decode('utf-8').strip("*#\n")
        # print(data_decoded.strip("*#\n"))
        # format_str = "header,manu_code,imei,time,lastcmd,data"
        keys = self.format_str["cmd_format"].split(",")
        values = data_decoded.split(",", 5)
        data_parsed = dict(zip(keys, values))
        # if (data_parsed['lastcmd'] == "L1"):
        # cmd_format = "userid,timestamp,cycle"
        data_keys = self.format_str[data_parsed["lastcmd"]].split(",")
        data_values = data_parsed["data"].split(",")
        data_dict = dict(zip(data_keys, data_values))
        data_parsed.update(data_dict)

        self.device_info.update(data_parsed)

        dict_result = {
            "deviceName": self.device_info["deviceName"] + self.device_info["imei"],
            "deviceType": self.device_info["deviceType"]
        }

        try:
            dict_result["telemetry"] = [
                {
                    "timestamp": ""
                },
                {
                    "voltage": -1
                },
                {
                    "lat": 0
                },
                {
                    "lon": 0
                }
            ]
            dict_result["attributes"] = [
                {
                    "status": -1
                },
                {
                    "imei": ""
                },
                {
                    "lastcmd": ""
                },
                {
                    "userid": ""
                }
            ]

            for section in ('attributes', 'telemetry'):
                for key, value in self.device_info.items():
                    try:
                        index = findKey(dict_result[section], key)
                        if index != -1 and value is not None:
                            dict_result[section][index][key] = value
                        # else:
                        #     log.error('Key for not found in config')

                    except Exception as e:
                        log.exception(e)
        except Exception as e:
            log.exception(e)

        log.debug(dict_result)
        # print(dict_result)
        return dict_result
    
    def converter_downlink(self, data):
        data_return = ""
        if ("bike_search" in data and data["bike_search"]):
            data_return = "FFFF" + f"*CMDS,{self.device_info['manu_code']},{self.device_info['imei']},{(self.device_info['time_start'])},S8,{self.device_info['ring_time']},0#\n".encode("utf-8").hex()
            self.device_info['lastcmd'] = "S8"
            data_return = bytes.fromhex(data_return)
            print("DATA_RETURN:", data_return)
        elif ("status" in data and data["status"] == 0):
            timestamp = str(int(time.time()))
            self.device_info['timestamp'] = timestamp
            data_return = "FFFF" + f"*CMDS,{self.device_info['manu_code']},{self.device_info['imei']},{str(self.device_info['time_start'])},L0,{self.device_info['reset']},{self.device_info['userid']},{timestamp}#\n".encode("utf-8").hex()
            self.device_info['lastcmd'] = "L0"
            data_return = bytes.fromhex(data_return)
            print("DATA_RETURN:", data_return)
        elif ("location" in data):
            data_return = "FFFF" + f"*CMDS,{self.device_info['manu_code']},{self.device_info['imei']},{str(self.device_info['time_start'])},D0#\n".encode("utf-8").hex()
            self.device_info['lastcmd'] = "D0"
            data_return = bytes.fromhex(data_return)
            print("DATA_RETURN:", data_return)
        elif ("lock_info" in data):
            data_return = "FFFF" + f"*CMDS,{self.device_info['manu_code']},{self.device_info['imei']},{str(self.device_info['time_start'])},S5#\n".encode("utf-8").hex()
            self.device_info['lastcmd'] = "S5"
            data_return = bytes.fromhex(data_return)
            print("DATA_RETURN:", data_return)
        else:
            data_return = "Can't send request"
        return data_return

    

