import re

import pytest

import micromagneticmodel as mm


class MyDerivedClass(mm.abstract.Abstract):
    _allowed_attributes = ["arg1", "arg2"]


class TestAbstract:
    def setup(self):
        self.obj = MyDerivedClass(arg1=1, arg2="abc")

    def test_init(self):
        assert self.obj.arg1 == 1
        assert self.obj.arg2 == "abc"

        with pytest.raises(AttributeError):
            MyDerivedClass(arg1=1, arg3=3)  # arg3 not allowed

    def test_iter(self):
        assert len(list(self.obj)) == 2
        assert "arg1" in list(zip(*list(self.obj)))[0]

        obj = MyDerivedClass(arg2="abc")
        assert len(list(obj)) == 1
        assert "arg2" in list(zip(*list(obj)))[0]
        assert "arg1" not in list(zip(*list(obj)))[0]

    def test_name(self):
        assert self.obj.name == "myderivedclass"

    def test_repr(self):
        assert re.search(r"MyDerivedClass\(arg1=.+, arg2=.+\)", repr(self.obj))
