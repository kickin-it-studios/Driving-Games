v1.0 of Drift Racing is finished!!!

The multiplayer and single player "drive mode" versions of Drift Racing are done at this point. The game automatically starts 1 or 2 person mode depending on the number of controllers plugged into the computer.
The game keeps track of laps and lap time, and if playing by yourself, the objective is to get as fast a lap as possible, or as many laps in a row as possible.

In multi-player, it's a race to complete 5 laps, with the counter resetting everytime you crash. Do you go as fast as you can, or play it safe when you have 4 laps completed?

There is obviously lots more work to do, but this version also made a TON of progress behind the scenes (and then promptly broke half of it when implementing multiplayer).

It broke commonly used game states into separate callable files, created a function that is implementable, as well as created configuration files to give greater control over maps, car characteristics, color schemes, and more. I've also begun to introduce a folder structure which should help keep everything organized.

I have not had a chance to test the frame rate on a mac yet, but i made a change that i'm hoping will improve things slightly. However, it is just a temporary solution as I ripped out all the time difference functions (meaning frames might not sync with real time or something).

That's all for now. 2 days left to implement an ai to run on it... don't think this is going to go well...