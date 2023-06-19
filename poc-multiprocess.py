import multiprocessing

def my_function():
    # Code to be executed in the new process
    print("This is running in a new process")

def my_function2():
    # Code to be executed in the new process
    print("This is running in a new process 2")

if __name__ == "__main__":
    # Create a new process
    process = multiprocessing.Process(target=my_function)
    process2 = multiprocessing.Process(target=my_function2)
    
    # Start the process
    process.start()
    process2.start()
    print('this is the main process')
    
    # Wait for the process to complete
    process.join()
