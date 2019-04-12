#README file:
___________________________________________________________________________________________________________________



This is a multi-threaded text file indexing command line application in C. In this application, there is one producing thread and N number of consuming threads. The producing thread is responsible for scanning the input directory for any text files. The consuming threads process the text file.
At the end of main the application prints top 10 frequent words.





Usage:

The file path should be provided by the user in the form of command line arguments. For example: ./ssfi /home/user/Desktop

Generally, the number of consumers is 2, but they can be changed by a switch "-t". For example: ./ssfi -t 3 /home/user/Desktop

A make file has been provided to compile the "ssfi.c" file.
To compile just run "make" or "make compile" on the terminal.



Technical notes:

The problem is clearly a modified version of  "producer-consumer problem" or also known as "bounded buffer" problem. 
The producing thread writes into a shared buffer (an array of strings) and signals to all the consuming thread about a new entry using semaphore. Depending upon the CPU scheduler any of the consuming threads wake up and consumes i.e processes the file entry. The consumers must not work until there is at least one entry in the buffer and producer must not enter any files if the buffer is at its max capacity. This synchronisation between a producer thread and multiple threads is achieved by &full and &empty semaphores. 





1) No external library is used for the application, everything including data structures for the wordlist is implemented from scratch. (typedef struct __word_list_t)



2) Much care has been taken to engineer this so that the runtime complexity remains very minimal. To retrieve the top 10 words for the results, generally sorting of the list needs to be done, but that would cost Big O (NlogN) runtime(where N is the number of elements in the list).
So, cleverly in my approach scanning it 10 times was better as its time complexity is just asymptotically linear(Big O (N)).



Constraints:


The engineering of this application is such that the number of files to be processed must be known before, but this can be tackled by using a monitor variable. 

The number of files to be processed must be greated that number of worker threads. This is by the engineering of the application. For example if the number of working threads is 3 and files to be processed is 2, then this app will not work. To be more specific the number of files to be processed should be multiple of the number of worker threads. Correct usage can be number of files to be process = 15, worker threads = 3 OR files to be process = 18, worker threads = 9 files to be process = 22, worker threads = 11 etc



Future work can be:

Using a monitor variable to get the number of files to be processed, so that both the constraints can be eliminated.

I hope NetApp likes the project :)
