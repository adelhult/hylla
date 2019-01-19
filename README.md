<div align="center">
	<img width="500" height="350" src="media/logo.svg" alt="Hylla">
  	<br>
  	<br>
  	<p>
    		<i>
      			Hylla is Swedish, meaning both 'shelf' and 'honour'.<br/>
      			So, honour your projects by neatly organizing them on a digital shelf using simple commands.
    		</i>
  	</p>
</div>

## About :grey_question:
Yet to write this section

## Usage :computer:
```
hylla [OPTIONS] COMMAND [ARGS]
```
Note, if Hylla is executed without specifying a command, a list of all available options and commands will be printed.

### Create a new project
```
hylla new [OPTIONS] NAME [TAGS] ...
```
**Options:**

```--readme-template FILE```
Specify a template which will be used to create the project README.md, 
the environmental variable HYLLA_README_TEMPLATE can also be used.

```--commands```
Allows the user to write a list of commands that will be executed every time the project is opened.

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
This function will be more advanced in a future version, making it possible to search for projects based upon tag(s) and possibly date.

### Open Github page
```
hylla docs
```
Will open this page in a web browser. 

### Edit a project
Work in progress

### Delete a project
Work in progress
