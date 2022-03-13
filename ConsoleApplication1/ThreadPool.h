#pragma once

#include <thread>
#include <vector>
#include <functional>
#include <mutex>

class ThreadPool
{
public:
	ThreadPool();
	~ThreadPool();

	void submitJob(const std::function<void()>& f);
	bool hasJobs();

private:
	void threadLoop();

	std::vector<std::thread>		   _threads;
	std::vector<std::function<void()>> _jobs;
	std::mutex						   _mutex;
	bool							   _isRunning;
};