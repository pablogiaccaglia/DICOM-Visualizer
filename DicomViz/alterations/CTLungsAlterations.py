import numpy
from skimage import measure

def largestLabelVolume(im, bg = -1):
    vals, counts = numpy.unique(im, return_counts = True)
    counts = counts[vals != bg]
    vals = vals[vals != bg]
    if len(counts) > 0:
        return vals[numpy.argmax(counts)]
    else:
        return None


def segmentLungsMask(image, param, fill_lung_structures = True):
    # not actually binary, but 1 and 2.
    # 0 is treated as background, which we do not want
    binary_image = numpy.array(image >= param, dtype = numpy.int8) + 1
    labels = measure.label(binary_image)

    # Pick the pixel in the very corner to determine which label is air.
    # Improvement: Pick multiple background labels from around the patient
    # More resistant to “trays” on which the patient lays cutting the air around the person in half

    background_label = labels[0, 0, 0]

    # Fill the air around the person
    binary_image[background_label == labels] = 2

    # Method of filling the lung structures (that is superior to
    # something like morphological closing)
    if fill_lung_structures:
        # For every slice we determine the largest solid structure
        for i, axial_slice in enumerate(binary_image):
            axial_slice = axial_slice - 1
            labeling = measure.label(axial_slice)
            l_max = largestLabelVolume(labeling, bg = 0)

            if l_max is not None:  # This slice contains some lung
                binary_image[i][labeling != l_max] = 1
    binary_image -= 1  # Make the image actual binary
    binary_image = 1 - binary_image  # Invert it, lungs are now 1

    # Remove other air pockets inside body
    labels = measure.label(binary_image, background = 0)
    l_max = largestLabelVolume(labels, bg = 0)
    if l_max is not None:  # There are air pockets
        binary_image[labels != l_max] = 0

    return binary_image
