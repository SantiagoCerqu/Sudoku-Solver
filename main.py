from utils import *
from sudoku_solver import *
import cv2
import re

img_path = 'static/temp/'

def changeName(name, value):
    '''Change the name and format for the different images
    name: original name of the image
    value: string value with the name of the process
    '''
    if matches := re.search(r"\w+", name):
        return f"{matches.group()}_{value}.png"

def solver(img_name):
    ''' Solve the sudoku and get the image of the process
    img_name: the name of the input image
    '''
    images = []
    # 1. Open the image
    img = cv2.imread(f'{img_path}{img_name}')
    # 2. Preprocess the image
    img_preprocess = imPreprocess(img)
    # 2.1 Save the preproces image
    image_name_preprocess = changeName(img_name,"preprocess")
    cv2.imwrite(f"{img_path}{image_name_preprocess}", img_preprocess)
    images.append(image_name_preprocess)
    # 3. Find Grid contour
    contour = gridContour(img_preprocess)
    # 4. Extract the grid with the original image
    img = extractGrid(img, contour)
    # if img == False:
    #     return False

    # 4.1 Save the grid image
    # Draw the boxes in the image
    img_boxes = img.copy()
    for box in getBoxes(img_boxes):
        cv2.rectangle(img_boxes,
                      tuple(box[0]),
                      tuple(box[1]),
                      (0,255,0),
                      2)
    
    image_name_grid = changeName(img_name, "grid")
    cv2.imwrite(f"{img_path}{image_name_grid}", img_boxes)
    images.append(image_name_grid)

    # 5. Extract each box of the grid
    boxes = extractBox(img)
    # 6. Predict each digit and create the grid
    numbers = predictNumbers(boxes)
    final_grid = sudokuGrid(numbers)
    # 6.1 Draw the original numbers in the grid
    predicted_numbers_img = img.copy()
    center_points = centerPoints(img_boxes)
    counter = 0
    for number in numbers:
        if number != 0:
            cv2.putText(predicted_numbers_img,
                        str(number),
                        center_points[counter],
                        cv2.FONT_HERSHEY_COMPLEX,
                        2,
                        (0,255,0),
                        2)
        counter += 1

    image_name_prediction = changeName(img_name, "prediction")
    cv2.imwrite(f"{img_path}{image_name_prediction}", predicted_numbers_img)
    images.append(image_name_prediction)

    # 7. Solve Sudoku with backtracking algorithm
    solved_sudoku = solveSudoku(final_grid.copy())
    # 8. Put the numbers in the grid image
    original_numbers = getOriginalNumbers(final_grid)
    final_image = displaySudoku(img, 
                                solved_sudoku,
                                original_numbers,
                                False)
    # Name the image to end with _solved.png and save    
    image_name_solved = changeName(img_name, "solved")
    cv2.imwrite(f"{img_path}{image_name_solved}", final_image)
    images.append(image_name_solved)
    # Return the name of the image
    return images

 
# def main():
#     # 1. Open the image
    
#     # filename = 
    
#     img = cv2.imread(f'{path}')
#     cv2.imshow('normal_image',img)

#     # 2. Preprocess the image
#     preprocess_img = imPreprocess(img)
#     # cv2.imshow('preprocessed_image', preprocess_img)

#     # 3. Find Grid contour
#     grid_contour = gridContour(preprocess_img)
#     # contour = cv2.drawContours(img.copy(), grid_contour, -1, (0,0,255), 5)
#     # cv2.imshow('contour_image', contour)

#     # 4. Extract the grid with the original image
#     grid = extractGrid(img, grid_contour)
#     # cv2.imshow('grid_image', grid)
#     # img_boxes = grid
#     # for box in getBoxes(grid):
#     #     cv2.rectangle(img_boxes,
#     #                   tuple(box[0]),
#     #                   tuple(box[1]),
#     #                   (0,255,0),
#     #                   2)
#     # cv2.imshow('Boxes', img_boxes)

#     # 5. Extract each box
#     numbers = extractBox(grid)
#     # Show every image
#     # counter = 0
#     # for number in numbers:
#     #     cv2.imshow(f'img_{counter}',number)
#     #     counter+=1

#     # 6. Predict each digit and create the grid
#     numbers = predictNumbers(numbers)
#     final_grid = sudokuGrid(numbers)

#     # 7. Solve Sudoku with backtracking algorithm
#     # Give a copy of the final_grid
#     solved_sudoku = solveSudoku(final_grid.copy())
    

#     # 8. Put the numbers in the grid image
#     # If I want to get only the numbers solved I set to False
#     initial_numbers = getOriginalNumbers(final_grid)
#     final_image = displaySudoku(grid, solved_sudoku,initial_numbers,False)  
#     # cv2.imshow('Solved_sudoku', final_image)

# if __name__ == "__main__":
#     main()