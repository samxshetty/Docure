import cv2
import numpy as np

def extract_features_orb(img_path):
    # Read image as grayscale
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image at {img_path} could not be loaded.")
    
    # Create ORB detector object
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return keypoints, descriptors

def match_descriptors(descriptors1, descriptors2):
    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Calculate similarity percentage based on the number of good matches
    if len(descriptors1) == 0 or len(descriptors2) == 0:
        return 0.0  # Return 0 if either image has no descriptors
    
    similarity = len(matches) / min(len(descriptors1), len(descriptors2))
    similarity_percentage = similarity * 100
    return round(similarity_percentage, 2)

def match(path1, path2):
    _, descriptors1 = extract_features_orb(path1)
    _, descriptors2 = extract_features_orb(path2)
    
    if descriptors1 is None or descriptors2 is None:
        return 0.0  # Return 0 if descriptors could not be extracted
    
    similarity_percentage = match_descriptors(descriptors1, descriptors2)
    
    return similarity_percentage
