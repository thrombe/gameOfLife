import json
in_file = './outfile.txt'
structure_file = './structures.txt'
with open(in_file, 'r') as i:
    structure_new = json.load(i)
with open(structure_file, 'r') as i:
    structures = json.load(i)
print(structure_new)

structures[input('enter structure name: ')] = structure_new

with open(structure_file, 'w') as i:
    json.dump(structures, i)
