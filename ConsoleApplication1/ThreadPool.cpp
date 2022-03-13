#include "ThreadPool.h"
#include <iostream>

ThreadPool::ThreadPool() :
    _isRunning(true),
    _threadsRunning(0)
{
    int thread_count = std::thread::hardware_concurrency();

    if (thread_count == 0)
    {
        throw std::exception("Can't get core count.");
    }

    std::clog << "Creating " << thread_count << " threads." << std::endl;

    while (thread_count-- > 0)
    {
        _threads.push_back(
            std::thread(std::bind(&ThreadPool::threadLoop, this))
        );
    }
}

ThreadPool::~ThreadPool()
{
    _isRunning = false;

    for (int i = 0; i < _threads.size(); i++)
    {
        _threads[i].join();
    }
}

void ThreadPool::threadLoop()
{
    std::function<void()> job;

    while (_isRunning)
    {
        // Zona critica
        {
            std::unique_lock<std::mutex> waitLock(_waitMutex);

            if (_jobs.empty())
            {
                _condVar.wait(waitLock, [&]() { return !_jobs.empty(); });
            }

            // Retrieve job

            std::unique_lock<std::mutex> lock(_mutex);

            job = _jobs[0];
            _jobs.erase(_jobs.begin());

            _threadsRunning++;
        }
        // End zona critica

        if (job)
        {
            job();
        }

        {
            std::unique_lock<std::mutex> lock(_mutex);

            _threadsRunning--;
        }
    }
}

void ThreadPool::submitJob(const std::function<void()>& f)
{
    std::unique_lock<std::mutex> lock(_mutex);

    _jobs.push_back(f);

    _condVar.notify_one();
}

bool ThreadPool::isWorking()
{
    std::unique_lock<std::mutex> lock(_mutex);

    return _jobs.size() + _threadsRunning > 0;
}