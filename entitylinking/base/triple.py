import re


class Triple:
    """表示一个三元组SPO
    """

    def __init__(self, subject_id, subject, predicate, object, object_id=0):
        self._id = subject_id
        self._subject = subject
        self._predicate = predicate
        if object != None:
            self._object = object
        else:
            self._object = ""
        self._object_id = object_id

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
        self._object = value

    @property
    def subject_id(self):
        return self._id

    @subject_id.setter
    def subject_id(self, value):
        self._id = value

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = value
