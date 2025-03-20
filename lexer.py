class Token:
  def __init__(self, token_type, index, value = None):
    self.token_type = token_type
    self.value = value
    self.index = index
  def add(self, other):
    self.value += other
  def __str__(self):
    if self.value == None:
      return self.token_type
    return f'{self.token_type} {self.value} at {self.index if self.index is not None else 0}'
  def __repr__(self):
    return self.__str__()

simple_operators = {
  '+': 'ADD',
  '-': 'SUB',
  '*': 'MUL',
  '/': 'DIV',
  '(': 'LPAREN',
  ')': 'RPAREN',

#  '>=': 'GE',
#  '>': 'GT',
#  '==': 'EQ',
#  '<': 'LT',
#  '<=': 'LE',
#  '!=': 'NEQ'
}

def any_simple_operator_startsWith(val):
  for simple_operator_chars in simple_operators.keys():
    if simple_operator_chars.startswith(val):
      return True
  return False

class Scanner:
  def __init__(self, c_str = ""):
    self.c_str = c_str
    self.cur_char_i = 0

  def get(self):
    char = self.c_str[self.cur_char_i] if self.cur_char_i < len(self.c_str) else ''
    self.cur_char_i += 1
    return char

  def peek(self):
    return self.c_str[self.cur_char_i] if self.cur_char_i < len(self.c_str) else ''
  
  def get_pos(self):
    return self.cur_char_i
  def set_pos(self, i):
    self.cur_char_i = i

  def scan(self):
    if self.peek().isspace():
      self.get()
      while self.peek().isspace():
        self.get()
      #return Token('', start_i) # White character token
    
    start_i = self.get_pos()
    c_char = self.get()
    if c_char.isdigit():
      c_val = c_char
      while self.peek().isdigit():
        c_val += self.get()
      return Token('INT', start_i, c_val)
    elif c_char.isalpha():
      c_val = c_char
      while True:
        n_val = self.peek()
        if not n_val.isalnum() and not n_val.isdigit():
          break
        c_val += self.get()
      return Token('IDENTIFIER', start_i, c_val)
    
    # Handle simple operators
    # if simple_operators[c_char]:
    #  return Token(simple_operators[c_char], start_i)

    # More advanced processing of multi-char operators (?)
    current_simple_id = c_char
    if not any_simple_operator_startsWith(current_simple_id):
      raise Exception(f"Unexpected character at {start_i} - `{c_char}`")
    
    last_valid_operator = current_simple_id if current_simple_id in simple_operators else None
    last_valid_operator_end_i = self.get_pos() # Position where we renew scanning
    while True:
      current_simple_id += self.peek()
      if not any_simple_operator_startsWith(current_simple_id):
        break
      self.get()
      if current_simple_id in simple_operators:
        last_valid_operator = current_simple_id
        last_valid_operator_end_i = self.get_pos()
    
    if last_valid_operator is not None:
      self.set_pos(last_valid_operator_end_i)
      return Token(simple_operators[last_valid_operator], start_i)
    # End

    raise Exception(f"Unexpected character at {start_i} - `{c_char}`")
 
  def run_scanner(self):
    tokens = []
    while self.cur_char_i != len(self.c_str):
      token = self.scan()
      tokens.append(token)

    return tokens

testScanner = Scanner('''lubieplacki 1ele
gdak5 2+3*(76+8/3)+ 3*(9-3) 5''')
testScanner.run_scanner()
