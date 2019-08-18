import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

input_args = ['-s', '.', '-m=node_cmp']
pytest.main(input_args)