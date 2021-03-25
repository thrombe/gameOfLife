from PIL import Image
import json
outfile = ''

outfile = './outfile.txt'

filein = './coolPattern.png'
width = 1020 # image width
height = 1020 #image height
widthPix = 46 # GOL width
heightPix = 46 # GOL height


img = Image.open(filein)
image = img.load()

pixLen = height/heightPix
totalPix = heightPix*widthPix
#output = Image.new(img.mode, img.size) #create blank output image
output = img.copy() # copy image object
out = output.load() # load output image for editing
outlist = []
for j in range(1, heightPix + 1):
    for i in range(1, widthPix+1):
        y, x = int(j*pixLen - pixLen*3/2) , int(i*pixLen - pixLen*3/2)
        out[x, y] = (255, 0, 0)
        if image[x, y][0] > 150: outlist.append(f'{i};{j}') # from the app
        #if image[x, y] == (0, 0, 0): outlist.append(f'{i};{j}') # from wikipedia and stuff
output.save('out.jpg')

def printy(string):
    if outfile:
        with open(outfile, 'w') as i:
            print(string, file = i )
    print(string)


print(len(outlist)) # alive cells in no.
with open(outfile, 'w') as i:
    json.dump(outlist, i)
#printy(list(output.getdata())) # print image rgb