# Copyright 2021, Ryan P. Kelly.

import argparse
import base64
import io
import os
import stat
import sys
import tempfile

from spindrift.packager import package


class App(object):

    def run(self):

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--package-name",
            help="name of the package you want to package",
            required=True,
        )

        parser.add_argument(
            "--package-entry",
            help=(
                "entry point to your code. should either be a handler "
                "function or the flask app, and it must be imported as "
                "handler or as app for lambda, or application for elastic "
                "beanstalk"
            ),
        )

        default_runtime = "python{}.{}".format(
            sys.version_info[0],
            sys.version_info[1],
        )

        parser.add_argument(
            "--package-runtime",
            help=(
                "the runtime to package for (default: {})"
                .format(default_runtime)
            ),
            default=default_runtime,
        )

        parser.add_argument(
            "--extra-package",
            help=(
                "any extra packages to install. use multiple times to "
                "specify multiple packages."
            ),
            action="append",
        )

        parser.add_argument(
            "--output-path",
            help="where to output the resulting zip file",
        )

        args = parser.parse_args()

        with tempfile.NamedTemporaryFile() as tf:

            package(
                args.package_name,
                "plain",
                args.package_entry,
                args.package_runtime,
                tf.name,
                extra_packages=args.extra_package,
            )

            tf.flush()
            tf.seek(0)

            main = base64.b64encode(tf.read())

            template = """#!/usr/bin/env python

import base64
import io
import sys
import tempfile
import zipfile

main = {main!r}

data = io.BytesIO(base64.b64decode(main))

zf = zipfile.ZipFile(data)

with tempfile.TemporaryDirectory() as temp_path:
    zf.extractall(temp_path)

    sys.path.insert(0, temp_path)

{entry}
"""

            entry_lines = args.package_entry.split("\n")
            entry_lines = ["    " + el.strip() for el in entry_lines]

            entry = "\n".join(entry_lines)

            contents = template.format(main=main, entry=entry)

            if args.output_path:

                set_mode = False
                if not os.path.exists(args.output_path):
                    set_mode = True

                with open(args.output_path, "wt") as fp:
                    fp.write(contents)

                if set_mode:
                    st = os.stat(args.output_path)
                    os.chmod(
                        args.output_path,
                        st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                    )
            else:
                sys.stdout.write(contents)
