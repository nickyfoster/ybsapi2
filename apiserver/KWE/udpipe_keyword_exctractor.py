from apiserver.KWE import UDPipeKeywordsExtractor

from apiserver.KWE import UDPipeModel


class UDPipeProcess():
    def __init__(self, model_file):
        self.__model_file = model_file
        self.__model_loaded = False

        self.__model = UDPipeModel(path=self.__model_file)

    def process_task(self, documents):
        examples = documents
        result = [self.__model(x) for x in examples]
        return result


class UDPipeKeywordsExtractorProcess():
    def __init__(self, model_file):
        self.udpipe_service = UDPipeProcess(model_file)

    def process_task(self, documents):
        kwe = UDPipeKeywordsExtractor()
        if isinstance(documents, str):
            is_str = True
            documents = [documents]
        else:
            is_str = False

        result = kwe.transform(self.udpipe_service.process_task(documents=documents))
        if is_str: result = result[0]

        return result
