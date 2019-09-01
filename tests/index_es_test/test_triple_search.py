import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.index_elasticsearch.triple_index import TripleIndex

if __name__ == '__main__':
    triple_index = TripleIndex()
    triples = triple_index.search(subject='李白')
    print(triples)
    
    mentions = triple_index.search_candidates(subject='李白', object='唐朝')
    print(mentions)