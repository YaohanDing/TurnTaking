# AMI dataset annotator for turn requesting and turn yielding
This is an interactive annotation script to create labels for the turn requesting and turn yielding. The annotator has been tested on python2.7 and python3.6.
# To run this annotator, you'll only need `annotator.py` and `requirements.py`, and follow the steps below: 
1. Clone this repository or download zip of this repository.
2. Install the required python packages:
```
pip install -r requirements.txt 
```
3. Start the annotator:
```
python annotator.py --video_path <path_to_your_video>
```

4. The video annotator will automatically play. When annotating, pause the video by pressing ``space`` and assign label by pressing 'r' for turn requesting, 'y' for turn yielding, and 'n' for an negative example.

5. Following the screen, select one of the listed cues.
