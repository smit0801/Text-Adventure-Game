import json

# Define the player's starting location and inventory
player_location = 0
player_inventory = []

# Load the map data from the JSON 
with open('map_filename') as f:   # Opens the file containng map data
    json_str = f.read()       # Reads the content of  file

# Parse the JSON data as an array
map_data = json.loads(json_str)   # Converting  JSON string to a Python list

# Helper function to look up a room index
def get_room(room_index):
    return map_data[room_index]

# Helper function to print environment discription
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
            next_room_index = current_room["exits"][direction]
            next_room = get_room(next_room_index)

            # Check if the room requires an item and if the player has it
            required_item = next_room.get("required_item")
            restricted_item = next_room.get("restricted_item")
            if required_item and required_item not in player_inventory:
                print("You need the " + required_item + " to unlock next stage.")
            elif restricted_item and restricted_item in player_inventory:
                print("You need to drop " + restricted_item + " to go to next stage.")
            else:
                player_location = next_room_index
                current_room = next_room
                print_room(current_room)

                # Check if the player has reached the last room
                if player_location == len(map_data) - 1:
                    print("Congratulations, you've reached the end of the game!")
                    break

        else:
            print(f"There's no way to go {direction_abbrev}.")

    # Handle the "look" verb
    elif verb == "look":
        print_room(current_room)

    # Handle the "get" verb
    elif verb == "get":
        item_abbrev = " ".join(args)
        item_name = get_item(item_abbrev, current_room.get("items", []))
        if item_name:
            player_inventory.append(item_name)
            current_room["items"].remove(item_name)
            print(f"You get the {item_name}.")
        else:
            print(f"There's no item starting with '{item_abbrev}' here.")

    # Handle the "drop" verb
    elif verb == "drop":
        item_abbrev = " ".join(args)
        item_name = get_item(item_abbrev, player_inventory)
        if item_name:
            player_inventory.remove(item_name)
            current_room["items"].append(item_name)
            print(f"You drop the {item_name}.")
        else:
            print(f"You're not carrying an item starting with '{item_abbrev}'.")

    # Handle the "drop all" verb
    elif verb == "drop_all":
        if len(player_inventory) == 0:
            print("You're not carrying anything to drop.")
        else:
            for item_name in player_inventory:
                current_room["items"].append(item_name)
            player_inventory = []
            print("You drop all of your items.")

    # Handle the "inventory" verb
    elif verb == "inventory":
        if not player_inventory:
            print("You're not carrying anything.")
        else:
            print("You're carrying: " + ", ".join(player_inventory))

    # Handle the "help" verb
    elif verb == "help":
        print_valid_verbs()

    # Handle the "quit" verb
    elif verb == "quit":
        print("Thanks for playing!")
        break

    # Handle unknown verbs
    else:
        print("I don't know how to " + verb + ".")