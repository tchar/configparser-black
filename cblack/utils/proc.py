import subprocess
from typing import Dict, Generator, List, Any, Set, TextIO, Tuple
from itertools import zip_longest
import sys
import re
from functools import lru_cache


def execute(
    cmd: List[str], **kwargs: Any
) -> Generator[Tuple[str, TextIO], None, None]:
    kwargs = {**kwargs, "stderr": subprocess.PIPE, "stdout": subprocess.PIPE}
    proc = subprocess.Popen(cmd, **kwargs)
    zipped_outs = zip_longest(
        iter(proc.stdout.readline, ""), iter(proc.stderr.readline, "")
    )
    for stdout_line, stderr_line in zipped_outs:
        if stdout_line is not None:
            yield stdout_line, sys.stdout
        if stderr_line is not None:
            yield stderr_line, sys.stderr
        if stderr_line == b"" and stdout_line == b"":
            break
    proc.stdout.close()
    proc.stderr.close()
    return_code = proc.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, proc)


@lru_cache()
def get_black_args() -> Dict[str, Set[str]]:
    cmd = ["black", "--help"]
    args = {}
    arg_match = r"--?[a-zA-Z0-9_-]+"
    regex = re.compile(f"^\s+{arg_match}(?:,\s{arg_match})?")
    try:
        for line, _ in execute(cmd):
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            sub_args = regex.findall(line)
            if not sub_args:
                continue
            sub_args = sub_args[0].split(",")
            sub_args = map(str.strip, sub_args)
            sub_args = filter(None, sub_args)
            sub_args = list(sub_args)
            for sub_arg in sub_args:
                args[sub_arg] = set(sub_args)
    except subprocess.CalledProcessError:
        pass
    return args
