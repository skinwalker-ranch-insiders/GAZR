# GAZR 

A BIG THANKS to https://pypi.org/project/pytchat/ for making this happen.

@johns67467 contributed the ability to send events to MySQL.<br>
@Kris - We Have Fun : Insiders Discord : Code review, library and coding suggestions<br>
@John Neiberger : Insiders Discord : Code review, library and coding suggestions<br>
@SWR Insiders : Whose patience and testing helped make this happen so fast<br>
THANK YOU ALL!

Dockerfile included:
```
$ screen
$ git clone git@github.com:skinwalker-ranch-insiders/gazr.git
$ cd gazr
$ mkdir /usr/src/gazr
$ cp gazr/* /usr/src/gazr
$ cd /usr/src/gazr
$ vi /usr/src/gazr/settings.py
```

Set the following variables:
```
s_login='email@address.com for insiders website'
s_password='password'
stellarium_server='IP or hostnme of Stellarium'
```
Build andn run your GAZR container:
```
$ sudo docker build -t gazr .
$ sudo docker run -it --name gazr -d --rm --volume $(pwd):/usr/src/gazr --net=host gazr:latest sh ./rcloak.sh
```
If you have errors or problems, rerun the last command without the -d switch to see the output and debug information.
```
$ sudo docker run -it -name gazr --rm --volume $(pwd):/usr/src/gazr -net=host gazr:latest sh ./rcloak.sh
```
When a Moderator uses #SKY: in the YT Chat, it will direct Stellarium remote control to focus on the object indicated.
