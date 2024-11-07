import json

GUILD = 910728368641679400

dat = {}
with open('luke/udata.json') as json_file:
    dat = json.load(json_file)
print(dat)

gdat = {}
with open('luke/gdata.json') as json_file:
    gdat = json.load(json_file)
print(gdat)

reminders = {}
with open('luke/rdata.json') as json_file:
    reminders = json.load(json_file)
print(reminders)

tunnels = {}#cast and subscribe commands are currently not supposed to be used
with open('luke/sdata.json') as json_file:
    tunnels = json.load(json_file)
print(tunnels)

def searchByAttr(l, a, v):
    for x in l:
        if x[a] == v:
            return x
    return None

def save_state():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/udata.json", "w")
    json.dump(dat, out, indent = 2)
def checkuser(user):
    if not str(user.id) in dat:
        dat[str(user.id)] = {}

def save_gstate():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/gdata.json", "w")
    json.dump(gdat, out, indent = 2)

def save_reminders():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/rdata.json", "w")
    json.dump(reminders, out, indent = 2)
def save_tunnels():
    '''f = open('MStat.txt', 'w')
    for x in currencies:
        f.write(x+" "+str(currencies[x])+" "+str(dailyclaims[x])+"\n")
    f.close()'''
    out = open("luke/sdata.json", "w")#s stands for subscriptions
    json.dump(tunnels, out, indent = 2)