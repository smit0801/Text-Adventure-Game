
import json
import sys

class Game:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room_id = 0
        self.inventory = []

    def load_map(self, map_filename):
        with open(map_filename, 'r') as file:
            self.map_data = json.load(file)
            self.validate_map()

    def validate_map(self):
        if not isinstance(self.map_data, list):
            raise ValueError("Invalid map format. Map should be a list of room objects.")

        for room_id, room in enumerate(self.map_data):
            if not all(field in room for field in ['name', 'desc', 'exits']):
                raise ValueError(f"Invalid room format for room {room_id}. Missing required fields.")

            if not isinstance(room['exits'], dict):
                raise ValueError(f"Invalid exits format for room {room_id}. Exits should be a dictionary.")

            for exit_direction, exit_room_id in room['exits'].items():
                if not isinstance(exit_room_id, int) or exit_room_id < 0 or exit_room_id >= len(self.map_data):
                    raise ValueError(f"Invalid room ID '{exit_room_id}' in exit '{exit_direction}' for room {room_id}.")

    def display_room(self):
        room = self.map_data[self.current_room_id]
        
        print(f"> {room['name']}\n\n{room['desc']}\n")
        
        if 'items' in room and room['items']:
            items = ', '.join(room['items'])
            print(f"Items: {items}\n")
        
        exits = ', '.join(room['exits'])
        print(f"Exits: {exits}\n")

    def process_go(self, direction):
        room = self.map_data[self.current_room_id]
        valid_directions = room['exits'].keys()

        if not direction:
            print("Sorry, you need to 'go' somewhere.")
            return

        if direction in valid_directions:
            self.current_room_id = room['exits'][direction]
            print(f"You go {direction}.\n")
            
            self.display_room()
        else:
            print(f"There's no way to go {direction}.")

    def process_look(self):
        self.display_room()

    
    def process_get(self, item):
        room = self.map_data[self.current_room_id]

        if not item:
            print("Sorry, you need to 'get' something.")
            return

        matching_items = [map_item for map_item in room.get('items', []) if map_item.startswith(item)]
        if len(matching_items) == 1:
            self.inventory.append(matching_items[0])
            room['items'].remove(matching_items[0])
            print(f"You pick up the {matching_items[0]}.")
        elif len(matching_items) > 1:
            print(f"Did you want to get {', '.join(matching_items)}?")
        else:
            print(f"There's no {item} anywhere.")


    def process_drop(self, item):
        if item in self.inventory:
            room = self.map_data[self.current_room_id]
            self.inventory.remove(item)
            room.setdefault('items', []).append(item)
            print(f"You drop the {item}.")
        else:
            print(f"You don't have {item} in your inventory.")

    def process_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def process_quit(self):
        print("Goodbye!")
        sys.exit()

    def process_help(self):
        print("You can run the following commands:")
        command_formats = {
            'go': "go ...",
            'get': "get ...",
            
        }
        for method_name in dir(self):
            if method_name.startswith("process_"):
                command = method_name[len("process_"):].lower()
                format_str = command_formats.get(command, command)
                print(f"  {format_str}")

    def play(self):
        self.display_room()
        while True:
            user_input = input("What would you like to do? ").strip().lower()
            if user_input.startswith('go'):
                direction = user_input[3:]
                self.process_go(direction)
            elif user_input in self.map_data[self.current_room_id]['exits']:
                self.process_go(user_input)
            elif user_input == 'look':
                self.process_look()
            elif user_input.startswith('get'):
                item = user_input[4:]
                self.process_get(item)
            elif user_input.startswith('drop '):
                item = user_input[5:]
                self.process_drop(item)
            elif user_input == 'inventory':
                self.process_inventory()
            elif user_input == 'quit':
                self.process_quit()
            elif user_input == 'help':
                self.process_help()
            else:
                print("Use 'quit' to exit.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
    else:
        game = Game(sys.argv[1])
        game.play()
