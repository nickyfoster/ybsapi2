from typing import List
import nltk


class UDPipeKeywordsExtractor:
    """
    Keywords Extractor based on syntax tree processing which is obtained from UDPipe model
    """

    def __init__(self, only_verb_head: bool = True, lemmatize: bool = True, lower: bool = True):
        """
        :param only_verb_head: flag which specifies if only verb heads will be used in keywords construction
        :param lemmatize: flag which specifies if keywords will be lemmatized (adds generalization)
        :param lower: flag which specifies if keywords will be lower-cased (adds generalization)
        """

        super().__init__()
        self.__only_verb_head = only_verb_head
        self.__token_field = 'lemma' if lemmatize else 'form'
        self.__lower = lower

    def transform(self, conlls):
        """
        """

        KEYWORDS = []
        for conll in conlls:
            tree = conll
            keywords = []
            for root in tree:
                UDPipeKeywordsExtractor.prune_tree(root, token_field=self.__token_field)
                keywords += UDPipeKeywordsExtractor.get_keywords(root, only_verb_head=self.__only_verb_head)

            if self.__lower:
                keywords = [x.lower() for x in keywords]
            KEYWORDS.append(keywords)

        return KEYWORDS

    @staticmethod
    def get_keywords(root, only_verb_head) -> List[str]:
        """
        Obtain keywords from root (or head)
        :param root: conll head object
        :param only_verb_head: flag which specifies if only verb heads will be used in keywords construction
        :return: list of keywords
        """
        all_tokens = UDPipeKeywordsExtractor.get_all_tokens([root])
        keywords = []

        for head in all_tokens:
            head_tok = head.token

            if head_tok.get('ignored', False) or (only_verb_head and head_tok['upostag'] != 'VERB'):
                continue

            all_child_ignored = True
            for child in head.children:
                child_tok = child.token
                if child_tok.get('ignored', False):
                    continue

                if child_tok['upostag'] != 'VERB':
                    keyword = ' '.join([x[0] for x in sorted(head_tok['form'] + child_tok['form'], key=lambda x: x[1])])
                    keywords.append(keyword)
                    all_child_ignored = False

            if all_child_ignored and (len(head_tok['form']) >= 3 or len(all_tokens) == 2):
                keyword = ' '.join([x[0] for x in sorted(head_tok['form'], key=lambda x: x[1])])
                keywords.append(keyword)

        return keywords

    @staticmethod
    def prune_tree(root, token_field):
        level = 0
        all_tokens = UDPipeKeywordsExtractor.get_all_tokens([root])

        for t in all_tokens:
            t.token['form'] = [(t.token[token_field], t.token['id'])]

        while True:
            level_tokens = [t for t in all_tokens if UDPipeKeywordsExtractor.get_token_level(t)[0] == level]

            if len(level_tokens) == 0:
                break

            for token in level_tokens:
                head = [t for t in all_tokens if t.token['id'] == token.token['head']]
                if len(head) == 0:
                    continue
                elif len(head) == 1:
                    UDPipeKeywordsExtractor.prune_dep(token, head[0])
                else:
                    raise ValueError('There are more than 1 head for token')

            level += 1

    @staticmethod
    def get_token_level(t, start_level=0):
        children = t.children
        levels = [start_level]
        for c in children:
            levels += UDPipeKeywordsExtractor.get_token_level(c, start_level + 1)

        return [max(levels)]

    @staticmethod
    def prune_dep(token, head):
        t, h = token.token, head.token
        token.token['ignored'] = False

        if UDPipeKeywordsExtractor.check_if_head_modifier(t):
            h['form'] = t['form'] + h['form']
            t['ignored'] = True
        elif UDPipeKeywordsExtractor.check_if_ignored(t):
            t['ignored'] = True

    @staticmethod
    def check_if_head_modifier(token):
        cases = [('advmod', ['PART']), ('case', ['ADP']), ('nmod', ['PRON'])]
        t = (token['deprel'], token['upostag'])

        for case in cases:
            if (case[0] is None or case[0] == t[0]) and (case[1] is None or t[1] in case[1]):
                return True

        return False

    @staticmethod
    def check_if_ignored(token):
        cases = [(None, ['DET']), (None, ['PUNCT', 'NUM', 'PRON']), ('cc', ['CCONJ']), ('mark', ['SCONJ']),
                 ('advmod', ['ADV']), (None, ['SYM'])]
        t = (token['deprel'], token['upostag'])

        for case in cases:
            if (case[0] is None or case[0] == t[0]) and (case[1] is None or t[1] in case[1]):
                return True

        return False

    @staticmethod
    def get_all_tokens(c):
        res = c.copy()
        children = nltk.flatten([token.children for token in c])

        if len(children) > 0:
            res += UDPipeKeywordsExtractor.get_all_tokens(children)

        return res
