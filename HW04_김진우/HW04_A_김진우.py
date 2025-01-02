class Quizzes:
    def __init__(self, listOfGrades): 
        self._listOfGrades = listOfGrades

    def average(self):
        # drops the lowest grade 해야하기 때문에 먼저 정렬을 한 다음 최저 점수를 제거하고 평균을 계산
        if len(self._listOfGrades) > 1:
            sorted_grades = sorted(self._listOfGrades)  # 점수 정렬
            remaining_grades = sorted_grades[1:]  # 최저 점수 제거
            return sum(remaining_grades) / len(remaining_grades)  # 평균 계산
        else: # 점수가 1개인 경우 : 최저점수가 곧 자기자신이므로 그걸 제거하면 평균이 0 // 점수가 0개인 경우 : 점수가 없으므로 평균이 0
            return 0.0  
        
    def __str__(self):
        return f"Quiz average: {self.average():.1f}"

def main():
    listOfGrades = []  # declares an empty list listOfGrades 조건에 따라 리스트 생성
    for i in range(1, 7):  # request 6 quiz grades as inputs 조건 충족을 위한 코드
        grade = float(input(f'Enter grade on quiz {i}: '))  # 점수 입력 받기
        listOfGrades.append(grade)  # appends each of them to listOfGrades 조건에 따라 리스트에 추가
    q = Quizzes(listOfGrades)  
    print(q) 
main()