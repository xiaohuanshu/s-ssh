from __future__ import print_function
from sshconf import read_ssh_config, empty_ssh_config
from os.path import expanduser
import fnmatch
import fire
import libtmux
import random


class SuperSSH(object):
    ssh_hosts = filter(lambda x: '*' not in x, read_ssh_config(expanduser("~/.ssh/config")).hosts())

    def __init__(self, layout='main-horizontal'):
        self.layout = layout

    @staticmethod
    def ssh_host_filter(pattern):
        return fnmatch.filter(SuperSSH.ssh_hosts, pattern)

    def _init_tmux(self):
        server = libtmux.Server()
        session = server.new_session('test5', window_command='pwd', window_name='asdf')
        window = session.new_window(attach=False, window_name="ha in the bg")
        # window.select_window()\
        session.attach_session()

    def multi(self, pattern):
        if '*' not in pattern:
            pattern += '*'
        hosts = SuperSSH.ssh_host_filter(pattern)
        if not hosts:
            print("Not match any hosts")
            exit()

        server = libtmux.Server()
        session = server.new_session(
            session_name='ssh-%s-%d' % (pattern.replace("*", ""), random.randint(1000, 9999)),
        )
        w1 = session.attached_window
        w1.move_window(99)
        w = session.new_window(
            attach=True,
        )
        for i, host in enumerate(hosts, start=1):
            if i == 1:
                p = w.attached_pane
            else:
                p = w.split_window(
                    attach=False,
                    target=p.id,
                )
            p.send_keys("printf '\\033]2;%s\\033\\\\'" % host)
            p.cmd("set", "pane-border-format", "#{pane_index} #T")
            p.cmd("set", "pane-border-status", "top")
            p.send_keys('ssh %s && exit' % host)
            p.send_keys('clear')
        w1.kill_window()
        w.cmd("set", "synchronize-panes")
        session.set_option('mouse', True)
        session.set_option('main-pane-height', 300)
        w.select_layout(self.layout)
        session.attach_session()


def main():
    fire.Fire(SuperSSH)


if __name__ == '__main__':
    main()
