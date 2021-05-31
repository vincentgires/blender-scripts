import os
import subprocess


def sequence_to_gif(
        inputs, output, fps=15, optimize=True, depth=8, bounce=False):
    """Convert image sequence to gif

    Inputs can be folder or list of image paths.
    """

    if isinstance(inputs, str):
        if os.path.isdir(inputs):
            inputs = [os.path.join(inputs, i) for i in os.listdir(inputs)]
            inputs.sort()

    fps = '1x{}'.format(fps)
    command = [
        'magick',
        '-delay', fps,
        '-loop', '0']
    command.extend(inputs)
    if bounce:
        command.extend(['-duplicate', '1,-2-1'])
    if optimize:
        command.extend(['-layers', 'optimize'])
    if depth:
        command.extend(['-depth', str(depth)])
    command.append(output)
    subprocess.call(command)
