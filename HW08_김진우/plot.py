import matplotlib.pyplot as plt

def main():
    myfile = open("FirstChoice.txt", "r")
    firstList = []
    while True: 
        val = myfile.readline().rstrip() # 파일을 읽어서 한줄씩 읽어오기
        if val == "": # 파일이 끝나면
            break 
        firstList.append(eval(val)) # 파일에 있는 값을 리스트에 추가
    myfile.close()

    myfile = open("SimulatedAnnealing.txt", "r")
    annealList = []
    while True:
        val = myfile.readline().rstrip()
        if val == "":
            break
        annealList.append(eval(val))
    myfile.close()

    plt.plot(range(len(firstList)), firstList) 
    plt.plot(range(len(annealList)), annealList) 
    plt.xlabel("Number of Evaluations")
    plt.ylabel("Tour Cost")
    plt.title("Search Performance (TSP-100)")
    plt.legend(["First-Choice HC", "Simulated Annealing"])
    plt.show()

main()