
# Created By: Josh Mlaker
# 
# Description: Used for storing an index for universal purposes
# Dependencies: None


index = 0
VIDindex = 0

# Updates an index with a new value
def updateIndex(newIndex, type):
    with open(__file__, "r") as f:
        lines = f.read().split('\n')
        new_line = f'{type} = {newIndex}'
        # While this line is not used, it is important
        new_file = '\n'.join([lines[0]] + [new_line] + lines[2:])

    with open(__file__, "w") as f:
        f.write('\n'.join([lines[0]] + [new_line] + lines[2:]))
