import json
import sys

# Helper functions
def load_map(filename):
    with open(filename) as f:
        game_map = json.load(f)
    return game_map

def validate_map(game_map):
    if "start" not in game_map or "rooms" not in game_map:
        return False

    room_names = set()
    for room in game_map["rooms"]:
        if "name" not in room or "desc" not in room or "exits" not in room:
            return False
        if room["name"] in room_names:
            return False
        room_names.add(room["name"])
        for exit_name, exit_room in room["exits"].items():
            if exit_room not in room_names:
                return False

    return True

def print_room(room):
    print(f"> {room['name']}\n")
    print(room["desc"])
    if "items" in room:
        print(f"\nItems: {', '.join(room['items'])}")
    print(f"\nExits: {' '.join(room['exits'].keys())}\n")

def get_exit(exits, direction):
    for exit_name, exit_room in exits.items():
        if direction == exit_name:
            return exit_room
    return None

def get_item(items, item_name):
    for item in items:
        if item_name in item:
            return item
    return None

def remove_item(items, item_name):
    return [item for item in items if item_name not in item]

# Game Logic
def play_game(game_map):
    current_room = game_map["rooms"][game_map["start"]]
    inventory = []

    print_room(current_room)

    while True:
        command = input("What would you like to do? ").strip().lower()

        if command == "quit":
            print("Goodbye!")
            break
        elif command == "look":
            print_room(current_room)
        elif command.startswith("go"):
            direction = command.split()[-1]
            next_room_name = get_exit(current_room["exits"], direction)
            if next_room_name is None:
                print(f"There's no way to go {direction}.")
            else:
                current_room = game_map["rooms"][next_room_name]
                print_room(current_room)
        elif command.startswith("get"):
            item_name = command.split()[-1]
            item = get_item(current_room.get("items", []), item_name)
            if item is None:
                print(f"There's no {item_name} anywhere.")
            else:
                inventory.append(item)
                current_room["items"] = remove_item(current_room["items"], item_name)
                print(f"You pick up the {item}.")
        elif command == "inventory":
            if not inventory:
                print("You're not carrying anything.")
            else:
                print("Inventory:")
                for item in inventory:
                    print(f"  {item}")
        elif command in [exit_name for exit_name in current_room["exits"]]:
            next_room_name = current_room["exits"][command]
            current_room = game_map["rooms"][next_room_name]
            print_room(current_room)
        else:
            print("I don't understand that command.")

# Extensions
def print_help():
    print("You can run the following commands:")
    print("  go ...")
    print("  get ...")
    print("  look")
    print("  inventory")
    print("  quit")
    print("  help")
    print("  drop ...")
    print("  [exit_name]")

def drop_item(inventory, current_room, item_name):
    item = get_item(inventory, item_name)
    if item is None:
        print(f"You don't have a {item_name} to drop.")
    else:
        inventory.remove(item)
        current_room["items"] = current_room.get("items", []) + [item]
        print(f"You drop the {item}.")

# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adventure.py [map_file]")
        sys.exit(1)

    map_file = sys.argv[1]
    game_map = load_map(map_file)

    if not validate_map(game_map):
        print("Error: Invalid map file.", file=sys.stderr)
        sys.exit(1)

    print("Welcome to the Text Adventure Game!")

    while True:
        command = input("What would you like to do? ").strip().lower()

        if command == "help":
            print_help()
        else:
            try:
                play_game(game_map)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


