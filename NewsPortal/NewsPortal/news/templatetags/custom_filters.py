from django import template

register = template.Library()


@register.filter()
def censor(value):
    # print(value)
    censor_word = ['редиска', 'Some']
    words = value.split()
    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected type 'str'")
    for word in words:
        word = word.replace(',', '').replace('.', '')
        if word in censor_word:
            # print(1)
            # print(word[0] + ('*' * (len(word) - 1)))
            value = value.replace(word, word[0] + ('*' * (len(word) - 1)))
            # print(value)
    return value
