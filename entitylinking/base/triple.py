class Triple:
    """表示一个三元组SPO
    """

    def __init__(self, subject, predicate, object):
        self._subject = subject
        self._predicate = predicate
        self._object = object

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        self._predicate = value

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        self._object = object