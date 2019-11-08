from keyword_extractor.UDPipeProcess import UDPipeProcess
from keyword_extractor.utilities import UDPipeKeywordsExtractor

class UDPipeKeywordsExtractorProcess():
    def __init__(self, model_file):
        #model_file - path to file
        self.udpipe_service = UDPipeProcess(model_file)

    def process_task(self, documents):
        kwe = UDPipeKeywordsExtractor()

        # ==============================================================================================================
        # Listify if necessary:
        if isinstance(documents, str):
            is_str = True
            documents = [documents]
        else:
            is_str = False

        # ==============================================================================================================
        # Check is such the language presented:
        # if language not in self.__language_configs:
        #     raise ApplicationException(code=ResponseCode.INTERNAL_SERVER_ERROR,
        #                                message=f'Unsupported language: {language}')

        # ==============================================================================================================
        # Get services:
        # services = self.__language_configs[language]
        # udpipe_service = services.get('udpipe_service', None)

        # ==============================================================================================================
        # Perform UDPipe parsing:
        # if udpipe_service is None:
        #     raise ApplicationException(code=ResponseCode.INTERNAL_SERVER_ERROR,
        #                                message=f'UDPipe service was not configured for this language: {language}')
        # else:
        result = kwe.transform(self.udpipe_service.process_task(documents=documents))

        # ==============================================================================================================
        # Un-list if necessary
        if is_str: result = result[0]

        return result



