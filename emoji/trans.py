#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import emoji
import re
from collections import defaultdict

def selflist(word):
    return [word]

def getsyl(map, word):
    syls = map.get(word)
    return sysl if syls else word

def trans():
    wtsl = defaultdict(selflist)
    sent = "wind and waves may rock the boat, but only you can tip the crew"
    words = re.split(r'\W+', sent.rstrip())
    print(words)
    for word in words:
        print("{} => {}".format(word, getsyl(wtsl, word)))

def char(i):
    try:
        return chr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')

def unicode_chr_str(hex_unicode):
    if '-' not in hex_unicode:
        return char(int(hex_unicode, 16))
    parts = hex_unicode.split('-')
    return ''.join(char(int(x, 16)) for x in parts)

if __name__ == '__main__':
    trans()
    print(u'\U0001f604'.encode('unicode-escape'))
    print(u'\U0001f604')
    ss = u'\U0001f604'
    #xx = chr(ss[0])
    #print("ss({}) xx({})".format(ss, xx))
    # -*- coding: UTF-8 -*-
    #convert to unicode
    teststring =  "I am happy \U0001f604"
    # #teststring = unicode(teststring, 'utf-8')

for i, t in enumerate(sorted(jt.items(), key=lambda x: int(x[1]['order']), reverse=True)):
...     if i < 10:
...             ck = unicode_chr_str(t[0])
...             print(ck, "\t", len(ck), "\t", t[1]['order'], "\t", t[0], "\t", t[1]['shortname'])

    #encode it with string escape
    teststring = teststring.encode('unicode_escape')
    print("💗 Growing Heart")
    print(emoji.emojize('Water! :water_wave:'))
    print(emoji.demojize(u'🌊')) # for Python 2.x
# print(emoji.demojize('🌊')) # for Python 3.x.
    print(u"And \U0001F60D")
    print("(-woman) astronaut", chr(int("0001f680", 16)))
    print("woman_astronaut", chr(int("0x0001f680", 0)))

    print("\U0001f483\U0001f3fe")

    print(chr(0x001f483),chr(0x001f3fe))
    print('💃 🏾 ')
    print(chr(0x001f483)+chr(0x001f3fe))
    print('💃🏾 ')
    print(chr(int('1f483',16))+chr(int('1f3fe',16)))

dec_emo = {
	127744: ['🌀 ', 'blue-spiral', ''],
	127745: ['🌁 ', 'foggy-mountain', ':foggy:'],
	127746: ['🌂 ', 'umbrella-down', ':closed_umbrella:'],
	127747: ['🌃 ', 'city-at-night', ':night_with_stars:'],
	127748: ['🌄 ', 'sunrise-over-mountains', ':sunrise_over_mountains:'],
	127749: ['🌅 ', 'ocean-sunrise', ':sunrise:'],
	127750: ['🌆 ', 'city-at-dusk', ':city_dusk:'],
	127751: ['🌇 ', 'city-sunset', ':city_sunset:'],
	127752: ['🌈 ', 'rainbow', ':rainbow:'],
	127753: ['🌉 ', 'bridge-at-night', ':bridge_at_night:'],
	127754: ['🌊 ', 'wave', ':ocean:'],
	127755: ['🌋 ', 'volcano', ':volcano:'],
	127756: ['🌌 ', 'milky-way', ':milky_way:'],
	127757: ['🌍 ', 'globe-africa', ':earth_africa:'],
	127758: ['🌎 ', 'globe-americas', ':earth_americas:'],
	127759: ['🌏 ', 'globe-asia-australia', ':earth_asia:'],
	127760: ['🌐 ', 'globe with meridians'],
	127761: ['🌑 ', 'new moon', ':new_moon:'],
	127762: ['🌒 ', 'quarter moon', ':waxing_crescent_moon:'],
	127763: ['🌓 ', 'halfmoon', ':first_quarter_moon:'],
	127764: ['🌔 ', 'three-quarter moon'],
	127765: ['🌕 ', 'full moon', ':full_moon:'],
	127766: ['🌖 ', 'waning gibbous moon', ':waning_gibbous_moon:'],
	127767: ['🌗 ', 'waning halfmoon', ':last_quarter_moon:'],
	127768: ['🌘 ', '', ':waning_crescent_moon:'],
	127769: ['🌙 ', '', ':crescent_moon:'],
	127770: ['🌚 ', '', ':new_moon_with_face:'],
	127771: ['🌛 ', '', ':first_quarter_moon_with_face:'],
	127772: ['🌜 ', '', ':last_quarter_moon_with_face:'],
	127773: ['🌝 ', '', ':full_moon_with_face:'],
	127774: ['🌞 ', '', ':sun_with_face:'],
	127775: ['🌟 ', '', ':star2:'],
	127776: ['🌠 ', 'shooting star', ':dizzy:'],
	127777: ['🌡 ', 'thermometer', '', 'hot'],
##
	127780: ['🌤 ', '', ':white_sun_small_cloud:'],
	127781: ['🌥 ', '', ':parly_sunny:'],
	127782: ['🌦 ', '', ':white_sun_rain_cloud'],
	127783: ['🌧 ', '', ':cloud_rain:'],
	127784: ['🌨 ', '', ':cloud_snow:'],
	127785: ['🌩 ', '', ':cloud_lightning:'],
	127786: ['🌪 ', '', ':cloud_tornado:'],
	127787: ['🌫 ', '', ':fog:'],
	127788: ['🌬 ', '', ':wind_blowing_face'],
	127789: ['🌭 ', '', ':hotdog:'],
	127790: ['🌮 ', '', ':taco:'],
	127791: ['🌯 ', '', ':burrito'],
	127792: ['🌰 ', '', ':chestnut:'],
	127793: ['🌱 ', '', ':seedlig:'],
	127794: ['🌲 ', '', ':evergreen_tree:'],
	127795: ['🌳 ', '', ':deciduous_tree'],
	127796: ['🌴 ', '', ''],
}
