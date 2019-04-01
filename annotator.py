from collections import OrderedDict

import cv2
import argparse
import os

parser = argparse.ArgumentParser(description="AMI Dataset Annotator for Turn Yielding and Requesting")

parser.add_argument("--video_path", type=str, default='', required=True, help="The video path")

parser.add_argument("--step", type=int, default=25, help="The number of frames to step")

args = parser.parse_args()


def main():
    print(os.path.exists(args.video_path))
    cap = cv2.VideoCapture(args.video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    # time = cap.get(cv2.CAP_PROP_POS_MSEC)
    # print(time)
    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    record = False
    output = OrderedDict()
    while curr_frame < total_frames:
        ret, frame = cap.read()
        curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

        if curr_frame in output:
            text = 'Frame: %d, %s' % (curr_frame, output[curr_frame])
        else:
            text = 'Frame: %d' % curr_frame

        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        # cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame-1)
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
            # During pause, check to see if either <space> or "+" is pressed.
            # If so, release the pause.
            while key != ord(' '):
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
                    output[curr_frame] = 'requesting'
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
                    output[curr_frame] = 'yielding'
                    ret, frame = cap.read()
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

        # TODO: Discuss if annotate while video is playing.
        # # When "r" is pressed, record a turn requesting event
        # if key == ord('r'):
        #     print("recorded turn requesting:", curr_frame)
        #     output[curr_frame] = 'requesting'
        #
        # # When "y" is pressed, record a turn yielding event
        # if key == ord('y'):
        #     print("recorded turn yielding:", curr_frame)
        #     output[curr_frame] = 'yielding'

        print(curr_frame)







if __name__ == "__main__":
    main()