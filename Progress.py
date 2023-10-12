class Progress:
    def __init__(self, total, 
                    label: str = 'progress:',
                    unit: str = 't', 
                    step: int = 1, 
                    precision: int = 2, 
                    bar_length: int = 10, 
                    style: str = '=',
                    width_rate: int = 1,
                    flag: str = 's'
                    ):
        import time
        self.__total = total
        self.__end = len(self.__total)
        self.__yet = -1
        self.label = label
        self.unit = unit
        self.log_step = step
        self.precision = precision
        self.bar_length = bar_length
        self.style = style
        self.width_rate = width_rate
        self.last_time = None
        self.flag = flag  # 'o' or 's'
        
    @property
    def progress(self):
        return round(self.__totalPrecision, self.precision)
    
    @property
    def __totalPrecision(self):
        return self.__yet / self.__end
    
    def __calculateTime(self):
        if self.last_time is not None:
            delta_time = time.perf_counter() - self.last_time
            self.last_time = time.perf_counter()
            return delta_time ** (1 if self.flag == 'o' else -1)
        self.last_time = time.perf_counter()
        return 0.01
        
    def step(self, flag):
        rating = '{:4>.3f}%s/s'%self.unit if flag == 's' else '{:4>.3f}s/%s'%self.unit
        self.__yet += 1
        shape_length = self.bar_length
        progress = self.progress * self.bar_length
        bar = self.style * int(progress)
        
        def logConsole():
            print((('\r%s {:0>5.1f}%s[{: <%d}] ' + rating)
                        % (self.label, '%', shape_length * self.width_rate)
                            ).format(
                                self.progress * 100,
                                bar,
                                self.__calculateTime()
                            ), 
                end = '' if self.__totalPrecision != 1 else '\n'
                )
        if self.__yet % self.log_step == 0:
            logConsole()
        
    def __iter__(self):
        self.__iterObject = tuple(self.__total)
        self.__index = -1
        return self
    
    def __next__(self):
        self.step(self.flag)
        if self.__index >= self.__end - 1:
            raise StopIteration()
        self.__index += 1
        
        return self.__iterObject[self.__index]
    
    
import time
def run_test():
    st = time.perf_counter()
    for i in Progress(range(1000), flag = 'o'):  # flag default is o
        time.sleep(0.00001 * i + 0.005)
    print('progress for:', time.perf_counter() - st)
    
    st = time.perf_counter()
    for i in range(1000):
        time.sleep(0.00001 * i + 0.005)
    print('normal for:', time.perf_counter() - st)
    
    
    for i in Progress(range(1000), flag = 's'):
        time.sleep(-0.00005 * i + 0.05)
        

def fibo3(n):
    i, j = 1, 1
    for _ in Progress(range(n // 2)):
        i += j
        j += i
    return j if n % 2 == 0 else i

fibo3(1000000)
print('end')