# lockdown
#### run as admin to use password change feature
    from lockdown import Locker
    lock = Locker(panic=True,
                  panic_pass='panicpassword',
                  private_exes='notepad.exe',
                  pivate_paths=['c:']) #set up your Locker
                  
    lock.private_exes = 'secret.exe' #append more exes
    lock.private_exes = ['slack.exe', 'excel.exe'] #lists are ok too
    lock.private_paths = '/user' #add new paths the same way
    lock.run() #run main loop

