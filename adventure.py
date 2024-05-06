import json
import sys

# Check if the filename is provided as an argument
if len(sys.argv)!= 2:
    print("Usage: python adventure.py <map_filename>")
    sys.exit(1)

map_filename = sys.argv[1]

# Load the map data from the JSON
with open(map_filename) as f:   # Opens the file containing map data
    json_str = f.read()       # Reads the content of the file

# Parse the JSON data as a dictionary
map_data = json.loads(json_str)   # Converting JSON string to a Python dictionary

# Define the player's starting location and inventory
player_location = "start"
player_inventory = []

# Helper function to look up a room by name
def get_room(room_name):
    for room in map_data["rooms"]:
        if room["name"] == room_name:
            return room
    return None

# Helper function to print environment description
def print_room(room):
    print("> " + room["name"])
    print(room["desc"])
    if room.get("exits") and len(room["exits"]) > 0:
        print("Exits: " + ", ".join(room["exits"].keys()))
    if room.get("items") and len(room["items"]) > 0:
        print("Items: " + ", ".join(room["items"]))

# Helper function to print the list of valid verbs
def print_valid_verbs():
    valid_verbs = ["go", "get", "drop", "drop_all", "look", "inventory", "quit", "help"]
    print("You can run the following commands:")
    for verb in valid_verbs:
        if verb == "get":
            print(" get <item>")
        elif verb == "drop":
            print(" drop <item>")
        elif verb == "go":
            print(" go <direction>")
        else:
            print(" " + verb)

# Helper function for Abbreviations
def get_verb(verb_abbrev):
    verb_dict = {
        'g': 'go',
        'ge': 'get',
        'dr': 'drop',
        'i': 'inventory',
        'h': 'help',
        'q': 'quit'
    }
    return verb_dict.get(verb_abbrev, verb_abbrev)

# Helper function to handle direction abbreviations
def get_direction(direction_abbrev, exits):
    for full_dir, _ in exits.items():
        if full_dir.startswith(direction_abbrev):
            return full_dir
    return None

# Helper function to handle item abbreviations
def get_item(item_abbrev, items):
    for item in items:
        if item.startswith(item_abbrev):
            return item
    return None

# Initialize current_room outside of the loop
current_room = get_room(player_location)

# Game loop
while True:
    # Read player input and split it into words
    command = input("What would you like to do? ").strip().lower().split()

    # Handle empty input
    if not command:
        continue

    # Parse the verb and any additional arguments
    verb_abbrev = command[0]
    verb = get_verb(verb_abbrev)
    args = command[1:]

    # Handle the "go" verb
    if verb == "go":
        direction_abbrev = " ".join(args)
        direction = get_direction(direction_abbrev, current_room["exits"])
        if direction:
            next_room_name = current_room["exits"][direction]
            next_room = get_room(next_room_name)

            # Check if the room requires an item and if the player has it
            required_item = next_room.get("required_item")
            restricted_item = next_room.get("restricted_item")
            if required_item and required_item not in player_inventory:
                print("You need the " + required_item + " to go there.")
            elif restricted_item and restricted_item in player_inventory:
                print("You can't go that way with the " + restricted_item + ".")
            else:
                player_location = next_room_name
                current_room = next_room
                print("> " + current_room["name"])
                print(current_room["desc"])
                if current_room.get("exits") and len(current_room["exits"]) > 0:
                    print("Exits: " + ", ".join(current_room["exits"].keys()))
                if current_room.get("items") and len(current_room["items"]) > 0:
                    print("Items: " + ", ".join(current_room["items"]))
        else:
            print("You can't go that way.")

    # Handle the "get" verb
    elif verb == "get":
        item_abbrev = " ".join(args)
        item = get_item(item_abbrev, current_room["items"])
        if item:
            player_inventory.append(item)
            current_room["items"].remove(item)
            print("You got the " + item + ".")
        else:
            print("You don't see that item here.")

    # Handle the "drop" verb
    elif verb == "drop":
        item_abbrev = " ".join(args)
        item = get_item(item_abbrev, player_inventory)
        if item:
            player_inventory.remove(item)
            current_room["items"].append(item)
            print("You dropped the " + item + ".")
        else:
            print("You don't have that item.")

    # Handle the "drop_all" verb
    elif verb == "drop_all":
        player_inventory.clear()
        current_room["items"].extend(["all of your items"])
        print("You dropped all your items.")

    # Handle the "look" verb
    elif verb == "look":
        print_room(current_room)

    # Handle the "inventory" verb
    elif verb == "inventory":
        if player_inventory:
            print("You are carrying: " + ", ".join(player_inventory))
        else:
            print("You are not carrying anything.")

    # Handle the "help" verb
    elif verb == "help":
        print_valid_verbs()

    # Handle the "quit" verb
    elif verb == "quit":
        print("Goodbye!")
        break

    # Handle invalid verbs
    else:
        print("Sorry, I didn't understand that command.")


