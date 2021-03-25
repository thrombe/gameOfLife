from PIL import Image
import json
outfile = ''

#outfile = './outfile.txt'

####OPTIONS#####
filein = './structureImages/coolPattern.png'
widthPix = 46 # GOL width
heightPix = 46 # GOL height
def check(pixel): return pixel[0] > 150 # pixel is a tuple of (RGB) values (each from 0 to 255)(there might also be a alpha value as the 4th value in tuple)
# int('hexvalue', 16) #converts hex to decimal
################

img = Image.open(filein)
image = img.load()
width, height = img.size
#print(img.size)

pixLen = height/heightPix
totalPix = heightPix*widthPix
#output = Image.new(img.mode, img.size) #create blank output image
output = img.copy() # copy image object
out = output.load() # load output image for editing
outlist = []
for j in range(1, heightPix + 1):
    for i in range(1, widthPix+1):
        y, x = int(j*pixLen - pixLen/2) , int(i*pixLen - pixLen/2)
        out[x, y] = (255, 0, 0)
        if check(image[x, y]): outlist.append(f'{i};{j}')
        #if image[x, y][0] > 150: outlist.append(f'{i};{j}') # from the app
        #if image[x, y] == (0, 0, 0): outlist.append(f'{i};{j}') # from wikipedia and stuff
output.save('./structureImages/out.jpg')

def printy(string):
    if outfile:
        with open(outfile, 'w') as i:
            print(string, file = i )
    print(string)


print(len(outlist)) # alive cells in no.

if outfile:
    with open(outfile, 'w') as i:
        json.dump(outlist, i)
#printy(list(output.getdata())) # print image rgb

################### append to the file

#in_file = './outfile.txt'

structure_file = './structures.txt'
#with open(in_file, 'r') as i:
#    structure_new = json.load(i)
structure_new = outlist
with open(structure_file, 'r') as i:
    structures = json.load(i)
print(structure_new)

structures[input('enter structure name: ')] = structure_new

with open(structure_file, 'w') as i:
    json.dump(structures, i)
