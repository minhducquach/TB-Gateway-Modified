#     Copyright 2022. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from thingsboard_gateway.connectors.socket.socket_uplink_converter import SocketUplinkConverter, log
from thingsboard_gateway.gateway.statistics_service import StatisticsService

from thingsboard_gateway.connectors.socket.device_utils.omni_lock import OMNI_LOCK

import json

class BytesSocketUplinkConverter(SocketUplinkConverter):
    def __init__(self, config):
        self.__config = config
        self.device_info = {}
        self.format_str = {}

    @StatisticsService.CollectStatistics(start_stat_type='receivedBytesFromDevices',
                                         end_stat_type='convertedBytesFromDevice')
    def convert(self, data):
        dict_result = {}
        converter = None
        converter_name = self.filter_converter(data)
        if (converter_name == "OMNI_LOCK"):
            converter = OMNI_LOCK()
            dict_result = converter.convert(data)
        return dict_result, converter

    def filter_converter(self, data): # Return converter name of device
        return "OMNI_LOCK"