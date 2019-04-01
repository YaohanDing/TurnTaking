from collections import OrderedDict
import cv2
import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser(description="AMI Dataset Annotator for Turn Yielding and Requesting")

parser.add_argument("--video_path", type=str, default='', required=True, help="The video path")

parser.add_argument("--step", type=int, default=25, help="The number of frames to step")

args = parser.parse_args()


def main():
    print(os.path.exists(args.video_path))
    cap = cv2.VideoCapture(args.video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    record = False
    output = OrderedDict()
    while curr_frame < 40:
        ret, frame = cap.read()
        curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(curr_frame)

        if curr_frame in output:
            text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
        else:
            text = 'Frame: %d' % curr_frame

        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('im', frame)

        key = cv2.waitKey(delay=int(1000/frame_rate))

        if key == 27:
            exit()

        # Handles pressing <space> key to pause and restart video.
        # The video also plays when pressing the "+" key, which starts the recording
        if key == ord(' '):
            # Enters pause state. Video is paused beyond this point
            key = cv2.waitKey()
            if key == 27:
                exit()
            # During pause, check to see if <space> is pressed.
            # If so, release the pause.
            while key != ord(' ') and curr_frame < 40:
                if key == ord('a'):  # "a" is pressed step backwards
                    cap.set(cv2.CAP_PROP_POS_FRAMES, max(curr_frame - 1, 0))
                    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, frame = cap.read()
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    print("step back to:", curr_frame)

                if key == ord('d'):  # "d" is pressed, step forward
                    cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr_frame + 1, total_frames))
                    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, frame = cap.read()
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    print("step forward to:", curr_frame)

                # When "r" is pressed, record a turn requesting event
                if key == ord('r'):
                    print("recorded turn requesting:", curr_frame)
                    data = ['requesting']

                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    
                    # Available cues
                    cues = ['Quick Gaze Shift', 'Forward Leaning', 'Head Nodding', 'Hand Reaching Forward', 'Rapid Blinking', 'Mouth Attempting to Speak']

                    # Visualize cue selections
                    for i, c in enumerate(cues):
                        cv2.putText(frame, "%d. %s" % (i+1, c), (0, 20 * (i+2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    
                    # Select the cue to this frame from 1 to 6
                    selection = cv2.waitKey()
                    while selection not in range(49, 49 + len(cues)):
                        selection = cv2.waitKey()

                    # record and visualize the selection
                    num = selection-48
                    data.append(cues[num-1])
                    output[curr_frame] = data
                    text = 'Frame: %d, ' % curr_frame + str(data)
                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    output[curr_frame] = data

                    # Step forward 1 frame
                    cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr_frame + 1, total_frames))
                    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, frame = cap.read()
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    print(output)

                # When "y" is pressed, record a turn yielding event
                if key == ord('y'):
                    print("recorded turn yielding:", curr_frame)
                    data = ['yielding']
                    ret, frame = cap.read()
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                    # Available cues
                    cues = ['Gaze Fixating on Next Person(s)', 'Stopped Motions', 'Yielding Hand Gestures', 'More Opened Eyes']

                    # Visualize cue selections
                    for i, c in enumerate(cues):
                        cv2.putText(frame, "%d. %s" % (i+1, c), (0, 20 * (i+2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    
                    # Select the cue to this frame from 1 to 6
                    selection = cv2.waitKey()
                    while selection not in range(49, 49 + len(cues)):
                        selection = cv2.waitKey()

                    # record and visualize the selection
                    num = selection-48
                    data.append(cues[num-1])
                    output[curr_frame] = data
                    text = 'Frame: %d, ' % curr_frame + str(data)
                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    output[curr_frame] = data

                    # Step forward 1 frame
                    cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr_frame + 1, total_frames))
                    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, frame = cap.read()
                    
                    # Visualize the next frame
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    print(output)

                # When "n" is pressed, this is a negative example with neither turn requesting and turn yielding,
                # but displays some cues
                if key == ord('n'):
                    print("recorded negative:", curr_frame)
                    data = ['none']
                    ret, frame = cap.read()
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                    # Available cues
                    cues = ['Quick Gaze Shift', 'Forward Leaning', 'Head Nodding', 'Hand Reaching Forward', 'Rapid Blinking', 'Mouth Attempting to Speak', 
                            'Gaze Fixating on Next Person(s)', 'Stopped Motions', 'Yielding Hand Gestures', 'More Opened Eyes']

                    # Visualize cue selections
                    for i, c in enumerate(cues):
                        cv2.putText(frame, "%d. %s" % (i+1, c), (0, 20 * (i+2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    
                    # Select the cue to this frame from 1 to 6
                    selection = cv2.waitKey()
                    while selection not in range(49, 49 + len(cues)):
                        selection = cv2.waitKey()

                    # record and visualize the selection
                    num = selection-48
                    data.append(cues[num-1])
                    output[curr_frame] = data
                    text = 'Frame: %d, ' % curr_frame + str(data)
                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    output[curr_frame] = data

                    # Step forward 1 frame
                    cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr_frame + 1, total_frames))
                    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, frame = cap.read()
                    
                    # Visualize the next frame
                    if curr_frame in output:
                        text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
                    else:
                        text = 'Frame: %d' % curr_frame

                    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('im', frame)
                    print(output)

                # When "-" is pressed, delete an entry
                if key == ord('-'):
                    if curr_frame in output:
                        output.pop(curr_frame)
                        ret, frame = cap.read()
                        text = 'Frame: %d' % curr_frame

                        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.imshow('im', frame)

                    print(output)

                key = cv2.waitKey()
                if key == 27:
                    exit()

        if key == ord('a'):  # "a" is pressed
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(curr_frame - args.step, 0))
            curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            print("step back to:", curr_frame)

        if key == ord('d'):  # "d" is pressed
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr_frame + args.step, total_frames))
            curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            print("step forward to:", curr_frame)

    name = args.video_path.replace(".avi", ".csv")
    gather_outputs(name, output)

def gather_outputs(name, output):
    arr = []
    for key in sorted(output.keys()):
        arr.append([key, output[key][0], output[key][1]])

    df = pd.DataFrame(arr)
    df.to_csv(name, header=False)

if __name__ == "__main__":
    main()