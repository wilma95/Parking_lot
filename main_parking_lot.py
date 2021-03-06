#parking_lot.py
import heapq
from collections import defaultdict, OrderedDict


class Car:
    def __init__(self, registration_number, color):
        self.registration_number = registration_number
        self.color = color

    def __str__(self):
        return "Car [registration_number=" + self.registration_number + ", color=" + self.color + "]"


class ParkingLot:
    def __init__(self):
        self.registration_slot_mapping = dict()
        self.color_registration_mapping = defaultdict(list)
        # we need to maintain the orders of cars while showing 'status'
        self.slot_car_mapping = OrderedDict()
        # initialize all slots as free
        self.available_parking_lots = []

    def create_parking_lot(self, total_slots):
        # Using min heap as this will always give minimum slot number in O(1) time
        print("Created a parking lot with {} slots".format(total_slots))
        for i in range(1, total_slots + 1):
            heapq.heappush(self.available_parking_lots, i)
        return True

    def status(self):
        print("Slot No.  Registration No  Colour")
        for slot, car in self.slot_car_mapping.items():
            print("{}         {}    {}".format(slot, car.registration_number, car.color))
        return True

    def get_nearest_slot(self):
        return heapq.heappop(self.available_parking_lots) if self.available_parking_lots else None

    def leave(self, slot_to_be_freed):
        found = None
        for registration_no, slot in self.registration_slot_mapping.items():
            if slot == slot_to_be_freed:
                found = registration_no

        # Cleanup from all cache
        if found:
            heapq.heappush(self.available_parking_lots, slot_to_be_freed)
            del self.registration_slot_mapping[found]
            car_to_leave = self.slot_car_mapping[slot_to_be_freed]
            self.color_registration_mapping[car_to_leave.color].remove(found)
            del self.slot_car_mapping[slot_to_be_freed]
            print("Slot number {} is free".format(slot_to_be_freed))
            return True

        else:
            print("slot is not in use")
            return False

    def park(self, car):
        slot_no = self.get_nearest_slot()
        if slot_no is None:
            print("Sorry, parking lot is full")
            return
        print("Allocated slot number: {}".format(slot_no))
        self.slot_car_mapping[slot_no] = car
        self.registration_slot_mapping[car.registration_number] = slot_no
        self.color_registration_mapping[car.color].append(car.registration_number)
        return slot_no

    # Registration numbers of all cars of a particular colour
    def registration_numbers_for_cars_with_colour(self, color):
        registration_numbers = self.color_registration_mapping[color]
        print(", ".join(registration_numbers))
        return self.color_registration_mapping[color]

    # Slot numbers of all slots where a car of a particular colour is parked
    def slot_numbers_for_cars_with_colour(self, color):
        registration_numbers = self.color_registration_mapping[color]
        slots = [self.registration_slot_mapping[reg_no] for reg_no in registration_numbers]
        print(", ".join(map(str, slots)))
        return slots

    def slot_number_for_registration_number(self, registration_number):
        slot_number = None
        if registration_number in self.registration_slot_mapping:
            slot_number = self.registration_slot_mapping[registration_number]
            print(slot_number)
            return slot_number
        else:
            print("Not found")
            return slot_number