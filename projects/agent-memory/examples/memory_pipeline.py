"""
Memory Pipeline
Pipeline processing
"""
from memory import Memory


class Pipeline:
    def __init__(self):
        self.stages = []
    
    def add(self, stage):
        self.stages.append(stage)
    
    def process(self, data):
        result = data
        for stage in self.stages:
            result = stage(result)
        return result


def demo():
    pipeline = Pipeline()
    pipeline.add(lambda x: x.upper())
    pipeline.add(lambda x: x + "!")
    print(pipeline.process("hello"))


if __name__ == "__main__":
    demo()
