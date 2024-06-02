# Camera Calibration Script

This script is designed for camera calibration using chessboard images. It finds the chessboard corners, refines them, and computes the camera matrix and distortion coefficients. Additionally, it saves images with drawn chessboard corners for visualization.

## Features

- Detects and refines chessboard corners in images.
- Computes camera calibration parameters (camera matrix, distortion coefficients, rotation vectors, and translation vectors).
- Saves processed images with drawn chessboard corners.
- Saves calibration parameters to a YAML file.

## Usage

To use this script, you need to pass the required arguments for the number of corners in the chessboard, paths to the images, and paths for saving the output.

### Command Line Arguments

- `-a`: Number of inside corners in rows (default: 8).
- `-b`: Number of inside corners in columns (default: 7).
- `-i` or `--images`: Path to the images (default: `/home/user/Document/data/*.png`).
- `-s` or `--saving`: Path to save the calibration parameters (default: `/home/user/Document/data/result/cam_calibration_matrix.yaml`).
- `--save-img-dir`: Directory to save images with drawn chessboard corners (default: `/home/user/Document/data/result`).

### Running the Script

```bash
python camera_calibration.py -a 8 -b 7 --images '/path/to/images/*.png' --saving '/path/to/save/calibration.yaml' --save-img-dir '/path/to/save/processed_images'
```

Ensure to enclose the paths in quotes if they contain spaces.

## Example

```bash
python camera_calibration.py -a 9 -b 6 --images '/home/user/calibration_images/*.png' --saving '/home/user/calibration_output/camera_calibration.yaml' --save-img-dir '/home/user/calibration_output/processed_images'
```

This example will:
- Use a chessboard with 9 rows and 6 columns of inside corners.
- Load images from the specified directory.
- Save the calibration parameters to the specified YAML file.
- Save the processed images with drawn chessboard corners to the specified directory.


## Additional Information

For more details on the calibration process and underlying algorithms, refer to the OpenCV documentation on [camera calibration](https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html).

## Contact

For any questions or issues, feel free to open an issue in the repository or contact the maintainer.
