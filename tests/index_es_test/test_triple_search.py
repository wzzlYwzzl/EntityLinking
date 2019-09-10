import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.index_elasticsearch.triple_index_with_id import TripleIndex

if __name__ == '__main__':
    triple_index = TripleIndex()
    
    new_str = triple_index.handle_special_char('苏华董事长简介 - 四川现代教育集团')
    print(new_str)
    
    triples = triple_index.search(subject='李白')
    print(triples)
    
    mentions = triple_index.search_candidates(subject='李白', object='唐朝')
    print(mentions)