import serial

s = serial.Serial("/dev/ttyUSB0",38400, timeout = 1)

def data_cap():
    l = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    #vehicle speed
    data = communicate('010D')
    d = data[6:8]
    d = d.decode('ascii')
    r = int(d, 16)
    print('vehicle speed:',r)
    l[0] = r
    print('---------')

    #water temperature
    data = communicate('0105')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = d10 - 40
    print('water temp:',r)
    l[1] = r 
    print('---------')

    #control module voltage?
    data = communicate('0142')
    d = data[6:11]
    d = d[0:2] + d[3:5]
    d = d.decode('ascii')
    print(d)
    d10 = int(d, 16)
    r = d10 / 1000
    print('voltage',r)
    l[2] = r
    print('---------')

    #odometer?
    data = communicate('0131')
    d = data[6:11]
    d = d[0:2] + d[3:5]
    d = d.decode('ascii')
    print(d)
    r = int(d, 16)
    print('distance traveled since codes cleared',r)
    l[3] = r
    print('---------')

    #engine speed
    data = communicate('010C')
    d = data[6:11]
    d = d[0:2] + d[3:5]
    d = d.decode('ascii')
    print(d)
    d10 = int(d, 16)
    r = d10/4
    print('engine speed:',r)
    l[4] = r
    print('---------')

    #calculated engine load value
    data = communicate('0104')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = d10 * 100 / 255
    print('engine load:',r)
    l[5] = r
    print('---------')

    #Intake manifold absolute pressure
    data = communicate('010B')
    d = data[6:8]
    d = d.decode('ascii')
    r = int(d, 16)
    print('intake manifold absolute pressure:',r)
    l[6] = r
    print('---------')

    #timing advance
    data = communicate('010E')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = (d10 - 128) / 2
    print('timing advance:',r)
    l[7] = r
    print('---------')

    #intake air temperature
    data = communicate('010F')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = d10 - 40
    print('intake air temp:',r)
    l[8] = r
    print('---------')

    #mass air flow rate
    data = communicate('0110')
    d = data[6:11]
    d = d[0:2] + d[3:5]
    d = d.decode('ascii')
    print(d)
    d10 = int(d, 16)
    r = d10 / 100
    print('MAF air flow rate:',r)
    l[9] = r
    print('---------')

    #throttle position
    data = communicate('0111')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = d10 * 100 / 255
    print('throttle position:',r)
    l[10] = r
    print('---------')

    #run time since engine start
    data = communicate('011F')
    d = data[6:11]
    d = d[0:2] + d[3:5]
    d = d.decode('ascii')
    print(d)
    r = int(d, 16)
    print('run time',r)
    l[11] = r
    print('---------')

    #fuel level input
    data = communicate('012F')
    d = data[6:8]
    d = d.decode('ascii')
    d10 = int(d, 16)
    r = d10 * 100 / 255
    print('fuel level input',r)
    l[12] = r


def communicate(comm):
    #print (s.name)
    command = comm
    s.write(command.encode('ascii')+b'\r')
    data = s.readline()
    print(data)
    return data


def con_establish():
    print (s.name)
    command = 'ati'
    s.write(command.encode('ascii','ignore')+b'\r')
    data = s.readline()
    #d = data.decode('ascii','ignore')
    if d == b'ELM327 v1.5\r\r>':
        command = '0100'
        s.write(command.encode('ascii','ignore')+b'\r')
        data = s.readline()
        #d = data.decode('ascii')
        d1 = data[:5]
        print(d1)
        if d1 == b'41 00':
            print('connection ready!')

if __name__ == "__main__":
    #while True:
     #   comm = input('please type the command:')
      #  communicate(comm)
    data_cap()