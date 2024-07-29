What is this?
=============

Fractals is a fractal simulation activity for the Sugar desktop. Fractals are fascinating patterns that look similar at various scales of magnification. If you zoom in on a fractal, no matter how close you get, you still see the same or similar shapes repeating themselves.

How to use?
===========

Fractals can be run on the Sugar desktop.  Please refer to;

* [How to Get Sugar on sugarlabs.org](https://sugarlabs.org/),
* [How to use Sugar](https://help.sugarlabs.org/)

How to run?
=================

Dependencies:- 
- Python >= 3.10
- PyGObject >= 3.42
- PyGame >= 2.5
  
These dependencies need to be manually installed on Debian, Ubuntu and Fedora distributions.


**Running outside Sugar**


- Install the dependencies

- Clone the repo and run -
```
git clone https://github.com/vaibhav-sangwan/fractals.git
cd fractals
python main.py
```

**Running inside Sugar**

- Open Terminal activity and change to the Fractals activity directory
```
cd activities\Fractals.activity
```
- To run
```
sugar-activity3 .
```
