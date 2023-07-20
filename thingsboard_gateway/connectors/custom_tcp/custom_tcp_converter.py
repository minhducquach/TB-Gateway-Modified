from thingsboard_gateway.connectors.converter import Converter, log    # Import base class for the converter and log ("converter.log" in logs directory).
import json

class CustomTCPUplinkConverter(Converter):    # Definition of class.
    def __init__(self, config):    # Initialization method
        self.__config = config    # Saving configuration to object variable
        self.result_dict = {
            'deviceName': config.get('name', 'CustomSerialDevice'),
            'deviceType': config.get('deviceType', 'default'),
            'attributes': [],
            'telemetry': []
        }    # template for a result dictionary.
    def convert(self, config, data: bytes):    # Method for conversion data from device format to ThingsBoard format.
        data_parsed = json.loads(data)
        self.result_dict["deviceName"] = data_parsed["name"]
        self.result_dict["deviceType"] = data_parsed["type"]
        for section in ('telemetry', 'attributes'):
                for item in config[section]:
                    try:
                        converted_data = data_parsed[item['key']]
                        print("CONVERT: ", converted_data)

                        if item.get('key') is not None:
                            self.result_dict[section].append(
                                {item['key']: converted_data})
                        else:
                            log.error('Key for %s not found in config: %s', config['type'], config['section_config'])
                    except Exception as e:
                        log.exception(e)
        print(self.result_dict)
        return self.result_dict    # returning result dictionary after all iterations.