import random
import pytest

@pytest.fixture(scope="module")
def random_endpoint() -> int:
    return random.randint(1,100)
