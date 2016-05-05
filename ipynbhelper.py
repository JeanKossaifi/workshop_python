"""Utility script to be used to cleanup the notebooks before git commit

This a mix from @minrk's various gists.

"""

import sys
import os
import io
try:
    from queue import Empty
except:
    from Queue import Empty

from nbformat import current
try:
    from jupyter_client import KernelManager
    assert KernelManager  # to silence pyflakes
except ImportError:
    # 0.13
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager
    KernelManager = BlockingKernelManager


def remove_outputs(nb):
    """Remove the outputs from a notebook"""
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                if 'prompt_number' in cell:
                    del cell['prompt_number']


def remove_signature(nb):
    """Remove the signature from a notebook"""
    if 'signature' in nb.metadata:
        del nb.metadata['signature']


def process_notebook_file(fname, action='clean', output_fname=None):
    print("Performing '{}' on: {}".format(action, fname))
    orig_wd = os.getcwd()
    with io.open(fname, 'r') as f:
        nb = current.read(f, 'json')

    if action == 'check':
        os.chdir(os.path.dirname(fname))
        run_notebook(nb)
        remove_outputs(nb)
        remove_signature(nb)
    else:
        # Clean by default
        remove_outputs(nb)
        remove_signature(nb)

    os.chdir(orig_wd)
    if output_fname is None:
        output_fname = fname
    with io.open(output_fname, 'w') as f:
        nb = current.write(nb, f, 'json')


if __name__ == '__main__':
    # TODO: use argparse instead
    args = sys.argv[1:]
    targets = [t for t in args if not t.startswith('--')]
    action = 'check' if '--check' in args else 'clean'
    action = 'render' if '--render' in args else action

    if not targets:
        targets = [os.path.join(os.path.dirname(__file__), 'notebooks')]

    for target in targets:
        if os.path.isdir(target):
            fnames = [os.path.abspath(os.path.join(target, f))
                      for f in os.listdir(target)
                      if f.endswith('.ipynb')]
        else:
            fnames = [target]
        for fname in fnames:
            output_fname = fname
            process_notebook_file(fname, action=action,
                                  output_fname=output_fname)
