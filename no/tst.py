
>>> rgxb = re.compile(r"^\s*['\"]")
>>>
>>> tr()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'tr' is not defined
>>>
>>> def tr():
...

KeyboardInterrupt
>>> def tr(ex):
...     if (ex):
...             print('True')
...     else
  File "<stdin>", line 4
    else
       ^
SyntaxError: invalid syntax
>>>
>>>
>>>
>>> def tr(ex):
...     if (ex):
...             print('True')
...     else:
...             print('false')
...
>>> tr(1)
True
>>> tr(re.match(rgxm, "33. duh")
... )
True
>>> tr(re.match(rgxm, "hazard 33. duh"))
false
>>> sst = "'" + ss + "'"
>>> sst
"'Why, it's what I'm obliged to keep a little of in the house, to putinto the blessed infants' Daffy
, when they ain't well, Mr. Bumble,'replied Mrs. Mann as she opened a corner cupboard, and took down
 abottle and glass.  'It's gin.  I'll not deceive you, Mr. B.  It's gin.'"
>>> rgxb
re.compile('^\\s*[\'\\"]')
>>> mb = re.match(rgxb, sst)
>>> mb.dir

