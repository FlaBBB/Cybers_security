
import re

restricted = '!"#$%&\'+,-/\\;<>?@*^`|~0123456789'
# code = input('>>> ')
code = "_.__dir__.__class__.__base__.__subclasses__()"

assert (code.count('_') < 30)
assert (len(code) < 150)

if not re.findall('[%s]' % re.escape(restricted), code):
    try:
        print(eval(code, {'__builtins__': None, '_': {}.__class__.__subclasses__()}))
    except:
        pass
else:
    print('Restricted characters detected!', re.findall('[%s]' % re.escape(restricted), code))