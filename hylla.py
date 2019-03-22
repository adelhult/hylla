import os
import sys
import shutil
import datetime
from json import loads
import sqlite3
import click
import requests

# class used when displaying projects (might be a bit unecessary)
class Project:
    def __init__(self, name, path, tags, code, date, id):
        self.name = name
        self.dir = path
        self.tags = tags.split(', ')
        self.tags_str = tags
        self.code = code
        self.date = date
        self.id = id
    def __repr__(self):
        # logic to display even long names in a pretty way
        if len(self.name) <= 7:
            return f'{self.name}\t\ttags:{self.tags_str}'
        elif len(self.name) > 15:
            return f'{self.name[:13]}..\ttags:{self.tags_str}'
        else:
            return f'{self.name}\ttags:{self.tags_str}'

# an object used to send config data to every command
class Config(object):
     def __init__(self):
         self.location = False
         self.conn = False
         self.c = False
pass_config = click.make_pass_decorator(Config, ensure=True)


# Creating a click group
@click.group()
@click.option('--location',
              envvar='HYLLA_LOCATION',
              prompt='Specify a location to store your projects (or set HYLLA_LOCATION)',
              type=click.Path(exists=True, file_okay=False))
@pass_config
def cli(config, location):
    """Hylla - Organize all your projects from the command-line"""
    config.location = location
    # Database connection and vars
    conn = sqlite3.connect(os.path.join(location, 'hylla_database.db'))
    c = conn.cursor()
    # add to config object
    config.conn = conn
    config.c = c

    # Create the table, if it does not exist already.
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS projects (
                            name text,
                            path text,
                            tags text,
                            code text,
                            date text,
                            id integer primary key
        )""")

# 'Docs' command, used to open the docs/github in a browser window
@cli.command('docs')
def open_docs():
    """Open the documentation in your browser"""
    click.echo('https://www.github.com/adelhult/hylla')
    click.launch("https://www.github.com/adelhult/hylla")


# 'New' command:
@cli.command('new')
@click.argument('name')
@click.argument('tags', nargs=-1)
@click.option('--readme-template',
            envvar='HYLLA_README_TEMPLATE',
            type=click.Path(exists=True, dir_okay=False))
@click.option('--commands', is_flag=True)
@click.option('--clone', is_flag=True)
@click.option('--github', nargs=2)
@click.option('--migrate',
            type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--no-readme', is_flag=True)
@pass_config
def new(config, name, tags, readme_template, commands, clone, github, migrate, no_readme):
    """Create a new project"""
    clone_url = False
    # define vars project_name and project_dir
    project_name, project_dir = parse_project_data(name, config)

    # check if the project exists already and if that is the case, exit.
    if project_exists(project_name, project_dir, config):
        click.secho('Error! Project name is already used', bg='red', fg='white')
        sys.exit(0)

    # open the notepad if the user used the flag --commands
    if commands:
        MARKER = '# Everything above this line is executed when \'hylla open\' is used.'
        # If on windows, add a command to open a new cmd in the workin dir
        if os.name == 'nt':
            open_cmd_code = 'start "Hylla - {project_name}" /D . \n'
            code = click.edit(open_cmd_code + MARKER, require_save = False).split(MARKER, 1)[0]
        else:
            code = click.edit(MARKER).split(MARKER, 1)[0]
    else:
        if os.name == 'nt':
            code = 'start "Hylla - {project_name}" /D . \n'
        else:
            code = ''

    # Add to database
    add_to_database(project_name, project_dir, tags, config, code)
    click.secho('Project added to the database', bg='green', fg='black')

    # print info
    click.echo(f'Project name: {project_name}')
    click.echo(f'Tags: {tags}')

    # Migrate files to a new folder if the user used the migrate option, then exit.
    if migrate:
        print(f'All the files from {migrate} will be migrated to the new dir')
        # the copytree function creates a new
        shutil.copytree(migrate, project_dir)
        exit(0)
    else:
        # Create a project folder, if they did not the migrate function!
        os.mkdir(project_dir)
        click.echo('Project directory created!')

    # Logic for cloning from github or with the --clone command.
    if github:
        github_repos = f'https://api.github.com/users/{github[0]}/repos'
        # Try to get data from github
        try:
            r = requests.get(github_repos)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        # reading json data
        data = loads(r.text)
        repo_name = github[1]

        # Create a list with the names of all the repos.
        user_repos = []
        for repo in data:
            try:
                user_repos.append(repo['name'])
            except TypeError:
                # Failed to load data from user
                click.secho(f'Failed to load repository data for user "{github[0]}"',
                bg='red', fg='white')
                exit(0)

        while True:
            # Was a valid repo picked?
            if repo_name in user_repos:
                # find the clone_url.
                for repo in data:
                    if repo_name == repo['name']:
                        clone_url = repo['clone_url']
                        break
                break

            # if no repo with that named exists in the list
            else:
                # Alert the user!
                click.secho(f'{github[0]} has no repo named "{repo_name}"!', bg='red', fg='white')

                # Ask if they want to try again
                if not click.confirm('Would you like to choose from the existing repositories? ' \
                '(the attempt to clone will otherwise be aborted)'):
                    exit() # If the user said no, exit. otherwise move on:

                # The user chose to continue...
                # list all the repos:
                click.echo(f'Listing all repos belonging to {github[0]}')
                for name in user_repos:
                    click.echo(name)
                repo_name = click.prompt('Enter name')

    elif clone:
        clone_url = click.prompt('Git URL')

    # If a clone_url was specified in the code above, try to git clone.
    if clone_url:
        os.chdir(project_dir)
        os.system(f'git clone {clone_url} .')
        click.echo(f'Project directory cloned from {clone_url}!')
    # If the user choose not to clone a readme is created
    #(unless the user used the no_readme flag)
    elif not no_readme:
        create_readme(readme_template, project_dir, project_name)


# 'Open' command:
@cli.command('open')
@click.argument('name')
@click.option('--safe', is_flag=True)
@pass_config
def open_project(config, name, safe):
    """Open a project"""
    config.c.execute("SELECT * FROM projects WHERE name=:name", {'name':name})
    project = config.c.fetchone()

    # Maybe a file browser with the project should be opened
    # does the project exist?
    if not project:
        click.secho('Error! A project with that name does not exist', bg='red', fg='white')
        sys.exit(0)

    # Should perhaps parse the data to a Project object instead.
    # Check if the folder exists
    dir = project[1]
    if not os.path.exists(dir):
        click.secho('Error! The project directory is missing', bg='red', fg='white')
        click.secho('Creating a new one!', bg='green', fg='white')
        os.mkdir(dir)

    click.echo('Project directory:')
    click.echo(dir)

    if not safe:
        commands = project[3].split('\n')
        os.chdir(dir)
        for command in commands:
            os.system(command)
    else:
        click.echo('Safe mode is active and no commands are therefor executed')


# 'Edit' command:
@cli.command('edit')
@click.argument('variable', type=click.Choice(['name', 'tags', 'commands']))
@click.argument('name')
@pass_config
def edit(config, variable, name):
    """Edit a project"""

    #Look for data in the database
    config.c.execute("SELECT * FROM projects WHERE name=:name", {'name':name})
    collected_data = config.c.fetchone()

    #Check if such a project does exist, if not close the program.
    if not collected_data:
        click.echo("No project with that name exists!")
        exit(0)

    # Format the data using the format_projects function which creates an object
    # Note, format_projects needs a list.
    project = format_projects([collected_data])[0]

    if variable == 'name':
        click.echo("WIP")

    if variable == 'code':
        click.echo("WIP")

    elif variable == 'tags':
        click.echo(f'Current tags for "{project.name}": {project.tags}')
        click.echo('Write a list (seperated with commas followed by blank spaces) ' \
        'of all the tags that should be associated with the project.')
        new_tags = click.prompt('Input tags')
        if click.confirm(f'Do you really want to update the tags for "{project.name}"'):
            with config.conn:
                config.c.execute("UPDATE projects SET tags = ? WHERE name = ? ",
                (new_tags, name))
            click.echo('The changes has been made!')
        else:
            click.echo('No changes has been made!')
            exit(0)

# 'Remove' command:
@cli.command('remove')
@click.argument('name')
@pass_config
def remove(config, name):
    """Remove a project from the database"""
    config.c.execute("SELECT * FROM projects WHERE name=:name", {'name':name})
    if config.c.fetchone():
        if click.confirm(f'Are you sure you want to remove "{name}"'):
            with config.conn:
                config.c.execute('DELETE FROM projects WHERE name=:name', {'name':name})
                click.secho('The project has now been removed from the database!', bg='red', fg='white')
                click.echo('NOTE: All files are still left in the directory.')
        else:
            click.echo('OK, the project was not removed!')
    else:
        click.secho('Error! A project with that name does not exist', bg='red', fg='white')
        sys.exit(0)


# 'List' command:
@cli.command('list')
@click.option('--tag')
@click.option('--detailed', is_flag=True)
@pass_config
def list(config, tag, detailed):
    """List and search for projects"""
    if tag:
        config.c.execute("SELECT * FROM projects WHERE tags LIKE ? ORDER BY name COLLATE NOCASE ASC", (f'%{tag}%',))
    else:
        config.c.execute("SELECT * FROM projects ORDER BY name COLLATE NOCASE ASC")
    query_results = config.c.fetchall()

    # If no results, print message and exit program
    if len(query_results) <= 0:
        click.echo('No projects where found! :(')
        sys.exit(0)

    # If there were results print them all out
    for p in format_projects(query_results):
        if detailed:
            code = p.code[:24] + '...'
            click.secho(f'#{p.id}  {p.name}  {p.date}', bg='cyan', fg='black')
            click.echo(f'\ttags: {p.tags_str}')
            click.echo(f'\tpath: {p.dir}')
            click.echo(f'\tcommands: {code}')
        else:
            click.echo(p)


@cli.command('home')
@pass_config
def home(config):
    """ Open the dir with all the projects"""
    print(config.location)
    click.launch(config.location, locate=False)


# Function used to create the readme file
def create_readme(template_path, project_dir, project_name):
    file_path = os.path.join(project_dir, 'README.md')
    if not os.path.isfile(file_path):
        if template_path:
            # Makes a copy of the template file
            shutil.copyfile(template_path, file_path)
            click.echo('Created a README file based on the provided template')
        else:
            # No template file was provided, use the standard
            with open(file_path, 'w') as f:
                f.write(f'# {project_name}\n\n## TODO\n\n## Hylla\nThis file was generated by [Hylla](https://github.com/adelhult/hylla). If you wish to use a template of your own. Specifiy the environmental varible HYLLA_README_TEMPLATE.')
            click.echo('Created a standard README file')
    else:
        click.echo('A README does already exist in the folder')

def parse_project_data(name, config):
    project_name = name.strip().lower().replace(' ', '_')
    project_dir = os.path.join(config.location, project_name)
    return project_name, project_dir

# Determines if a project dir exits or if it is used in the database
def project_exists(name, dir, config):
    config.c.execute("SELECT * FROM projects WHERE name=:name", {'name':name})
    if os.path.exists(dir) or config.c.fetchone():
        return True
    return False

# Adds the project to the database
def add_to_database(name, dir, tags, config, code):
    date = str(datetime.date.today())
    tags_string = ', '.join(str(e) for e in tags)
    with config.conn:
        config.c.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, NULL)",
            (name, dir, tags_string, code, date))

def fetch_all_projects(config):
    config.c.execute("SELECT * FROM projects")
    return format_projects(config.c.fetchall())

def format_projects(data):
    projects = []
    for p in data:
        projects.append(Project(p[0],
                                p[1],
                                p[2],
                                p[3],
                                p[4],
                                p[5]))
    return projects

if __name__ == '__main__':
    cli()
