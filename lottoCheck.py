import requests
import os.path

class NotLottoNumber(Exception):
    'Raised when a number is not a valid lotto number'
    pass

class LottoAlreadyExists(Exception):
    'Raised when a duplicate lotto number is selected'
    pass


def getlottoresults() -> dict:
    url = 'https://gateway.mylotto.co.nz/api/results/v1/results/lotto'
    with requests.get(url) as response:
        if response.status_code == 200:
            print(f'Response ok')
            resultsJson = response.json()
            return resultsJson
        else:
            print(f'Response failed')

   
def checknumbers(results:dict) -> None:
    winningnumberscount = 0
    ournumbers:list[int] = getlottonumbers()
    numbersdata = results['lotto']['lottoWinningNumbers']
    winningnumbers = []
    for result in numbersdata['numbers']:
        if int(result) in ournumbers:
            winningnumberscount += 1
            winningnumbers.append(int(result))
        else:
            ...
    bonusball=int(numbersdata['bonusBalls'])
    if bonusball in ournumbers:
        bonusballwinner = True
        bonusballmessage = f' and the bonus ball {bonusball}'
    else:
        bonusballwinner = False
        bonusballmessage = ''
    
    match winningnumberscount:
        case 0:
            message = f'Not a winner this time, no numbers matched.'
            division = 8
        case 1:
            message = f'Not a winner this time, number matched: {', '.join(map(str,winningnumbers))}{bonusballmessage}.'
            division = 8
        case 2:
            message = f'Not a winner this time, numbers matched: {', '.join(map(str,winningnumbers))}{bonusballmessage}.'
            division = 8
        case 3:
            if bonusballwinner:
                message = f'Winner! You got {winningnumberscount} numbers and the Bonus Ball! Numbers matched: {', '.join(map(str,winningnumbers))} & Bonus Ball {bonusball}.'
                division = 6
            else:
                message = f'Winner! You got {winningnumberscount} numbers but not the bonus ball. Numbers matched: {', '.join(map(str,winningnumbers))}.'
                division = 7
        case 4:
            if bonusballwinner:
                message = f'Winner! You got {winningnumberscount} numbers and the Bonus Ball! Numbers matched: {', '.join(map(str,winningnumbers))} & Bonus Ball {bonusball}.'
                division = 4
            else:
                message = f'Winner! You got {winningnumberscount} numbers but not the bonus ball. Numbers matched: {', '.join(map(str,winningnumbers))}.'
                division = 5
        case 5:
            if bonusballwinner:
                message = f'Winner! You got {winningnumberscount} numbers and the Bonus Ball! Numbers matched: {', '.join(map(str,winningnumbers))} & Bonus Ball {bonusball}.'
                division = 2
            else:
                message = f'Winner! You got {winningnumberscount} numbers but not the bonus ball. Numbers matched: {', '.join(map(str,winningnumbers))}.'
                division = 3
        case 6:
            message = f'Winner! You got {winningnumberscount} numbers! Numbers matched: {', '.join(map(str,winningnumbers))}.'
            division = 1
    if division < 7:
        winnings = getwinnings(division, results,'lotto')*10
        winnings = winnings + getwinnings(division, results, 'powerBall')
        winnings = f'${winnings:,.2f}'
        headers = {'Title':'Team Lotto Winner!','Tags':'moneybag'}
    elif division == 7:
        winnings = f'40 Bonus Tickets and ${getwinnings(division, results, 'powerBall'):,.2f}'
        headers = {'Title':'Team Lotto Winner!','Tags':'moneybag'}
    else:
        winnings = None
        headers = {'Title':'Team Lotto Loss','Tags':'disappointed'}

    
    posturl = getposturl()
    data = f'{message} Winnings - {winnings}'
    requests.post(url=posturl, data=data, headers=headers)
    
def getwinnings(division:int, results:dict, type:str) -> float:
    divisiondata = results[type][f'{str.lower(type)}Winners']
    for div in divisiondata:
        if div['division'] == division:
            winnings = float(div['prizeValue'])
            return winnings
        else:
            continue
    
def getposturl() -> str:
    filename = 'posturl.txt'
    if os.path.isfile(filename):
        ...
    else:
        url = input('Enter the URL for the POST request: ')  
        with open(filename,'w') as newfile:
              newfile.write(url)
    
    with open(filename,'r') as file:
        posturl = file.read()
    return posturl

def getlottonumbers() -> list[int]:
    filename = 'lottonumbers.txt'
    if os.path.isfile(filename):
        ...
    else:
        numbers = userinputnumbers()
        with open(filename,'w+') as newfile:
            for number in numbers:
                newfile.write('%s\n' %number)
        
    with open(filename,'r') as file:
        ournumbers = []
        for line in file.readlines():
            ournumbers.append(int(line.strip('\n')))
    return ournumbers

def userinputnumbers() -> list[int]:
    numbers: list[int] = []
    numbercount = 0
    while numbercount < 6:
        number_str = input('Enter your lotto numbers one by one: ')
        try:
            number = int(number_str)
            if 0 < number <= 40:
                if number in numbers:
                    raise LottoAlreadyExists
                numbers.append(number)
                numbercount += 1
            else:
                raise NotLottoNumber
        except ValueError:
            print('This is not an integer. Please enter a valid integer.')
        except NotLottoNumber:
            print('This is not a valid lotto number. Please enter a number between 1 and 40.')
        except LottoAlreadyExists:
            print('You have already chosen this number. Please enter a unique number.')
    return numbers

def main() -> None:
    resultsJson = getlottoresults()
    checknumbers(resultsJson)
    

if __name__ == '__main__':
    main()