

class batches_generator:
    def __init__(self, seq, batch_size = 32, loop = True):
        self.loop = loop
        self.data = seq
        self.batch_size = batch_size
        self.batches = self.data.shape[0]//self.batch_size
        if self.batch_size * self.batches < self.data.shape[0]:
            self.batches += 1
        self.current = 0

    def __next__(self):
        if self.current+1 > self.batches:
            if self.loop:
                self.current = 0
            else:
                raise StopIteration('there is no more batches!')
        curr_data_batch = self.data[self.current*self.batch_size:(self.current+1)*self.batch_size]
        self.current += 1
        return curr_data_batch

    def __len__(self):
        return self.batches