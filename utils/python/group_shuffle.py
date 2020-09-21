import sys
import random


FILE_MODE = False
TO_SHUFFLE_FILE_LOCATION = ""


def read_names_from_file():
    """
    if you want to specify sub group size the first line must be a parsable integer
    """
    with open(TO_SHUFFLE_FILE_LOCATION) as input_file:
        group_info = [info.strip() for info in input_file.readlines()]
        try:
            sub_group_size = int(group_info.pop(0))
        except ValueError:  # group size omitted
            sub_group_size = 0
    if sub_group_size >= len(group_info):
        print("Sub-group size must be an integer and smaller than group")
        sys.exit(-2)
    return sub_group_size, group_info


def read_names_from_cli():
    try:
        sub_group_size = int(input(
            "Sub-group size; if left empty will just shuffle the names:\n"))
    except ValueError:
        print("Sub-group size must be an integer and smaller than group")
        sys.exit(-2)

    group_names = []
    print("Group member names (enter q to quit):\n")
    while (name := input()) != "q":
        group_names.append(name)
    
    return sub_group_size, group_names


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "f":
            FILE_MODE = True
            TO_SHUFFLE_FILE_LOCATION = sys.argv[2]
        else:
            print(
                f"Couldn't parse cli args! {sys.argv[1]} is unknown. Specify files with 'f'")
            sys.exit(-1)

    if FILE_MODE:
        SUB_GROUP_SIZE, NAMES_TO_SHUFFLE = read_names_from_file()
    else:  # interactive mode -> read names from cli
        SUB_GROUP_SIZE, NAMES_TO_SHUFFLE = read_names_from_cli()

    random.shuffle(NAMES_TO_SHUFFLE)

    shuffled_groups = []

    for i in range(int(len(NAMES_TO_SHUFFLE) / SUB_GROUP_SIZE)):
        sub_group = []
        for j in range(SUB_GROUP_SIZE):
            sub_group.append(NAMES_TO_SHUFFLE.pop(random.randint(0, len(NAMES_TO_SHUFFLE) - 1)))
        shuffled_groups.append(sub_group)

    print("Shuffled groups:\n", shuffled_groups)