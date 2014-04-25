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
was cool and easily realizable. Instead of killing Murlocs,
I took my courage to levelup my python skills.


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
$ python3 cml.py --verbosity
```

Then you can use CacheMyLibs by using the address from you localhost
```javascript
<script src='http://127.0.0.1:8666/jquery/2.1.1-beta1/jquery.min.js'></script>
```

That's it ! CacheMyLibs will try to get it from your localhost (the cache). If the
file couldn't be find, then it will try to search the librairie from the defined
CDN and cache it for you.

Configuration options
---------------------
You can configure his nutriments by editing the configuration file *config.ini*

#### SERVER section
* port (default 8666): where to feed this animal
* pid (defaut /var/run/cml/cml.pid): check if he is alive (not implemented yet)

#### CACHE section
This section provides you some basic influence over the caching options.
* use-cache (default: yes): make him faster to catch his prey(s). By setting use-cache to `no` this tool will become somehow very useless. So I won't recommend to disable this feature.
* cache-dir (default: cache/): where to store the aliments. This is the directory where all catched file will be stored.

#### CDN section
This section will let you configure the real CDN servers that are needed to grab librairies that aren't cached
on you system.

#### LIBS section
This section let you add *aliases* over the librairies that you want
to automatically download. For instance, it will let you replace
```javascript
<script src='http://127.0.0.1:8666/jquery/2.1.1-beta1/jquery.min.js'></script>
```
by
```javascript
<script src='http://127.0.0.1:8666/jquery.min.js'></script>
```
In order to enable this you should add an entry into the configuration file. Here is a small
example of how it should look like:

```config
[LIBS]
jquery.min.js = jquery/2.1.1-beta1/jquery.min.js
react.js = react/0.10.0/react.min.js
```

Arguments options
-----------------
* --verbosity (default: False): do you want to speak with the python ?
* --config (default: config.ini): let you use a specific config file
* --port (default: None): let you specify a port value to overwrite configuration file
* --no-pid (default: False): don't check and don't use pid file

Author and contributions
=======================
Yves Lange (author)


