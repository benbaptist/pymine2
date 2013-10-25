import random, struct
#Ugly code. Made just for quick development.
class FlatlandTerrainGenerator:
    def __init__(self):
        self.y = {}
        for y in xrange(256):
            self.y[y] = {}
            for x in xrange(16):
                self.y[y][x] = {}
                for z in xrange(16):
                    self.y[y][x][z] = 0
        for y in xrange(256):
            self.generate_y(y)
    def generate_y(self,y):
        for x in xrange(16):
            for z in xrange(16):
                if y<1:
                    self.y[y][x][z] = 7
                elif y<60:
                    self.y[y][x][z] = random.choice([1,1,1,1,13,13,16])
                elif y<65:
                    self.y[y][x][z] = random.choice([1,1,1,13])
                elif y<70:
                    self.y[y][x][z] = random.choice([3,3,3,3,13])
                elif y<71:
                    self.y[y][x][z] = random.choice([2 for _ in xrange(25)]+[12])
                elif y<72:
                    if random.randint(0,100) == 15 and 17 not in self.get_surrounding_blocks(y, x, z):
                        self.y[y][x][z] = 17
                elif y<73:
                    if self.y[y-1][x][z] == 17:
                        treelogs = random.randint(3,4)
                        for treelog in xrange(treelogs):
                            self.y[y+treelog][x][z] = 17
                        for leaf in xrange(2):
                            try:
                                self.y[y+treelogs][x][z] = 18
                                self.y[y+leaf+treelogs][x][z] = 18
                                self.y[y+treelogs][x-leaf][z] = 18
                                self.y[y+treelogs][x+leaf][z] = 18
                                self.y[y+treelogs][x][z-leaf] = 18
                                self.y[y+treelogs][x][z+leaf] = 18
                            except KeyError:
                                pass
    
    def get_surrounding_blocks(self, y, x, z):
        surrounding_blocks = []
        try:
            surrounding_blocks.append(self.y[y][x+1][z])
            surrounding_blocks.append(self.y[y][x-1][z])
            surrounding_blocks.append(self.y[y][x][z+1])
            surrounding_blocks.append(self.y[y][x][z-1])
            
            surrounding_blocks.append(self.y[y+1][x+1][z])
            surrounding_blocks.append(self.y[y+1][x-1][z])
            surrounding_blocks.append(self.y[y+1][x][z+1])
            surrounding_blocks.append(self.y[y+1][x][z-1])
            
            surrounding_blocks.append(self.y[y-1][x+1][z])
            surrounding_blocks.append(self.y[y-1][x-1][z])
            surrounding_blocks.append(self.y[y-1][x][z+1])
            surrounding_blocks.append(self.y[y-1][x][z-1])
        except TypeError:
            pass
        except KeyError:
            pass
        
        return surrounding_blocks
    
    def generate_data(self):
        data=''
        for y in xrange(256):
            for x in range(16):
                for z in range(16):
                    data += struct.pack('B', self.y[y][x][z])
        return data