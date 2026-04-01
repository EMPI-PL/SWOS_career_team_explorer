# Changelog

### ver 0.42
* [FIX] Fixed issue where if Manager's name contains 16 characters it would fail to open .CAR file [#16](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/16) (@aerofan)
* [FIX] Fixed application would throw a bunch of errors if user decided cancel openning of .CAR file [#9](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/9)
* [FIX] Fixed last letter of that player's name with HEX value ending '0' would crash the app [#11](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/11) (@jwigert, @Jezza53)
* Code preparation for additional functionalities

---

### ver 0.41
* :star2: [NEW] Added ability to change bank balance [#6](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/6)
* [FIX] Spelling error in main screen [#13](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/13) (@Jezza53)
* other minor changes and optimizations

---

### ver 0.40
* :star2: [NEW] Player's individual skills are now displayed [#3](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/3)
* :star2: [NEW] Basic configuration file is available now under *CARexplorer.conf*
* :star2: [NEW] Generate XML data from SWOS/DATA directory for future editing
* [NEW] New buttons and options added to GUI  
  Currently mostly inactive due to work in progress
* [FIX] Opening another file will displays wrong info or leaves previously loaded data [#1](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/1)
* [FIX] Wrong names displayed on occasion [#2](https://github.com/EMPI-PL/SWOS_career_team_explorer/issues/2)
* [FIX] Corrected minimal requirements for Python (must be >=3.10)
* Changed name of launch file from *gui.py* to ***CARexplorer.py***
* Changed window size to include player's skills
* Changed color scheme for headers for better experience
* Changed background display only at app launch
* Changed background picture size to fit the new window
* other minor changes...

---

### ver 0.31
* Minor bugfixes

---

### ver 0.30
* :star2: [NEW] GUI created
* Minor bugfixes

---

### < ver 0.29
No public releases. Core created to read from *CAR* files