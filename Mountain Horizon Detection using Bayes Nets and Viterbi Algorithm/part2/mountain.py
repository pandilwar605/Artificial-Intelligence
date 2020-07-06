#!/usr/local/bin/python3
#
# Authors: Anuj Godase (abgodase), Sanket Pandilwar (spandilw), Amogh Batwal (abatwal)
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019


from PIL import Image
import numpy as np
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = np.array(input_image.convert('L'))
    filtered_y = np.zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return np.sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 ))):
            image.putpixel((x, t), color)
    return image


#Function for Normalizing 
def norm(col_vector):
    return col_vector/np.sum(col_vector)

#Returns transition probabilities pij based on curr and prev column
def get_transition_prob(curr,rows,ind):
    curr=curr.T
#    rows=14
    transition_prob=np.zeros((curr.shape[0],1))
    total_rows=curr.shape[0]
    indexes=[] # will store only the indexes which are going to be visited from previous column's best row
    for i in range(1,rows):#only considering +- 10 percent of total rows      
        if(ind-i>=0):
            indexes.append(ind-i)
        if(ind+i<curr.shape[0]):
            indexes.append(ind+i)
        indexes.append(ind)
     
    for j in range(total_rows): #iterate over all the rows
        if(ind==j):
            prob=1
            transition_prob[j]=prob
            continue
        if(j in indexes):
            prob= 1/abs(ind-j) # assigning probabilities based on how far current row is from previous column's best row
            transition_prob[j]=prob      
    return transition_prob,indexes

# main program
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)
img=Image.open(input_filename)
img1=Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)

#### Part 1
x = np.uint8(255 * edge_strength / (np.amax(edge_strength)))
imageio.imwrite('edges.jpg', np.uint8(255 * edge_strength / (np.amax(edge_strength))))

# You'll need to add code here to figure out the results! For now,

#### Part 2
columns = edge_strength.shape[1] #number of columns in given image
rows=edge_strength.shape[0] #number of rows in given image
rows_to_calculate=int(0.1*rows) #Considering only +-10 percent of rows instead of 
#calculating prob for each co-ordinate to reduce computation


ridge_case1 = np.argmax(edge_strength, axis = 0)
imageio.imwrite("bayesnet.jpg", draw_edge(input_image, ridge_case1, (0, 0, 255), 5))

observed_var=edge_strength

viterbi=[]
vi= (1/rows) * norm(observed_var[:,0]) # uniform prior * initial emission
vi=np.reshape(vi,(vi.shape[0],1))
viterbi.append(vi)
for i in range(1,columns): #starting from column 1 since we know initial state probability already     

    ej_emission=norm(observed_var[:,i])
    ej_emission=np.reshape(ej_emission,(ej_emission.shape[0],1)) # reshaping into column vector
    pij_transition,indexes = get_transition_prob(observed_var[:,i], rows_to_calculate, np.argmax(vi)) # returns pij
    for j in range(rows):
        if(j not in indexes):
            ej_emission[j]=0
    
    vj_t_1 = ej_emission * np.max(3*vi*pij_transition)
    vj_t_1=np.reshape(vj_t_1,(vj_t_1.shape[0],1))
    vj_t_1=norm(vj_t_1) #normalizing vj vector to avoid underflow error
    vi=vj_t_1
    viterbi.append(vj_t_1)
    
viterbi=np.array(viterbi)

ridge_case2 = np.argmax(viterbi, axis = 1)
imageio.imwrite("viterbi.jpg", draw_edge(img, ridge_case2, (255, 0, 0), 5))

#### Part 3
human_op=np.zeros((edge_strength.shape)) #initializing viterbi matrix
gt_row=int(gt_row)
gt_col=int(gt_col)
vi=np.zeros((rows,1))
vi.put(gt_row,1.0)

#Going backwards from human input co-ordinates
for i in range(gt_col,-1,-1):
    ej_emission=norm(observed_var[:,i])
    ej_emission=np.reshape(ej_emission,(ej_emission.shape[0],1))
    pij_transition,indexes = get_transition_prob(observed_var[:,i], rows_to_calculate, np.argmax(vi))
    for j in range(rows):
        if(j not in indexes):
            ej_emission[j]=0
    vj_t_1 = ej_emission * np.max(2*vi*pij_transition)
    vj_t_1=np.reshape(vj_t_1,(vj_t_1.shape[0],1))
    vi=vj_t_1
    human_op[:,i]=vj_t_1.T
    
    
vi=np.zeros((rows,1)) 
vi.put(gt_row,1.0)

#Going forward from human input co-ordinate
for i in range(gt_col,columns):
    ej_emission=norm(observed_var[:,i])
    ej_emission=np.reshape(ej_emission,(ej_emission.shape[0],1))
    pij_transition,indexes = get_transition_prob(observed_var[:,i], rows_to_calculate, np.argmax(vi))
    for j in range(rows):
        if(j not in indexes):
            ej_emission[j]=0
    vj_t_1 = ej_emission * np.max(2*vi*pij_transition)
    vj_t_1=np.reshape(vj_t_1,(vj_t_1.shape[0],1))
    vi=vj_t_1
    human_op[:,i]=vj_t_1.T
    
ridge_case3 = np.argmax(human_op, axis = 0)
imageio.imwrite("humaninput.jpg", draw_edge(img1, ridge_case3, (0, 255, 0), 2))