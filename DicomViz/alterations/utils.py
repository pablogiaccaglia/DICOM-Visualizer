import copy
from collections import namedtuple

from ..alterations.CTLungsAlterations import segmentLungsMask

DicomMasks = namedtuple("DicomMasks", ["segmentedLungs", "segmentedLungsFill", "internalStructures"])


def getDicomMasks(originalImg, param):
    # get masks
    segmentedLungs = segmentLungsMask(originalImg, param, fill_lung_structures = False)
    segmentedLungsFill = segmentLungsMask(originalImg, param, fill_lung_structures = True)
    internalStructures = segmentedLungs - segmentedLungsFill
    dicomMasks = DicomMasks(segmentedLungs, segmentedLungsFill, internalStructures)
    return dicomMasks


def getSegmentedLungPixels(originalImg, segmentedLungsFill):
    # isolate lung from chest
    copied_pixels = copy.deepcopy(originalImg)
    for i, mask in enumerate(segmentedLungsFill):
        get_high_vals = mask == 0
        copied_pixels[i][get_high_vals] = 0

    return copied_pixels
