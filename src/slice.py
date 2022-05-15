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

with open("data/videos.txt", "r") as f:
    lines = []
    for line in f:
        line = line.strip()
        if line == '' or line.startswith('#'):
            # Comment or blank line
            continue
        line = line.split(',')
        times = [t.split('-') for t in line[1:]]
        lines.append((line[0], times))

for key, times in lines:
    print(key)
    for i, (start, end) in enumerate(times):
        start_min, start_sec = ["0" + s if len(s) == 1 else s
                                for s in [str(int(i))
                                          for i in start.split(':')]]
        end_min, end_sec = ["0" + s if len(s) == 1 else s
                            for s in [str(int(i))
                                      for i in end.split(':')]]
        start_time = f'00:{start_min}:{start_sec}'
        end_time = f'00:{end_min}:{end_sec}'
        #print(f'  {start_time} - {end_time}')
        cmd = f'ffmpeg -i download/cache/{key}.mp4 -ss {start_time} -c copy -to {end_time} download/processed/{key}.{i}.mp4'
        print(cmd)
        run_cmd(cmd)