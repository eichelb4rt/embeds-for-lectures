# Embeds for lectures

## Config

Create the file `config.json`, just like `config-template.json`. Insert your webhook url where you need it. The embeds are then sent to that webhook, with the colour you specified in the config.

## Lecturers

You can add lecturers by creating a file `lecturers.json`, just like `lecturers-template.json`. The fields for a lecturer are:

- name
- id, some short id, used to refer to them in the modules
- url (optional), link to their website
- icon_url (optional), link to a picture

## Modules

You can add modules by creating a file `modules.json`, just like `modules-template.json`. The fields for a module are:

- title
- lecturer, use the id here
- color (optional), can be specified to override the standard color
- id (optional), some sort of uni-intern code for the module
- url (optional), link to the website of the module
- properties (optional), array of strings, useful for short information, is then formatted to a list
- contents (optional), contents of the lecture
- aims (optional), aims of the lecture
