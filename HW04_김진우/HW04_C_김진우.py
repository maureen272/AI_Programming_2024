import random

class Contestant: 
    def __init__(self, name="", score=0): 
        self._name = name
        self._score = score

    def getName(self):
        return self._name # 이름 반환
    
    def getScore(self):
        return self._score # 점수 반환
    
    def setScore(self,value):
        self._score = value # 점수 설정

class Human(Contestant):
    def makeChoice(self): 
        valid_choices = ['rock', 'scissors', 'paper'] # 유효한 선택지를 설정
        self._choice = input(f"{self.getName()}, enter your choice: ") # 가위/바위/보 중 하나를 입력받기
        while (self._choice not in valid_choices): # 유효한 선택지가 아닌 경우 유효하지 않음을 알리고 다시 입력받기
            print(f"invalid choice {self._choice}")
            self._choice = input(f"{self.getName()}, enter your choice: ")
        return self._choice
        
class Computer(Contestant):
    def makeChoice(self):
        self._choice = random.choice(['rock', 'scissors', 'paper'])  # 컴퓨터는 3가지의 선택지 중 랜덤으로 선택
        print(f"{self.getName()} chooses {self._choice}")
        return self._choice
    
def playGame(h, c): # 변경하면 안되는 코드
    choiceH = h.makeChoice()
    choiceC = c.makeChoice()
    if choiceH == choiceC:
        pass
    elif judge(choiceH, choiceC):
        h.setScore(h.getScore() + 1)
    else:
        c.setScore(c.getScore() + 1)

def judge(choiceH, choiceC): # 변경하면 안되는 코드
    if ((choiceH == 'rock' and choiceC == 'scissors') or
        (choiceH == 'paper' and choiceC == 'rock') or
        (choiceH == 'scissors' and choiceC == 'paper')):
        return True
    else:
        return False
def main():
   human_name = input("Enter name of human: ") # 사람 이름 입력받기
   computer_name = input("Enter name of computer: ") # 컴퓨터 이름 입력받기
   print("")

   h = Human(human_name) # 사람 객체 생성
   c = Computer(computer_name) # 컴퓨터 객체 생성


   for i in range(3) : # 한 게임이 끝날 때 마다 점수 출력 // three-game matches 이므로 3번 반복
       playGame(h, c) # 게임 진행
       print(f"{h.getName()}: {h.getScore()}, ", end="") 
       print(f"{c.getName()}: {c.getScore()}")
       print("")
   
   if(h.getScore() < c.getScore()) : # 컴퓨터가 이긴 경우
       print(f"{c.getName().upper()} WIN")
   elif(h.getScore() == c.getScore()) : # 비긴 경우
       print("TIE")
   else : # 사람이 이긴 경우
       print(f"{h.getName().upper()} WIN")
main()