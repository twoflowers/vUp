# vUp - Virtual Machine Up


vUp allows for you to create your production environment locally.  

Using a mix of vagrant and docker, vUp will allow for you to easily and seamlessly create a development environment without the hassle of configuration. 

Simple Layout to easily drag and drop components for the application

## Installation and Setup

To run this project, install [Vagrant][vagrant], and then the `hostmanager` plugin:

    vagrant plugin install vagrant-hostmanager

To access the project, load http://192.168.4.2/ (the address of the `vup` machine, as defined in the Vagrantfile) in your browser. If you encounter a `502 Bad Gateway` error, run the following:

    vagrant ssh vup
    sudo su
    service uwsgi restart

This is an issue [with `uWsgi` in vagrant][issue9].

![The UI](http://i.imgur.com/xWJVbPt.png?1)

What it will look like once the components are in place
![The Project](http://i.imgur.com/RAYwMMh.png?1)



