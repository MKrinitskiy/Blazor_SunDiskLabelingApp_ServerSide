from pkg_resources import resource_string

# See http://jbauman.com/aboutgsl.html
words = resource_string(__name__, "horsephrase_words.txt").decode("utf-8").split()

from random import SystemRandom

def generate_horsephrase(number=2, choice=SystemRandom().choice, words=words, joiner="-"):
    """
    Generate a random passphrase from the GSL.
    """
    return joiner.join(choice(words) for each in range(number))


def output():
    print(generate())
    return 0
