from typing import List, Tuple
from cblack.config.tox import ToxIniBlackConfigParser
from cblack.config.setupcfg import SetupCfgBlackConfigParser
from cblack.config.pyprojecttoml import (
    PyprojectTomlBlackConfigParser,
)
import logging
import argparse
import subprocess
import os
import sys
from cblack.utils.out import pretty_args
from cblack.utils.proc import execute, get_black_args

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stderr))


class Runner:
    def get_args(self) -> Tuple[List[str], List[str]]:
        parsers = [
            SetupCfgBlackConfigParser(),
            ToxIniBlackConfigParser(),
            PyprojectTomlBlackConfigParser(),
        ]
        found = []
        for parser in parsers:
            config = parser.parse()
            if config is None:
                continue
            found.append([parser, config])

        config = found[-1][1] if found else {}
        if len(found) > 1:
            found_files = [f[0].filename for f in found]
            found_files = ", ".join(found_files)
            keep = found[-1][0].filename
            msg = "Found configs in {}, keeping {}".format(found_files, keep)
            logger.warning(msg)

        black_args = get_black_args()
        parser = argparse.ArgumentParser()
        _, extra_args = parser.parse_known_args()
        extra_args_set = set(extra_args)

        args = []
        for k in config:
            k_arg = "-{}".format(k)
            if k_arg not in black_args:
                k_arg = "--{}".format(k)
            if k_arg not in black_args:
                msg = '"{}" not found in supported black args'.format(k)
                logger.warning(msg)
                if len(k) == 1:
                    k_arg = "-{}".format(k)
                else:
                    k_arg = "--{}".format(k)
            if (
                black_args.get(k_arg, set()).intersection(extra_args_set)
                or k_arg in extra_args_set
            ):
                continue

            v = config[k]
            if v is None:
                args.append(k_arg)
                continue
            if not isinstance(v, list):
                args.extend([k_arg, v])
                continue
            for vv in v:
                args.extend([k_arg, vv])
        return args, extra_args

    def run(self) -> int:
        args, extra_args = self.get_args()
        env = os.environ.copy()
        pargs = " ".join(["black", *pretty_args(args), *extra_args])
        sys.stderr.write(" > {}".format(pargs))
        sys.stderr.write("\n")
        sys.stderr.flush()
        args = ["black"] + args + extra_args
        try:
            for line, file in execute(
                args,
                env=env,
                universal_newlines=True,
            ):
                file.write(line)
                file.flush()
        except subprocess.CalledProcessError as e:
            return e.returncode
        return 0
