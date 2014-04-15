CacheMyLibs
===========

Introduction
------------
Simple proxy that can download Javascript (or other) librairies for you.
This tools was made for lazy developpers like me. Everytime I started a project
that needs some JavaScript librairies I needed to download them or install some
other big tools to do it for me.


History
-------
Hugo (a little Tauren from the Orgrimmar city) mentionned the idea to create
a little proxy server that will directly download libs. I found that this idea
was cool and easily realizable. While he was spending his time killing some Murlocs
near Lordaeron, I took my courage to levelup my python skills.


Why Python ?
------------
Pythons are easy to cache and can be very and can be very fierce and unpredictable.
Also you can easily read in them and learn from them how to be sneaky. It's also
the main language from Archlinux and Raspberry Pi. Good enough ?


How to use this tool ?
======================
You will need **Python 3.x** as a dependency so don't forget to bring your
python into your home. Feed them a bit some time by launching the server:

```shell
$ python3 cml.py
```

You can configure his nutriments by editing the configuration file *config.ini*


Configuration options
---------------------
#### SERVER section
* port (default 8666): where to feed this animal
* pid (defaut /var/run/cml/cml.pid): check if he is alive

#### CACHE section
* use-cache (default: yes): make him faster to catch his prey(s). By setting use-cache to `no` this tool will become somehow very useless. So I won't recommend to disable this feature.
* cache-dir (default: cache/): where to store the aliments. This is the directory where all catched file will be stored.


Arguments options
-----------------
None for the moment


What about the author ?
=======================
He stopped playing World of Warcraft to create small tools for the community. It might not be very usefull for most of you but he enjoys a lot typing text and eating Marshmallows in front of his screen... no matter what ! Actually he works at AgFlow with a very great team that going to kill him because he is not fully concentrate on the work and invovlved in some stupid create that are useless for them ! Shit !
