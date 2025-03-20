class token:
  def __init__(self, token_type, value = None):
    self.type = token_type
    self.value = value
  def add(self, other):
    self.value += other
  def __str__(self):
    if self.value == None:
      return self.type
    return f'{self.type} {self.value}'
  def __repr__(self):
    return self.__str__()

class Scanner:
  def __init__(self, c_str = ""):
    self.c_str = c_str
    self.cur_char_i = 0
    self.c_token = None
    # 0 = None
    # 1 = Building integer
    # 2 = Building identifier
    self.state = 0

  def get_next(self):
    char = self.c_str[self.cur_char_i] if self.cur_char_i < len(self.c_str) else ''
    self.cur_char_i += 1
    return char

  def peek_next(self):
    return self.c_str[self.cur_char_i] if self.cur_char_i < len(self.c_str) else ''

  def pop_token(self):
    prev_token = self.c_token
    self.c_token = None
    return prev_token

  def scan(self):
    # Normally checking the space would be here

    if self.state == 0:
      if self.peek_next().isspace(): # Check if the character we'll be loading is a white character
        self.get_next() # Skip the white character (space)
        return

      c_char = self.get_next()
      if c_char.isdigit():
        self.c_token = token('INT', c_char)
        self.state = 1
      elif c_char.isalpha():
        self.c_token = token('IDENTIFIER', c_char)
        self.state = 2
      elif c_char == '+': # TODO: Add to map perhaps?
        return token('ADD')
      elif c_char == '-':
        return token('SUB')
      elif c_char == '*':
        return token('MUL')
      elif c_char == '/':
        return token('DIV')
      elif c_char == '(':
        return token('LPAREN')
      elif c_char == ')':
        return token('RPAREN')
      else:
        raise Exception(f"Unexpected character at {self.cur_char_i - 1} - `{c_char}`")
    elif self.state == 1:
      p_char = self.peek_next()
      if p_char.isdigit():
        self.get_next()
        self.c_token.add(p_char)
      else:
        self.state = 0
        return self.pop_token()
    elif self.state == 2:
      p_char = self.peek_next()
      if p_char.isalnum():
        self.get_next()
        self.c_token.add(p_char)
      else:
        self.state = 0
        return self.pop_token()

  def run_scanner(self):
    tokens = []
    while self.cur_char_i != len(self.c_str):
      token = self.scan()
      if token != None:
        tokens.append(token)

    return tokens

testScanner = Scanner("lubieplacki 1ele gdak5 2+3*(76+8/3)+ 3*(9-3)")
testScanner.run_scanner()
