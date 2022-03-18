#pragma once

#include <thread>
#include <vector>
#include <functional>
#include <mutex>

class ThreadPool
{
public:
	ThreadPool();
	ThreadPool(int num_threads);

	~ThreadPool();

	void submitJob(const std::function<void()>& f);
	bool isWorking();

private:
	void threadLoop();

	std::vector<std::thread>		   _threads;
	std::vector<std::function<void()>> _jobs;
	std::mutex						   _mutex;
	std::mutex						   _waitMutex;
	std::condition_variable			   _condVar;
	bool							   _isRunning;
	int								   _threadsRunning;
};