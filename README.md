# PycEditor #

[![Build Status](https://travis-ci.org/moff4/PycEditor.svg?branch=master)](https://travis-ci.org/moff4/PycEditor) 

Tool for editing `.pyc` files and Python bytecode in runtime.  

### Example:  

"Some code":
```python
def f():
    print('Hello World')
```

Editing this "some code"
```python
import random
import pyceditor
pyc = pyceditor.PycFile.load_from_pycode(f.__code__)
x = random.randint(15, 10**4)
pyc.code.co_consts = (None, 'Hi! Random number: %d' % x)
eval(pyc.pycode)
# prints random number
```


[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/komissarov)
