#!/bin/bash
# exec affter run any command line.
history -c && history -w

# exec affter create device. one-time
echo 'history -c' >> ~/.bash_logout
echo 'unset HISTFILE' >> ~/.bashrc
echo 'export LESSHISTFILE="-"' >> ~/.bashrc

cat ~/.bash_history