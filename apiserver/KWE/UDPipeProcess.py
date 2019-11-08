from keyword_extractor.UDPipeModel import UDPipeModel

class UDPipeProcess():
    def __init__(self, model_file):
        self.__model_file = model_file
        self.__model_loaded = False

        self.__model = UDPipeModel(path=self.__model_file)

    def process_task(self, documents):
        examples = documents
        result = [self.__model(x) for x in examples]
        return result