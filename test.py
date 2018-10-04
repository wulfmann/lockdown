from lockdown import Locker
from action import Action, TriggerType


def custom():
  print('custom')

def main():
  
  action = Action(TriggerType.PROC_NAME, 'notepad.exe', custom)
  lock = Locker(panic=False, panic_pass='panicpassword') #set up your Locker
  lock.private_exes = 'secret.exe' #append more exes
  lock.private_exes = ['slack.exe', 'excel.exe'] #lists are ok too
  lock.private_paths = '/user'
  lock.run()

if __name__ == '__main__':
  main()