fatpacker
=========

Package up your code into a standalone script file.

Let's say you've got a project, like this one:

```
setup.py
lib/
└── fatpacker
    ├── cli.py
    └── __init__.py
tools/
└── fatpacker
```

Your lovely fatpacker script depends on `lib/fatpacker/cli.py` but you want to
make your code easy to distribute! Not only that, `setup.py` has external
dependencies. How do we get this to our users in the simplest possible manner?

Enter: fatpacker. Fatpacker will pull together all of your dependencies with
[spindrift](https://github.com/f0rk/spindrift) and push them into a single, runnable file.

install
=======

```!sh
$ curl https://raw.githubusercontent.com/f0rk/fatpacker/master/tools/fatpacker-standalone > ~/bin/fatpacker
$ chmod +x ~/bin/fatpacker
```

usage
=====

```!sh
$ fatpacker --package-name fatpacker \
    --package-entry $'from fatpacker.cli import App\napp = App()\napp.run()' \
    --output-path /tmp/fatpacker-standalone
```

and behold:

```!sh
$ cat /tmp/fatpacker-standalone
#!/usr/bin/env python

import base64
import io
import sys
import tempfile
import zipfile

main = b'UEsDBBQAAAAIAAAAIQCp5Em2MAAAADMAAAAIA...'

data = io.BytesIO(base64.b64decode(main))

zf = zipfile.ZipFile(data)

with tempfile.TemporaryDirectory() as temp_path:
    zf.extractall(temp_path)

    sys.path.insert(0, temp_path)

    from fatpacker.cli import App
    app = App()
    app.run()
```

```!sh
$ /tmp/fatpacker-standalone --help
usage: fatpacker-standalone [-h] --package-name PACKAGE_NAME
                            [--package-entry PACKAGE_ENTRY]
                            [--package-runtime PACKAGE_RUNTIME]
                            [--extra-package EXTRA_PACKAGE]
                            [--output-path OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --package-name PACKAGE_NAME
                        name of the package you want to package
  --package-entry PACKAGE_ENTRY
                        entry point to your code. should either be a handler
                        function or the flask app, and it must be imported as
                        handler or as app for lambda, or application for
                        elastic beanstalk
  --package-runtime PACKAGE_RUNTIME
                        the runtime to package for
  --extra-package EXTRA_PACKAGE
                        any extra packages to install. use multiple times to
                        specify multiple packages.
  --output-path OUTPUT_PATH
                        where to output the resulting zip file
```
