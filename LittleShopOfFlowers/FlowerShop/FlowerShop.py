__author__ = 'Abbey'

class  FlowerShop(object):
    _bunches = 0
    _vases = 0
    _ranks = []
    _cache = []
    def __init__(self, bunches, vases, ranks):
        self._bunches = bunches
        self._vases = vases
        self._ranks = ranks
        for i in range(0, self._vases + 1):
            temp = []
            for j in range(0, self._bunches + 1):
                temp.append(0)
            self._cache.append(temp)

    _res = 0
    def compute(self):
        for i in range(1, self._vases + 1):
            for j in range(1, min(i, self._bunches) + 1):
                self._cache[i][j] = self._cache[i - 1][j - 1] + self._ranks[j - 1][i - 1]
                if i - 1 >= j:
                    self._cache[i][j] = max(self._cache[i][j], self._cache[i - 1][j])
                if j == self._bunches:
                    self._res = max(self._res, self._cache[i][j])

        print(self._res)


str1 = raw_input()
bunchesAndFlowers = str1.split(" ")
bunches = int(bunchesAndFlowers[0])
vases = int(bunchesAndFlowers[1])
ranks = []
for i in range(0, bunches):
    tempstr = raw_input()
    tempstrlist = tempstr.split(" ")
    tempranks = []
    for rank in tempstrlist:
        tempranks.append(int(rank))
    ranks.append(tempranks)

# bunches = 3
# vases = 5
# ranks = [[7, 23, -5, -24, 16], [5, 21, -4, 10, 23], [-21, 5, -4, -20, 20]]

fs = FlowerShop(bunches, vases, ranks)
fs.compute()