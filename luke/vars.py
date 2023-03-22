import json

dat = {}
with open('luke/udata.json') as json_file:
    dat = json.load(json_file)
print(dat)

gdat = {}
with open('luke/gdata.json') as json_file:
    gdat = json.load(json_file)
print(gdat)

def save_state():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/udata.json", "w")
    json.dump(dat, out, indent = 2)

def save_gstate():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/gdata.json", "w")
    json.dump(gdat, out, indent = 2)