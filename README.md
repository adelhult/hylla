<div align="center">
    <img width="400" height="280" src="media/logo.svg" alt="Hylla">
      <br>
      <br>
      <p>
          <b>Hylla is a command-line tool used to organize your projects.</b>
      </p>
      <!-- <p>
            <i>
                  Hylla is Swedish, meaning both 'shelf' and 'honour'.<br/>
                  So, honour your projects by neatly organizing them on a digital shelf using simple commands.
            </i>
      </p> -->
      <hr/>
      <p>
          <a href="https://github.com/adelhult/hylla#star-features ">Features</a> •
          <a href="https://github.com/adelhult/hylla#checkered_flag-setup">Setup</a> •
          <a href="https://github.com/adelhult/hylla#computer-usage">Usage</a> •
          <a href="https://github.com/adelhult/hylla/wiki">Documentation</a> •
          <a href="https://github.com/adelhult/hylla#license">License</a>
      </p>
</div>

## :star: Features

* Create project directories and keep them organized in one place.

* Generate a README.md file for every project.

* List all projects and search for them with subject tags.

* Launch custom scripts and start software every time a project is opened.

## :checkered_flag: Setup

Hylla is quick and easy to setup. Create a directory in which you wish to store all your projects, then give the environmental variable `HYLLA_LOCATION` the value of the directory path.

## :computer: Usage

It's often easier to learn by looking at a few examples instead of **[reading documentation](https://github.com/adelhult/hylla/wiki)**. In this very simple example below a project named *amazing_project* is created. This means that Hylla automatically creates a directory but also a README.md documentation file.

```
hylla new amazing_project
```

If we now wish to start working on our *amazing_project* it's as simple as using the open command. This will start a file manager at the project location.

```
hylla open amazing_project
```

**Is that all?** No, Hylla can do a lot more. Here is a more complex example.

```
hylla new ezgallery web php --commands --github adelhult ezgallery
```

This single command creates a project named *ezgallery* and clones a repo with the same name from my Github account adelhult. The two subject tags *web* and *php* are added as well to make it easier to later search for the project. The `--commands` flag means that a text editor will open and allow you to write a list of commands that are executed every time a project is opened. For example, if it's a coding project you're working on it might be handy to directly open your favourite text editor or execute some custom setup commands.

**More information about using all of Hyllas commands and options can be found by using the `--help` option or reading the [documentation](https://github.com/adelhult/hylla/wiki).**

# License

[MIT License](https://choosealicense.com/licenses/mit/)
