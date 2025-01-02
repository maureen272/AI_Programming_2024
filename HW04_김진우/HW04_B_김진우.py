class Fraction():
    def __init__(self, numerator=0, denominator=1): # Numerator and denominator should be taken as int 라고 했으므로 int형으로 분자, 분모 설정
        self._numerator = int(numerator)  # 
        self._denominator = int(denominator)  
        
    def getNumerator(self): # 분자값 반환
        return self._numerator

    def setNumerator(self, value):  # 분자값 설정
        self._numerator = value

    def getDenominator(self):  #분모값 반환
        return self._denominator

    def setDenominator(self, value):  # 분모값 설정
        self._denominator = value

    def print(self):  # Fraction.print(): print the Fraction class like example I/O below. 라고 했으므로 예시와 같은 형태로 출력
        print('\nThe fraction is ', self.getNumerator(),'/',self.getDenominator(),sep='')


class IrreducibleFraction(Fraction):
    def __init__(self, numerator=0, denominator=1):
        super().__init__(numerator, denominator)
        self._GCD = self._GCD(self.getNumerator(), self.getDenominator())  # 약분을 해야하므로 _GCD함수를 사용해 최대공약수 찾기

    def _GCD(self, m, n):  # m : 분자, n : 분모
        if (m * n != 0): # 분자/분모 중 최소 하나가 0이 될 때까지 재귀
            if m > n:
                return self._GCD(n, m % n)
            else:
                return self._GCD(m, n % m)
        else: # 둘 중 하나가 0이면 재귀 탈출 후 아래의 코드 실행
            if m == 0:
                return n # m= 0이 되면 n이 최대공약수
            else:
                return m # n= 0이 되면 m이 최대공약수

    def print(self):
        self.setNumerator(self.getNumerator() // self._GCD)  # 분자를 최대공약수로 약분
        self.setDenominator(self.getDenominator() // self._GCD)  # 분모를 최대공약수로 약분
        print('The reduced fraction is ', self.getNumerator(),'/',self.getDenominator(), sep='') #출력


def main(): # 조건에 Do not modify main function 이라 되어있으므로 주어진 코드 그대로 사용
    numerator = eval(input('Enter the Numerator: '))
    denominator = eval(input('Enter the Denominator: '))
    fraction = Fraction(numerator, denominator)
    fraction.print()
    reduced_fraction = IrreducibleFraction(numerator, denominator)
    reduced_fraction.print()
main()