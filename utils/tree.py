class TreeNode(object):

    def __init__(self, value=None, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    class TreeIter(object):

        def __init__(self, target):
            self.target = target

        def __bool__(self):
            return self.target is not None

        def __call__(self):
            return self.target.value
    
        def go_left(self):
            if self.target is None:
                return
            if self.target.left:
                self.target = self.target.left
                while self.target.right:
                    self.target = self.target.right
            else:
                while self.target.parent and self.target.parent.left == self.target:
                    self.target = self.target.parent
                self.target = self.target.parent

        def go_left_until(self, filter):
            self.go_left()
            while self.target and not filter(self()):
                self.go_left()

        def go_right(self):
            if self.target is None:
                return
            if self.target.right:
                self.target = self.target.right
                while self.target.left:
                    self.target = self.target.left
            else:
                while self.target.parent and self.target.parent.right == self.target:
                    self.target = self.target.parent
                self.target = self.target.parent

        def go_right_until(self, filter):
            self.go_right()
            while self.target and not filter(self()):
                self.go_right()

    def get_iter(self):
        return TreeNode.TreeIter(self)
    
    def get_left_iter(self):
        target = self
        while target.left:
            target = target.left
        return TreeNode.TreeIter(target)
    
    def get_right_iter(self):
        target = self
        while target.right:
            target = target.right
        return TreeNode.TreeIter(target)


def printTree(root, filter=lambda v: True):
    tree_iter = root.get_left_iter()
    while tree_iter:
        if filter(tree_iter()):
            print(tree_iter())
        tree_iter.go_right()
