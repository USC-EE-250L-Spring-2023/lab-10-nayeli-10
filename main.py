# Lab 10: distributed computing 
# team member 1: nayeli de leon
# team member 2: michelle arredondo
import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px
import json

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
        
    Summary: Finds the next largest prime number from list by checking if the value, 
    represented by 'x', has any factors. If 'x' has no factors, i.e all x % i  
    
    Args: Data is a list of integer values
    
    Returns: List of prime values
 
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
   
    Summary: Finds the next largest prime number from list by checking if the value, 
    represented by 'x' is a square root   
    
    Args: Data is a list of integer values
    
    Returns: List of prime values 
    
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:

    """TODO: Document this function. What does it do? What are the inputs and outputs?
    Summary:
    
    Args:
    
    Returns: the mean values 
    
    """
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://172.20.10.2:5000' # server IP address

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
        
    elif offload == 'process1':
    
        def offload_process1(mydata):
            nonlocal data1  
            # TODO: Send a POST request to the server with the input data
            message1 = requests.post(f"{offload_url}/process1", json=mydata)
            #print("status code: ", message1.status_code)
            data1 = message1.json()
            return data1
            
        thread = threading.Thread(target=offload_process1, args=(data,)) 
        thread.start()
        data2 = process2(data)
        thread.join(2)
        
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        def offload_process2(mydata):
        	nonlocal data2
        	#Send a POST request to the server with the input data
        	message2 = requests.post(f"{offload_url}/process2", json=mydata)
        	data2 = message2.json()
        	return data2
        	
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join(2)

    elif offload == 'both':
        # TODO: Implement this case
        #Send a POST request to the server with the input data
        message1 = requests.post(f"{offload_url}/process1", json=data)
        message2 = requests.post(f"{offload_url}/process2", json=data)
        data1 = message1.json()
        data2 = message2.json()
        

    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
	modes = ['none', 'both', 'process1','process2']
	data = []
	times = []
	
	for mode in modes:
		for i in range(5): #range = 0-4
			#start time
			start = time.perf_counter() 
			
			#run offloading mode
			answer = run(mode)
			
			#end time
			end = time.perf_counter()
			execution_time = (end-start) * 1000 #milliseconds #where does total_seconds() come from?
			times.append(execution_time)
		time_mean = np.mean(times)
		time_std = np.std(times)
		
		data.append([mode, time_mean, time_std])
	
	df = pd.DataFrame(data, columns = ['mode','time_mean','time_std'])
	
	
    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels
	fig = px.bar (df, x = "mode", y = "time_mean", error_y = "time_std", labels = {"mode":"Offload Mode", "time_mean":"Time Mean (ms)"}, title= "Makespans (total execution time)")
	#fig.show()


    # TODO: save plot to "makespan.png"
	fig.write_image("makespan.png")


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()
