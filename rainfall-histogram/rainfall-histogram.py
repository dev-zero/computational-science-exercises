#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
# This fetches the page from the URL, applies
# the specified XPATH expression and plots the numbers
# in the expression

URL   = 'http://worldweather.wmo.int/087/c00312.htm'
XPATH = '/html/body/table/tr/td[3]/table[2]/tr[11]/td/table/tr/td/table/tr/td[4]/b/font'

import lxml.html
from pylab import bar, xlabel, ylabel, show

# let lxml fetch the the url and apply the xpath expression
elements = lxml.html.parse(URL).xpath(XPATH)

bar(range(12), [int(e.text) for e in elements], width = 1)
xlabel("Month number")
ylabel("Rain in mm")
show()


