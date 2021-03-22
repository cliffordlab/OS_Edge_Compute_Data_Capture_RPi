#!/bin/sh

: <<'END'
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 16th, 2021
Copyright [2021] [Clifford Lab]
LICENSE:    
This software is offered freely and without warranty under 
the GNU GPL-3.0 public license. See license file for
more information
END

sudo sudo service ntp stop
sudo ntpdate 0.us.pool.ntp.org
sudo service ntp start