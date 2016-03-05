# adams
A script to generate mp3 files from Douglas Adams "The Hitchhiker's guide..." wav files ripped from 3 CD BBC 2005 edition.
## usage
```
adams.py disk_number
```
where `disk_number` is 1, 2 or 3. 

Source wav files should be placed in subfolders named `disk 1`, `disk 2` and `disk 3`.
Wave files are expected to be named `Track nn` where `nn` is the track number on the disk.
Output is generated into subfolder `mp3`.
