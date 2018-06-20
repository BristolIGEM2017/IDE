# IDE

The iGEM Development Environment (IDE).

IDE is a useful tool to allow local development for iGEM wiki users.

If you are using IDE to help develop your Wiki please accredit the Bristol iGEM Team visibly on your collaboration page. The IDE was updated by iGEM Team Aachen for 2018.

## Setup

In order to use IDE you will need python3 installed. It can be downloaded here https://www.python.org/downloads/.

Firstly edit the file `settings.py` and enter your team_name as shown exactly on the iGEM wiki url to set up IDE to work with your team name.

Secondly create an IDE page at `2017.igem.org/Team:TeamName/IDE` by editing the wiki page and inserting only "IDE" as shown below for the Bristol team.

![](http://imgur.com/TQoEdXQ.png)

Then run `python3 server.py`. For this open the command line in windows.

Then go to `localhost:8000/Team:TeamName` in your browser. You should then see the original iGEM wiki template for Bristol.


## Editing

In order to edit the content go into the html folder

There are currently three sub-folders of importance:

 * css - This folder is where all your CSS should be stored. If you are planning
   on using Bootstrap 4, we have a customised version to increase compatibility
   with the iGEM wiki that can be found.
   [here](https://github.com/BristolIGEM2017/bootstrapIGEM ). CSS can be
   included with the `{{css/style}}` tag to include `style.css`.
 * js - This folder should contain all of your JavaScript files. JavaScript can
   be included with the `{{js/script}}` tag to include `script.js`
 * templates - This folder should contain your templates. For example, the
   original template is included. To use it on a page you add a reference to
   the template as in wiki, that is `{{templates/header}}` to reference
   the header template. Note due to the iGEM Wiki system all html templates must be included outside the `html` tag, either above or below it.

It is recommended that you have a generic header and footer template that apply
across the entirety of your wiki for ease of use.

The url correspond exactly to the folders i.e. to access a file called
`project.html` you must go to `localhost:8000/Team:Teamname/project`.

To have a page at `localhost:8000/Team:Teamname/project/description` it is
permissible to add additional folders, in this case you would require a file
called `description.html` in the folder `project`.

The base url is specified in `index.html` in the base html folder.

You do not need to restart the server to reload any of these files.


## Build

When you are ready to upload your wiki you will need to run the build script.
Simply run `python3 build.py`. The output will be written into the `dist/`
folder and the file directories correspond the to URLs they need to be uploaded
to on the iGEM website.

* css - All files under the css folder need to be uploaded to `"2017.igem.org/Template:TeamName/css/filepath"`.
* js - All files under the js folder need to be uploaded to `"2017.igem.org/Template:TeamName/js/filepath"`.
* templates - All files under the templates folder need to be uploaded to `"2017.igem.org/Template:TeamName/filepath"`.
* Everything else must be uploaded to the `"2017.igem.org/Team:TeamName/filepath"` however, for `index.html` you must remove `/index` from the filepath.

## Future
To be able to use this IDE in the fututre you just need to edit the python files and replace the 2018 references with 2019 (or any other year).

## Creators

**[Albert Wigmore](https://github.com/albertwigmore)** and **[Oliver Wright](https://github.com/meiamsome)**

If you require any assistance please contact aw13789@my.bristol.ac.uk
