import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from entitylinking.base.document import Document

def test_add_mention_context():
    origin_text = "<entity>李娜</entity>的老公是<entity>姜山</entity>"
    doc = Document(origin_text)
    print(" ".join(doc.mention_list[0].context))
    print(" ".join(doc.mention_list[1].context))

    origin_text = "打球的<entity>李娜</entity>和唱歌的<entity>李娜</entity>不是同一个人"
    doc = Document(origin_text)
    print(" ".join(doc.mention_list[0].context))
    print(" ".join(doc.mention_list[1].context))
    
    doc = Document('<entity>李白</entity>这首歌是在唱唐朝的<entity>李白</entity>吗？')
    print(" ".join(doc.mention_list[0].context))
    print(" ".join(doc.mention_list[1].context))


test_add_mention_context()