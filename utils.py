'''
Preprocessing the image to get the sudoku grid
1. Preprocessing the image
2. Detect grid contour
3. Get the 4 vertices
4. Extract the grid
5. Create 81 boxes
6. Extract every box of the grid
7. Predict each number
8. Create a 9x9 board (sudoku data structure)
'''

# Libraries
import cv2
import numpy as np
import easyocr

# Global Variable
DIGITS = ['1','2','3','4','5','6','7','8','9']

# 1. Preprocess the image
def imPreprocess(img):
    '''Preprocess the image for a better image detection
    img: The image to preprocess, a class 'numpy.ndarray'
    '''
    # Change to black and white for a better reading of the image
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur image
    image = cv2.GaussianBlur(image, (9,9), 0)
    # Find boundaries in the image with Threshold
    image = cv2.adaptiveThreshold(image,
                                  255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY,
                                  11,
                                  2)
    # Invert the image
    image = cv2.bitwise_not(image)
    # Dilate the image to thick the font and contours
    # We need to create a kernel to dilate
    kernel = np.array([[0., 1., 0.],
                       [1., 1., 1.],
                       [0., 1., 0.]],
                       np.uint8)
    image = cv2.dilate(image, kernel)
    return image

# 2. Grid contour detection
def gridContour(img):
    '''Detect the contour of the grid
    img: Preprocessed image, a class 'numpy.ndarray'
    '''
    # Detect all contours
    contours, h = cv2.findContours(img,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    # Rearrange the contours depending on each area
    # The biggest area first (the grid)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    grid = contours[0]
    return grid

# 3. Get the 4 vertices
def getVertices(contour):
    '''Get the coordinates of the 4 vertices of the grid
    contour: Array of each point that conforms the contour
    ''' 
    # Find the 4 vertices of the grid
    vertices = cv2.approxPolyDP(contour, 50, True)
    # Return False if there are not 4 points
    if len(vertices) != 4:
        return False
    # Reorganize vertices with a list comprehension and sorted
    vertices = [vertex[0] for vertex in vertices]
    # Organize boundary vertices (min sum to max sum)
    vertices = sorted(vertices, key=sum)
    # Organize de 2nd and 3rd vertex
    if vertices[1][0] < vertices[2][0]:
        temp = vertices[1]
        vertices[1] = vertices[2]
        vertices[2] = temp
    return vertices

# 4. Extract the grid
def extractGrid(img, contour):
    '''Extract the grid from the image with the 4 vertices
    img: Original image, a class 'numpy.ndarray'
    '''    
    # Change the format of the list of vertices
    vertices = np.float32(getVertices(contour))
    # Create a new rectangle image
    vertices_2 = np.float32([[0, 0], [920, 0], [0, 920], [920, 920]])
    # Apply Perspective Transform Algorithm
    try:
        matrix = cv2.getPerspectiveTransform(vertices, vertices_2)
    except cv2.error:
        return False
    grid = cv2.warpPerspective(img, matrix, (920, 920))        
    return grid

# 5. Create 81 boxes
def getBoxes(img):
    '''Divide square image into 81 boxes
    img: Square image of 920x920 pixels
    '''
    # Get the image # of rows of the image
    side = img.shape[:1]
    # List of boxes
    squares = []
    # Divide the side into 9
    side = side[0] / 9 
    for j in range(9):
        for i in range(9):
            # Top left corner of a box
            p1 = (int(i * side), int(j * side))
            # Bottom right corner
            p2 = (int((i + 1) * side), int((j + 1) * side))         
            squares.append((p1, p2))
    # Return a list of of the coordinates of the boxes (pt1 to pt2)
    return squares

# 6. Extract every box of the grid
def extractBox(img):
    '''Prepare image and extract each box from the sudoku
    for a better digit recognition
    img: Square image of 920x920 pixels
    '''
    # Get a grid of boxes to split the image
    grid = getBoxes(img)

    # Preprocess the image
    # Dilate image
    kernel = np.array([[0., 1., 0.],
                       [1., 1., 1.],
                       [0., 1., 0.]],
                       np.uint8)
    img = cv2.dilate(img, kernel)
    # Change to black and white
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Invert image
    img = cv2.bitwise_not(img)

    # Invert color
    # Create a list to append all the split images
    squares = []
    for square in grid:
        # Slides [::] to travel from y[0] to y[1]
        # Slides [::] to travel from x[0] to x[1] 
        square = img[square[0][1]:square[1][1], square[0][0]:square[1][0]]
        squares.append(square)
    return squares   

# 7. Predict each number
def predictNumbers(boxes):
    '''Predict the numbers for each box,
    if no digit it will append 0
    boxes: Image of every box of the sudoku
    '''
    final_numbers = []
    # Configure the reades wirh easyocr
    reader = easyocr.Reader(['ru', 'en'])
    
    for box in boxes:
        # Blur each of the images
        box = cv2.blur(box,(3,3))
        # Read each box and predict the number
        number = reader.readtext(box,
                                 allowlist='123456789',
                                 text_threshold=0.5,
                                 mag_ratio=2,
                                 contrast_ths=0.8)
        
        # Append 0 if there is no prediction
        if not number or not number[0][1].isnumeric() or number[0][2] < 0.8:
            final_numbers.append(0)
            continue
        
        # Extract the number from the data structure
        number = int(number[0][1])

        # Check if the number is grater than 9
        if number > 9:
            # Offset the borders by 1 pixel until the number is less or equal to 9
            while True:
                # Make an offset from the borders of the image
                # Give a variable for the offset
                px = 1
                box = box[0 + px:box.shape[0] - px, 0 + px:box.shape[1] - px]
                # Read and predict the number again
                number = reader.readtext(box, 
                                    allowlist='123456789',
                                    text_threshold=0.5,
                                    mag_ratio=2,
                                    contrast_ths=0.8)
                # If the output is more or less than 1 item in the list
                if len(number) != 1:
                    continue
                # If the number is 1,2,3,4,5,6,7,8,9 append and break
                if number[0][1] in DIGITS:
                    final_numbers.append(int(number[0][1]))
                    break
        else:  
            # If the number is predicted append to the list        
            final_numbers.append(number)
    # Return a list of numbers
    return final_numbers

def getOriginalNumbers(board):
    '''Get the initial number indexes
    board: Matrix of 9x9 boxes
    '''
    indexes = []
    for row in range(9):
        for column in range(9):
            if board[row][column] != 0:
                indexes.append([row, column])
    return indexes

# 8. Create a 9x9 board (sudoku data structure)
def sudokuGrid(numbers):
    '''Create a 9x9 sudoku grid with all the values
    numbers: List of 81 numbers
    '''
    # Return a list reshaped by a grid of 9x9
    return np.array(numbers).reshape(9, 9)

# Center point of every box 
def centerPoints(img):
    '''Get the center posotion of each box
    img: a rectangle image
    '''
    # Create a list with all the center point of each box
    center_points = []
    # Get the boxes and the coordinates to put the number
    for box in getBoxes(img):
        # First we get the center of the box
        # Then we translate it to a quarter (botton left corner)
        # To have the number in the center
        x = ((box[0][0]+box[1][0]) // 2) - ((box[1][0]-box[0][0])//4)
        y = ((box[0][1]+ box[1][1]) // 2) + ((box[1][1]-box[0][1])//4)
        center_points.append(tuple([x,y]))
    return center_points

# 9. Display the board in the image
def displaySudoku(img, sudoku, original_numbers = [], show_original=True):
    '''Display the image with the solved sudoku
    img: Square image of the sudoku (the grid)
    sudoku: Sudoku solved. 2D array
    original_numbers: A list of list with the indices of the original numbers [row,column]
    show_original: Show the initial numbers
    '''    
    # Get the boxes and the coordinates to put the number
    center_points = centerPoints(img)

    # We copy the image
    grid_copy = img.copy()
    # Create a variable counter to keep track of the 81 box index
    counter = 0

    # Travel trough all rows and columns of the sudoku array
    for row in range(9):
        for column in range(9):
            # Put the number in the coordinates (center of the box)
            if show_original:
                cv2.putText(grid_copy,
                            str(sudoku[row][column]),
                            center_points[counter],
                            cv2.FONT_HERSHEY_COMPLEX,
                            2,
                            (0,0,255),
                            2,)
            else:
                # Check for the original numbers and dont put them
                if [row, column] not in original_numbers and not show_original:
                    cv2.putText(grid_copy,
                                str(sudoku[row][column]),
                                center_points[counter],
                                cv2.FONT_HERSHEY_COMPLEX,
                                2,
                                (0,0,255),
                                2,)
            # Increase the counter, the index of the box
            counter += 1
    return grid_copy

