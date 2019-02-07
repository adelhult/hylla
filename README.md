<div align="center">
	<img width="400" height="280" src="media/logo.svg" alt="Hylla">
  	<br>
  	<br>
  	<p>
    		<i>
      			Hylla is Swedish, meaning both 'shelf' and 'honour'.<br/>
      			So, honour your projects by neatly organizing them on a digital shelf using simple commands.
    		</i>
  	</p>
</div>

## :star: Features
* Create project directories and keep them organized in one place.

* Generate a README.md file for every project.

* List all projects and search for them with subject tags.

* Launch custom scripts and start software every time a project is opened. 


## :computer: Usage
Before you start using Hylla, define the environmental variable ```HYLLA_LOCATION``` to let the program know where all your projects should be stored. (Must be the path to an existing directory.)
```
hylla [OPTIONS] COMMAND [ARGS]
```
Note, if Hylla is executed without specifying a command, a list of all available options and commands will be printed.

### Create a new project
```
hylla new [OPTIONS] NAME [TAGS] ...
```
**Options:**

```--commands```
Allows the user to write a list of commands that will be executed every time the project is opened.

```--clone```
The user will later be prompted to enter the URL to a repository to git clone from.

```--readme-template FILE```
Specify a template which will be used to create the project README.md, 
the environmental variable HYLLA_README_TEMPLATE can also be used.

```--help```
Prints help information about the 'new' command.
	
 ### Open a project
Prints the project path and executes all the commands that the user has specified. 
```
hylla open [OPTIONS] NAME
```
**Options:**
	
```--safe```
If the safe flag is added, no commands will be executed.
	
```--help```
Prints help information about the 'open' command.

### List all projects
```
hylla list
```
**Options:**
```--tag```
List projects containing a specific subject tag.

```--detailed```
List more information about each project

```--help```
Prints help information about the 'list' command.

### Open Github page
```
hylla docs
```
Will open this page in a web browser. 

### Edit a project
Work in progress

### Delete a project
Work in progress


### Open the directory where all the projects are stored
```
hylla home
```
## License
[MIT License](https://choosealicense.com/licenses/mit/)
