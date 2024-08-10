import re
p = r'<t/(\S*)/t>'
print(re.findall(p, "hello there! How are you? <t/function()/t> <t/heaven()/t> <h/should I use it?/h>"))

