import subprocess

def run_cmd(cmd: str):
    proc = subprocess.run(
        ['bash', '-c', cmd], capture_output=True)
    if proc.returncode != 0:
        msg = 'expected exit code 0 from `{}`, got exit code {}: {}'.format(
            cmd, proc.returncode, proc.stdout.decode('unicode_escape'))
        if proc.stderr:
            msg += ' ' + proc.stderr.decode('unicode_escape')
        raise ValueError(msg)