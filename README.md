# Rosie's Bar 🐕
Automatic dog feeder in a portable Docker image.

<p align="center">
  <img src="res/rosie.jpeg" width="600">
</p>

## Description
Automatically dispense food for your animal at different given hours of the day.  
This software is designed to be dumped as a Docker image into a Raspberry connected to a motor Controler. All hardware-related setup and plans are currently not available on the repository.


# Installation
```shell
git clone https://github.com/NicolasBizzozzero/Rosies-Bar
```

# Running
```shell
./script/docker_build.sh
./script/docker_run.sh
```

# FAQ
* What happens if a croquette is stuck between the motor ?
  * We specifically chose a motor strong enough to break the croquette if that happens.


# Acknowledgments
Thank you to my good friend Guillaume Emery for setting-up this project with me and to make it happen.
