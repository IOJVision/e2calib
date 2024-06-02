import numpy as np
import cv2
import glob
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import os

# Argument parser
parser = argparse.ArgumentParser(description='Camera calibration using chessboard images.')
parser.add_argument('-r', type=int, default=8, help='Number of inside corners in rows (default: 8)')
parser.add_argument('-c', type=int, default=7, help='Number of inside corners in columns (default: 7)')
parser.add_argument('-i', '--images', type=str, default='/home/user/Document/data/*.png', help='Path to the images (default: /home/user/Document/data/*.png)')
parser.add_argument('-s', '--saving', type=str, default='/home/user/Document/data/result/cam_calibration_matrix.yaml', help='Path to save the calibration parameters (default: /home/user/Document/data/result/cam_calibration_matrix.yaml)')
parser.add_argument('--save-img-dir', type=str, default='/home/user/Document/data/result', help='Directory to save images with drawn chessboard corners (default: /home/user/Document/data/result)')
args = parser.parse_args()

# Use the parsed arguments
a = args.r
b = args.c
images_path = args.images
saving_path = args.saving
save_img_dir = args.save_img_dir

# Create the directory to save images if it doesn't exist
os.makedirs(save_img_dir, exist_ok=True)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(b-1,a-1,0)
objp = np.zeros((a * b, 3), np.float32)
objp[:, :2] = np.mgrid[0:b, 0:a].T.reshape(-1, 2) * 20

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# Get the list of images
images = glob.glob(images_path)
images.sort()

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (b, a), None)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (b, a), corners2, ret)
        print(fname)
        
        # Save the image with drawn chessboard corners
        save_img_path = os.path.join(save_img_dir, os.path.basename(fname))
        cv2.imwrite(save_img_path, img)
    else:
        print("Not found", fname)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("ret: ", ret)
print("mtx: \n", mtx)  # Parameter matrix
print("dist: \n", dist)  # Distortion coefficient
print("rvecs: \n", rvecs)  # Rotation vectors
print("tvecs: \n", tvecs)  # Translation vectors

# solvePnP to get the rvec matrix and tvec matrix
retval, rvec_mat, tvec_mat = cv2.solvePnP(objp, corners2, mtx, dist)

# Rodriguez to find full rotation matrix
dst, jacobian = cv2.Rodrigues(rvec_mat)

# Re-projection error gives a good estimation of how exact the found parameters are
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error
print("total error: {}".format(mean_error / len(objpoints)))
total_error = mean_error / len(objpoints)
print(total_error)

# Transform the matrix and distortion coefficients to writable lists
data = {'camera_matrix': np.asarray(mtx).tolist(),
        'dist_coeff': np.asarray(dist).tolist(),
        'total_error': np.asarray(total_error).tolist(),
        'object_point': np.asarray(objpoints).tolist(),
        'image_point': np.asarray(imgpoints).tolist(),
        'rvecs': np.asarray(rvecs).tolist(),
        'tvecs': np.asarray(tvecs).tolist(),
        'objp': np.asarray(objp).tolist(),
        'corners2': np.asarray(corners2).tolist(),
        'rvec_mat': np.asarray(rvec_mat).tolist(),
        'tvec_mat': np.asarray(tvec_mat).tolist(),
        'rotation_full_mat': np.asarray(dst).tolist()}

# Save the data to a file
with open(saving_path, "w") as f:
    yaml.dump(data, f)

print("Calibration is Done, View Result at: ", saving_path)