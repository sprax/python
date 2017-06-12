#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import emoji
import re

aa = ['??', '??', '??', '??', '??', '??']

def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)


a_str = '?? ?? me así, bla es se ?? ds ??????'

emojis = extract_emojis(a_str)
print("emojis: ", emojis)

a_list = ['?? ?? me así, bla es se ?? ds ??????']

# is_emoji("??") #True
# is_emoji("????") #False

re.findall(r'[^\w\s,]', a_list[0])
