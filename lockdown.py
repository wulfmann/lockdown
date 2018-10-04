import os
import psutil

class Locker:
  
  def __init__(self,
               lockdown=True,
               panic=False,
               user='%USERNAME%',
               panic_pass=None,
               private_paths=[],
               private_exes=[]
               ):
    self._lockdown = lockdown
    self._panic = panic
    self._user = user
    self._panic_pass = panic_pass
    self._private_paths = private_paths
    self._private_exes = private_exes
    self._connection_memory = {}
    self._process_memory = {}
    self._go = True
    
  @property
  def lockdown(self):
    return self._lockdown
    
  @property
  def panic(self):
    return self._panic
    
  @property
  def user(self):
    return self._user

  @property
  def private_paths(self):
    return self._private_paths
    
  @property
  def private_exes(self):
    return self._private_exes
    
  @property
  def panic_pass(self):
    return self._panic_pass
  
  @property
  def go(self):
    return self._go
    
  @lockdown.setter
  def lockdown(self, bool):
    if isinstance(bool, boolean):
      self._lockdown = bool

  @panic.setter
  def panic(self, panic):
    if isinstance(panic, boolean):
      self._panic = panic
      
  @panic_pass.setter
  def panic_pass(self, passwd):
    if isinstance(passwd, str):
      self._panic_pass = passwd
      
  @private_paths.setter
  def private_paths(self, paths):
    self._private_paths.extend(paths)
    
  @private_exes.setter
  def private_exes(self, exes):
    self._private_exes.extend(exes)
    
  @go.setter
  def go(self, go):
    if isinstance(go, boolean):
      self._go = go
    
  def set_state(self):
  
    ''' Set the current state of process list'''
    
    process_list = []
    for process_id in psutil.pids():
      try:
        temp_process = psutil.Process(process_id)
        process_list.append(temp_process)
        self._process_memory[process_id] = temp_process.name()
        self._connection_memory[temp_process.name()] = temp_process.connections()
      except Exception as err:
        pass
    return process_list

  def print_change(self, previous_process_list):
    
    ''' Print changes to process list to stdout'''
    
    current_process_list = self.set_state()
    matched = 0
    
    for proc_current in current_process_list:
      for proc_previous in previous_process_list:
        if proc_previous == proc_current:
          matched = 1
          break
      if not matched:
        name = str(proc_current.name()).lower()
        print(' +++ ' + name + ' : ' + str(proc_current.pid))
        if proc_current.connections():
          print(proc_current.connections())
        
        self._check(proc_current)
        
      matched = 0
    matched = 0
    
    for proc_previous in previous_process_list:
      try:
        name = proc_previous.name()
      except Exception as err:
        try:
          name = str(PROCESS_MEMORY[proc_previous.pid])
        except Exception as err:
          name = proc_previous
      for proc_current in current_process_list:
        if proc_previous == proc_current:
          matched = 1
          break
      if not matched:
        print(' --- ' + str(name) + ' : ' + str(proc_previous.pid))
      matched = 0

    return current_process_list

  def _check(self, proc_current):
    
    ''' Looking for exe or paths
    may trigger locks or password changes depending on flags set
    
    '''
    
    name = proc_current.name()
    for bad in self._private_paths:
      try: dir = proc_current.cwd().lower()
      except: dir = ''
      if bad in dir:
        if self._panic: self._change_password()
        if self._lockdown: self._lock_screen()

    if name in self._private_exes:
      if self._panic: self._change_password()
      if self._lockdown: self._lock_screen()

  def _lock_screen(self):
    
    ''' Lock the screen'''
    
    action = ('gnome-screensaver-command --lock', 'rundll32.exe user32.dll,LockWorkStation')[os.name == 'nt']
    os.system(action)

  
  def _change_password(self):

    ''' Change password
    windows specific
    '''
    
    try:
      os.system('net user ' + self._user + ' ' + self._panic_pass)
    except Exception as err:
      return 0
    return 1

  def run(self):
    
    ''' Loop to collect process state, check for not-allowed, and print changes to screen'''
    
    init = self.set_state()
    while self._go:
      init = self.print_change(init)
