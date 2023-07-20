# Babylon Lipsync

[Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) is a command-line tool created by Daniel S. Wolf that automatically creates mouth animation from voice recordings. You can use it for characters in computer games, in animated cartoons, or in any other project that requires animating mouths based on existing recordings.

Babylon Lipsync is an addon for [Blender](http://blender.org) that integrates Rhubarb Lip Sync and uses it to generate mouth-shape keyframes from blender shape keys.

For support using this addon in Blender, please report an issue at https://github.com/danemadsen/Babylon-Lipsync/issues

## Installation

Download a release from https://github.com/danemadsen/Babylon-Lipsync/releases.

Do **not** unzip the file.

In Blender, open Blender Preferences ``Edit -> Preferences`` select ``Add-ons`` and choose ``Install...``. In the file dialog, select the ``.zip`` file. Once installed, enable the add-on with the checkbox.

Download the latest rhubarb-lip-sync version from https://github.com/DanielSWolf/rhubarb-lip-sync

## Usage

Navigate to 'Object Data Properties' to view the Rhubarb Lipsync panel.

Ensure you have shape keys on your model that correspond to the phoneme set displayed on the github page for Rhubarb-Lipsync.

Assign each respective shape key to its respective slot.

Select a wav file to use a sound file.

(Optional) write the dialog of the sound file into the dialog text box

## Troubleshooting

In the event of problems, you can use the system console (Window->Toggle System Console on Windows, or start Blender from a command line on Mac/Linux) to get more info on progress and error messages. When reporting an issue, please include any errors reported here.
