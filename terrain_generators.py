import random, struct
#Ugly code. Made just for quick development.
class FlatlandTerrainGenerator:
    def __init__(self):
        self.y = [0]*256
        for y in xrange(256):
            self.y[y] = self.generate_y(y)
    def generate_y(self,y):
        x = [0]*16
        for i in xrange(16):
            z = [0]*16
            for i2 in xrange(16):
                if y<60:
                    z[i2] = random.choice([1,1,1,1,13,13,16])
                elif y<65:
                    z[i2] = random.choice([1,1,1,13])
                elif y<70:
                    z[i2] = random.choice([3,3,3,3,13])
                elif y<71:
                    z[i2] = random.choice([2 for _ in xrange(25)]+[12])
                else:
                    z[i2] = 0
            x[i] = z
        return x
    
    def generate_data(self):
        data=''
        for y in xrange(256):
            for x in range(16):
                for z in range(16):
                    data += struct.pack('B', self.y[y][x][z])
        return data