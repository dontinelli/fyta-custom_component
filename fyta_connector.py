# coding: utf-8

from datetime import datetime
import pytz

from fyta_client import Client

PLANT_STATUS = {
    1: "too low",
    2: "low",
    3: "perfect",
    4: "high",
    5: "too high",
    }

class FytaConnector(object):
    def __init__(self, email, password, access_token = "", expiration = None, timezone: pytz.timezone = pytz.utc):

        self.email = email
        self.password = password
        self.client = Client(email, password, access_token, expiration)
        self.online = False
        self.plant_list = {}
        self.plants = {}
        self.timezone = timezone

    async def test_connection(self) -> bool:

        return await self.client.test_connection()


    async def login(self) -> bool:
        login = await self.client.login()
        self.access_token = login["access_token"]
        self.expiration = login["expiration"]
        self.online = True

        return login


    async def update_data(self):
        self.plant_list = await self.client.get_plants()

        return self.plant_list


    async def update_all_plants(self):
        plants = {}

        plant_list = await self.update_data()

        for plant in plant_list.keys():
            current_plant = await self.update_plant_data(plant)
            if current_plant is not {}:
                plants |= {plant: current_plant}

        self.plants = plants

        return plants

    async def update_plant_data(self, plant_id: int):

        p = await self.client.get_plant_data(plant_id)
        plant_data = p["plant"]

        if plant_data["sensor"] is None:
            return {}

        current_plant = {}
        current_plant |= {"online": True}
        current_plant |= {"battery_status": bool(plant_data["sensor"]["is_battery_low"])}
        current_plant |= {"sw_version": plant_data["sensor"]["version"]}
        current_plant |= {"plant_id": plant_data["plant_id"]}
        current_plant |= {"name": plant_data["nickname"]}
        current_plant |= {"scientific_name": plant_data["scientific_name"]}
        current_plant |= {"status": int(plant_data["status"])}
        current_plant |= {"temperature_status": int(plant_data["measurements"]["temperature"]["status"])}
        current_plant |= {"light_status": int(plant_data["measurements"]["light"]["status"])}
        current_plant |= {"moisture_status": int(plant_data["measurements"]["moisture"]["status"])}
        current_plant |= {"salinity_status": int(plant_data["measurements"]["salinity"]["status"])}
        #current_plant |= {"ph": float(plant_data["measurements"]["ph"]["values"]["current"])}
        current_plant |= {"temperature": float(plant_data["measurements"]["temperature"]["values"]["current"])}
        current_plant |= {"light": float(plant_data["measurements"]["light"]["values"]["current"])}
        current_plant |= {"moisture": float(plant_data["measurements"]["moisture"]["values"]["current"])}
        current_plant |= {"salinity": float(plant_data["measurements"]["salinity"]["values"]["current"])}
        current_plant |= {"battery_level": float(plant_data["measurements"]["battery"])}
        current_plant |= {"last_updated": self.timezone.localize(datetime.fromisoformat(plant_data["sensor"]["received_data_at"]))}

        return current_plant

    @property
    def fyta_id(self) -> str:
        """ID for FYTA object"""
        return self.email

    @property
    def data(self) -> dict:
        """ID for FYTA object"""
        return self.plants

