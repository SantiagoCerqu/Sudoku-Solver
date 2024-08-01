# SUDOKU SOLVER
#### Video Demo:  <https://youtu.be/x4pK-SwLGPg>

#### Description:
What is Sudoku Solver? Well, Sudoku Solver is not only a program that solves a puzzle of 9x9 square grid. It is a program that gets an image from the user and tries its best to detect every number from each box, then solve it and return an image with the solved puzzle. It is presented as a simiple web page for a better interaction with the user.

So now that we know that this is more than a sudoku solver, lets dive into the design and implementation of the project. Because of learning purposes and greater ease, I used Python 3 to be the perfect language for this program. Also, there is a huge number of tools and libraries in Python that can help you built many applications. In this case I use openCV and easyOCR for all the processing and detection of the image, and Flask for the web page.

The project is a receipt of 4 steps with one input and one (ore multiple) output. The input is an image of a unsolved sudoku puzzle, and the output is a PNG image of the same sudoku but solved. When the input image is uploaded, the server will preprocess the image, then it will try to detect each number and generate the 9x9 grid, next it will solve the sudoku and finally the image will be diplayed to the user. So let's look at each functionality in depth.

1. Image Preprocessing: In this process we preprocess the image for a better detection of the numbers and the grid. Here is is used openCV library wich is great for image manipulation. The color is changed to Black and white, we apply Blur to remove the noise and threshold it to clean up. Then we find the contours of the big box and create an square image with only the sudoku grid. 

2. Number Detection: To detect each of the numbers, we take the preprocessed image, draw all the 81 boxes and split the image with those boxes into 81 separated images. Each box must contain every box of the image (with or without numbers). Then we take all those images and process them to predict the numbers. For this project it is used easyOCR to recognize the digits, and more preprocessing of the images for a better recognition. If it dosen't recognize any number it will return 0. This prediction is not perfect yet. 

3. Solver: After we get a list of all 81 numbers, with the empty boxes as zeros we transfor the list into a two dimensional array of 9 rows and 9 columns (81 values). Here the sudoku is ready to be solved! We take this matrix and apply a programming method called Backtracking Algorithm, wich it uses brute force and recursion to solve it. It will try every possible attempt until it doesn't find any other empty box (Until there are no zeros), and return the matrix. Finally it will take that matrix and put every number on the empty boxes, and generate a PNG image with the solved sudoku.

4. Web Page: Here it was used Flask to connect python and web page, with HTML and Bootstrap. It is a simple input to get the image and then it displaly to the user all the images with the process and the final result.

As I told you before, the digit recognition is not perfect, sometimes it detects other numbers or can't detect the numbers. Working on this proyect helped me to understand how to work with pixels and how to obtain data from images. Also how to work with many differnt type of variables and data structures to solve problems. Thank you!
This is CS50X... 

### Images
![Alt text](screenshots/Screenshot 2024-08-01 at 9.24.38 AM.png)
