import numpy as np 

def frog(x): 
    x1, x2 = x 
    return (x1 * np.sin(np.sqrt(np.abs(x2 + 1 - x1))) * 
            np.cos(np.sqrt(np.abs(x1 + x2 + 1))) + 
            (x2 + 1) * np.cos(np.sqrt(np.abs(x2 + 1 - x1))) * 
            np.sin(np.sqrt(np.abs(x1 + x2 + 1)))) 

'''
# Example usage 
x = np.array([-100,100]) 
result = frog(x) 
print(result) 
'''
