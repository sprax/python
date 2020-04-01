
from subprocess import Popen, PIPE
import errno

p = Popen('less', text=True,
    stdin=PIPE)

for x in range(100):
    line = 'Line number %d.\n' % x
    try:
        p.stdin.write(line)


    except IOError as e:
        if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
            # Stop loop on "Invalid pipe" or "Invalid argument".
            # No sense in continuing with broken pipe.
            break
        else:
            # Raise any other error.
            raise

p.stdin.close()
p.wait()

print('All done!') # This should always be printed below any output written to less.
