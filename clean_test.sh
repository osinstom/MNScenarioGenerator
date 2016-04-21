#!/bin/bash
sudo pkill -9 test_
sudo pkill -9 ITG
sudo pkill -9 twistd
sudo pkill -9 iperf
sudo pkill -9 wget
sudo pkill -9 test_d
sudo mn -c
