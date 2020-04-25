# Minimax Concurrent Play Game

Usages:

```
python -u concurrent.py -h
usage: concurrent.py [-h] [-g G] [-e E] [-s S]

optional arguments:
  -h, --help  show this help message and exit
  -g G        Game type
  -e E        Max Episodes
  -s S        Max Steps  
 ```
  
 Currently available games and game codes:
 ```
    Sg  - SampleGame
    Sg2 - SampleGame2
    Sf  - SafetyGame1
    T   - Temperature
 ```
 
 A typical invocation:
 ```
 python -u turnBased.py -g Sf
 ```
 The `-u` option is recommended to override python output buffering
