class cachetest:
    l = []
    def __iter__(self):
        return self.l.__iter__()

    def add(self,item):
        self.l.append(item)

c = cachetest()
c.add(1)
c.add(2)
c.add(3)
c.add(4)
print(1 in c)