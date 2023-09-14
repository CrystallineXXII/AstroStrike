class Counter:
    def __init__(self, startValue,*,loopOver=False, maxValue=0):
        self.value = startValue
        self.loopOver = loopOver
        self.maxValue = maxValue

    def tick(self, deltaTime):
        self.value += deltaTime

        if self.value > self.maxValue and not self.loopOver:
            self.value = self.maxValue
            return True
        elif self.value > self.maxValue and self.loopOver:
            self.value = 0
            return True
        return False

    def reset(self):
        self.value = 0
