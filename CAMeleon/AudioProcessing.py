import moviepy.editor as mpe
from Utils import HiddenPrints, count_frames
import os
from MaskRCNN import wordInDict, index_dict

## This function takes the path to the video and creates an array where each element in the array denotes which objects to mask on that frame.
def get_objs_to_mask(videoPath, allWords):
    num_frames = count_frames(videoPath)

    incomingMaskings = []
    incomingMaskings.append(allWords)

    confirmedMaskings = []
    objectsToMask = []

    for i in range(num_frames):
        confirmedMaskings, incomingMaskings = update_confirmed_maskings(incomingMaskings, confirmedMaskings)
        currentRoundMaskings = ""
        for entry in confirmedMaskings:
            currentRoundMaskings = currentRoundMaskings + entry + ","
        objectsToMask.append(currentRoundMaskings)
    return objectsToMask

def update_confirmed_maskings(incoming, confirmed):
    for word in incoming:
        confirmed.append(word)
        incoming.remove(word)
    return confirmed, incoming

def add_audio_to_video(outputVideoPath, fps):
    out_clip = mpe.VideoFileClip(outputVideoPath)
    out_clip.write_videofile(outputVideoPath[:-3] + 'mp4', fps=fps)
    out_clip.close()
    return