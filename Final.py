# Erick Jimenez
# PSID: 1463639
# Final

# Will this work? Find out next time on Dragon Ball Z.

import csv
import datetime

DAMAGED_INVENTORY_CSV = 'DamagedInventory.csv'
PAST_SERVICE_DATE_INVENTORY_CSV = 'PastServiceDateInventory.csv'
INVENTORY_CSV = 'Inventory.csv'
FULL_INVENTORY_CSV = 'FullInventory.csv'
DATES_LIST_CSV = 'ServiceDatesList.csv'
PRICE_LIST_CSV = 'PriceList.csv'
MANUFACTURER_LIST_CSV = 'ManufacturerList.csv'


class Item:
    def __init__(self, id=' ', manufacturer=' ', type=' ', price=-1, service_date=' ', damaged=' '):
        self.id = id
        self.manufacturer = manufacturer
        self.type = type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged


class Inventory:
    def __init__(self):
        self.inventory_container = self.read_files()

    def read_files(self):
        inventory_list = []
        self.read_manufacturer_csv(inventory_list)

        data = {}
        self.read_price_list_csv(data)

        sdl_dict = {}
        self.read_service_dates_csv(sdl_dict)

        self.populate_data(data, inventory_list, sdl_dict)
        inventory_list.sort(key=lambda x: x.manufacturer)

        return inventory_list

    def populate_data(self, data, inventory_list, sdl_dict):
        for inventory in inventory_list:
            inventory.price = data[inventory.id]
            inventory.service_date = sdl_dict[inventory.id]

    def read_service_dates_csv(self, sdl_dict):
        with open(DATES_LIST_CSV, 'r') as file:
            service_date_reader = csv.reader(file, delimiter=',')
            for row in service_date_reader:
                sdl_dict[row[0]] = row[1]

    def read_price_list_csv(self, data):
        with open(PRICE_LIST_CSV, 'r') as file:
            price_reader = csv.reader(file, delimiter=',')
            for row in price_reader:
                data[row[0]] = row[1]

    def read_manufacturer_csv(self, inventory_list):
        with open(MANUFACTURER_LIST_CSV, 'r') as file:
            item_reader = csv.reader(file, delimiter=',')
            for row in item_reader:
                inventory_list.append(Item(id=row[0].strip(), manufacturer=row[1].strip(),
                                           type=row[2].strip(), damaged=row[3].strip()))

    def write_full_inventory(self):  #
        with open(FULL_INVENTORY_CSV, 'w') as file:
            for inventory in self.inventory_container:
                file.write(
                    '{},{},{},{},{},{}\n'.format(inventory.id, inventory.manufacturer, inventory.type,
                                                 inventory.price, inventory.service_date, inventory.damaged))

    def get_item_types(self):
        types = []
        for i in self.inventory_container:
            types.append(i.type)
        types = list(dict.fromkeys(types))
        return types

    def get_item_manufacturer(self):
        manufacturer = []
        for i in self.inventory_container:
            manufacturer.append(i.manufacturer)
        manufacturer = list(dict.fromkeys(manufacturer))
        return manufacturer

    def write_type_inventory(self):
        types = self.get_item_types()
        for ty in types:
            with open(ty + INVENTORY_CSV, 'w') as ti_file:
                for inv in self.inventory_container:
                    if inv.type == ty:
                        ti_file.write(
                            '{},{},{},{},{}\n'.format(inv.id, inv.manufacturer, inv.price, inv.service_date,
                                                      inv.damaged))

    def write_past_service_date_inventory(self):
        today = datetime.date.today()
        with open(PAST_SERVICE_DATE_INVENTORY_CSV, 'w') as psdi_file:
            for inv in self.inventory_container:
                my_list = inv.service_date.split('/')
                inv_date = datetime.date(int(my_list[2]), int(my_list[0]), int(my_list[1]))
                if today > inv_date:
                    psdi_file.write('{},{},{},{},{}\n'.format(inv.id, inv.manufacturer, inv.type, inv.price,
                                                              inv.service_date, inv.damaged))

    def write_damaged_inventory(self):  # function for write DamagedInventory.csv file
        self.inventory_container.sort(key=lambda x: x.price, reverse=True)
        with open(DAMAGED_INVENTORY_CSV, 'w') as di_file:
            for inv in self.inventory_container:
                if inv.damaged == 'damaged':
                    di_file.write('{},{},{},{},{}\n'.format(inv.id, inv.manufacturer, inv.type, inv.price,
                                                            inv.service_date))

    def find_highest_price(self):
        maximum = -1
        max_object = Item()
        for inv in self.inventory_container:
            if int(inv.price) > maximum:
                maximum = int(inv.price)
                max_object = inv
        return max_object

    def find_item_from_inventory(self, user_input):
        type_list = self.get_item_types(self.inventory_container)
        manufacturer_list = self.get_item_manufacturer(self.inventory_container)
        user_str = user_input.split(' ')

        type_counter, count = 0, 0
        user_type, user_manufacturer = '', ''
        is_manufacturer_available = False
        user_object_list = []
        user_type_list = []
        today = datetime.date.today()
        for inv in self.inventory_container:
            my_list = inv.service_date.split('/')
            inv_date = datetime.date(int(my_list[2]), int(my_list[0]), int(my_list[1]))
            if today > inv_date:
                self.inventory_container.remove(inv)
        for inv in self.inventory_container:
            if inv.damaged == 'damaged':
                self.inventory_container.remove(inv)

        for s in user_str:
            for types in type_list:
                if s == types:
                    type_counter += 1
                    user_type = types
            for manufacturer in manufacturer_list:
                if s == manufacturer:
                    count += 1
                    user_manufacturer = manufacturer

        for inv in self.inventory_container:
            if inv.manufacturer == user_manufacturer and inv.type == user_type:
                user_object_list.append(inv)
                is_manufacturer_available = True

        self.find_item(count, is_manufacturer_available, type_counter, user_object_list, user_type, user_type_list)

    def find_item(self, count, is_manufacturer_available, type_counter, user_object_list, user_type, user_type_list):
        if type_counter == 1 and count == 1 and is_manufacturer_available:
            max = self.find_highest_price(user_object_list)
            print(
                'Your item is:{} {} {} {}'.format(max.id, max.manufacturer, max.type,
                                                  max.price))
            self.find_similar_item(max.type, self.inventory_container, int(max.price))
        elif type_counter == 1:
            for inv in self.inventory_container:
                if inv.type == user_type:
                    user_type_list.append(inv)
            max = self.find_highest_price(user_type_list)
            print(
                'Your item is:{} {} {} {}'.format(max.id, max.manufacturer, max.type,
                                                  max.price))
            self.find_similar_item(user_type, self.inventory_container)
        else:
            print('No such item in inventory')

    def find_similar_item(self, user_type, inv_list, price=-1):
        types = []
        data = Item()
        for inv in inv_list:
            if inv.item_type == user_type:
                types.append(inv)
        if price == -1:
            data = self.find_highest_price(types)
            print('You may, also, consider: {} {} {} {}'.format(data.id,
                                                                data.manufacturer,
                                                                data.type, data.price))
        else:
            types.sort(key=lambda x: x.price, reverse=True)
            index = 0
            for types in types:
                if types.price == price:
                    index = types.index(types)
            data = types[index - 1]
            print('You may, also, consider: {} {} {} {}'.format(data.item_ID,
                                                                data.manufacturer,
                                                                data.item_type, data.price))


def find_in_inventory(inventory, data):
    inventory.find_item_from_inv(data)
    data = input('\nPlease enter a item type and manufacturer: ')
    return data


def init_inventory():
    inventory = Inventory()
    inventory.read_files()
    inventory.write_full_inventory()
    inventory.write_type_inventory()
    inventory.write_past_service_date_inventory()
    inventory.write_damaged_inventory()
    return inventory


def process(inventory):
    print('****************          Inventory Management System         **********************')
    user_input = input('Please enter item type and manufacturer> : ')
    while user_input != 'q' or user_input != 'Q':
        user_input = find_in_inventory(inventory, user_input)


def execute():
    inventory = init_inventory()
    process(inventory)


if __name__ == '__main__':
    execute()


