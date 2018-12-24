The package aims to eleminate print statements from applications code.
Through that it supports a good traceable formated console and an optional
file output.

The console output is normally a minimized information output.
The logfile output should be gathering all needed information for debugging.
For both cases script_logger provides foramt suggestions.

The logfile handling is time roated it means after a certain time a new
logfile will be automatically generated.
Several ways to treat the old ones are included

Although a leveled output behavior is possible e.g. that only warnings or erros
are send to console but every log is written to file.

See in module example or test.py how it works.