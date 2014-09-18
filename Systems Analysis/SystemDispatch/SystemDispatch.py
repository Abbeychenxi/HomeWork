__author__ = 'Abbey'
#-*- coding: utf-8 _*_
import Queue

#任务对象
class Task(object):
    def __init__(self, arrivalTime_, taskQuantity_, priority_, id_):
        self.arrivalTime_ = arrivalTime_
        self.taskQuantity_ = taskQuantity_
        self.priority_ = priority_
        self.id_ = id_

    def __cmp__(self, other):
        if self.arrivalTime_ < other.arrivalTime_:
            return -1
        elif self.arrivalTime_ == other.arrivalTime_:
            if self.priority_ >= other.priority_:
                return -1
            else:
                return 1
        else:
            return 1


class Dispatcher(object):
    cpu = []#模拟cpu
    taskQueue = Queue.PriorityQueue()

    def popTask(self):
        nowTask = self.taskQueue.get()
        if len(self.cpu) == 0:#第一个任务直接进入cpu
            self.cpu.append(nowTask)
            print "Task to complete id: %d" % (nowTask.id_)
        else:
            duringTime = nowTask.arrivalTime_ - self.cpu[0].arrivalTime_
            if self.cpu[0].taskQuantity_ <= duringTime:#当前cpu空闲，任务直接进入cpu
                del self.cpu[0]
                self.cpu.append(nowTask)
                print "Task to complete id: %d" % (nowTask.id_)
            else:#退出当前任务，新任务进入cpu
                quantity = self.cpu[0].taskQuantity_ - duringTime
                if self.cpu[0].taskQuantity_ == 0:
                    quitTask = Task(nowTask.arrivalTime_, quantity, self.cpu[0].priority_)
                    self.taskQueue.put(quitTask)
                    del self.cpu[0]
                    self.cpu.append(nowTask)
                    print "Task to complete id: %d" % (nowTask.id_)
                else:
                    quitTask = Task(nowTask.arrivalTime_+1, quantity, self.cpu[0].priority_, self.cpu[0].id_)
                    self.taskQueue.put(quitTask)
                    del self.cpu[0]
                    self.cpu.append(nowTask)
                    print "Task to complete id: %d" % (nowTask.id_)
                    print "Old task go back to queue id: %d" % (quitTask.id_)

    def cpuStart(self, taskQueue):#模拟cpu状态
        self.taskQueue = taskQueue
        task0 = Task( 0, 0, 0, -1)
        self.cpu.append(task0)
        for time in range(0, 1000):#全局时间，代表进程时间
            print "current time " +str(time)
            if self.taskQueue.empty() == True:
                durTime = time - self.cpu[0].arrivalTime_
                if durTime >= self.cpu[0].taskQuantity_:
                    print "All task is done."
                    break
                else:
                    continue
            task = self.taskQueue.get()
            #print task.arrivalTime_
            if task.id_ == 0 and task.priority_ > self.cpu[0].priority_:
                print "target task come"
                res = time + task.taskQuantity_ - 1
                return res
            if time >= task.arrivalTime_ and task.priority_ > self.cpu[0].priority_:
                print "one task come"
                self.taskQueue.put(task)
                self.popTask()
                continue
            else:
                durTime = time - self.cpu[0].arrivalTime_
                if durTime >= self.cpu[0].taskQuantity_:
                    del self.cpu[0]
                    self.cpu.append(task0)
                if time > task.arrivalTime_:
                    task.arrivalTime_ = time
                self.taskQueue.put(task)
                continue

    def guessTime(self, setTime, taskWithoutPriority, li, top):
        limit = setTime - taskWithoutPriority.taskQuantity_#设置结束时间到目标任务进入cpu之间，cpu全部由目标任务占据
        priorityset = []#当前已有的优先级
        guessQ = Queue.PriorityQueue()
        bottom = 0
        for item in li:
            priorityset.append(item.priority_)
            if item.arrivalTime_ > limit:
                    continue
            guessQ.put(item)
        for attempt in range(1, 11):
            tempQ = guessQ
            guessPriority = (top + bottom)/2
            if priorityset.__contains__(guessPriority) == True:
                top += 1
                continue
            taskWithoutPriority.priority_ = guessPriority
            tempQ.put(taskWithoutPriority)
            time = self.cpuStart(tempQ)
            print "get res: " + str(time)
            if time == setTime:
                print("Success! find the priority: " + str(guessPriority))
                return guessPriority, tempQ
            elif time > setTime:
                bottom = guessPriority
            else:
                top = guessPriority
        print("find failed!")
        return -1


#task1 = Task(0, 2, 2, 1)
#task2 = Task(1, 3, 3, 2)
#task3 = Task(3, 4, 5, 3)
#task4 = Task(5, 1, 4, 4)
#task5 = Task(100, 10, 1, 5)

#task6 = Task(4, 3, -1, 0)
#setTime = 7

#li = [task1, task2]

#q = Queue.PriorityQueue()
#q.put(task1)
#q.put(task2)
#q.put(task3)
#q.put(task4)
#q.put(task5)
n = int(raw_input("任务数目: "))
lis = []
for t in range(0, n):
    task_ = raw_input()
    li = task_.split(" ")
    task = Task(int(li[0]), int(li[1]), int(li[2]), t)
    lis.append(task)

setTime = int(raw_input("目标任务完成时间: "))


cpuDispatch = Dispatcher()
#cpuDispatch.cpuStart(q)
cpuDispatch.guessTime(setTime, lis[0], lis, 5)

