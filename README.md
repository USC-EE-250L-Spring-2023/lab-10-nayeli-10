# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- team member 1: nayeli de leon
- team member 2: michelle arredondo

## Lab Question Answers

Question 1: 
	Answer: It would be worthwhile to offload the one or two processing tasks to our PC when the task would take up a lot of energy and memory. It would not be worthwhile to offload a task when the task is so small it's not really worth it, and offloading can cause network latency.
source: chatGPT

Question 2: Why do we need to join the thread here?
	Answer: we join the thread there so that the program can wait for 
	process1 to do it's thing before process2 can join in as they take turns running

Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism	
	Answer: Since the Rpi is running our main.py and our PC is running our server,
	the processing functions are executing in parallel. 2 different CPUs are being used
	source: article from above 

Question 4: What is the best offloading mode? Why do you think that is?
	Process 2 seems to be the best offloading mode since it has a shorter time, hence it's faster. It 
	can run two 

Question 5: What is the worst offloading mode? Why do you think that is?

Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?


