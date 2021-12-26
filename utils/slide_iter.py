class SlideIter(object):

    def __init__(self, target, offset=0):
        self.target = target
        self.offset = offset

    def skip(self, length=1):
        self.offset += length

    def get(self, length=1):
        prev_offset = self.offset
        self.offset += length
        return self.target[prev_offset : self.offset]

    def get_to(self, value):
        prev_offset = self.offset
        to_index = self.target.index(value, self.offset)
        self.offset = to_index
        return self.target[prev_offset : self.offset]

    def peek(self, length=1):
        return self.target[self.offset : self.offset + length]

    def peek_from(self, offset, length=1):
        offset += self.offset
        return self.target[offset : offset + length]

    def peek_to(self, value):
        to_index = self.target.index(value, self.offset)
        return self.target[self.offset : to_index]

    def peek_from_to(self, value, offset):
        offset += self.offset
        to_index = self.target.index(value, offset)
        return self.target[offset : to_index]
