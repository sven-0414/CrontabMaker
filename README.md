# Swehockey Crontab Generator

This Python script fetches match schedules from stats.swehockey.se and generates crontab entries that run another script shortly after the matches should be finished. Useful for updating statistics after completed games.

Since the script is meant to run automatically, it contains no menus and is controlled via an argument: the series ID. You can find this in the URL on Swehockey, for example:  
https://stats.swehockey.se/ScheduleAndResults/Overview/15986

The script was only intended for my personal scripts that ran to update Wikipedia point tables during the 2023/24 season. Any other use is at your own risk.

## Usage
```bash
python3 main.py <series-id>
```
Example output:

```bash
0-55/5 21 30 3 * /opt/hockeytabeller.zsh
00 23 30 3 * /opt/hockeytabeller.zsh
```

## Installation
```bash
git clone https://github.com/sven-0414/CrontabGenerator.git
cd CrontabGenerator
pip install -r requirements.txt
```
## Development Notes

This project demonstrates AI-assisted development. The Python implementation was created through collaboration with ChatGPT, showcasing the ability to leverage AI tools for rapid prototyping and solving real automation problems despite limited Python experience.

## License

The code is distributed under Apache 2.0, which basically means you can use, modify and distribute the code as long as you include acknowledgment to the original author.
