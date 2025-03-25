class Token:
  def __init__(self, token_type, index, value = None, end_index = None):
    self.token_type = token_type
    self.value = value
    self.index = index
    self.end_index = end_index
  def add(self, other):
    self.value += other
  def __str__(self):
    if self.value == None:
      return self.token_type
    return f'{self.token_type} {self.value} at {self.index if self.index is not None else 0}'
  def __repr__(self):
    return self.__str__()

keyword_identifiers = ['pass', 'break', 'continue', 'return', 'raise', 'from', 'global', 'nonlocal', 'del', 'await', 'lambda',
                       'assert', 'import', 'as', 'class', 'def', 'async', 'if', 'elif', 'else', 'while', 'for', 'in',
                       'with', 'try', 'except', 'finally', 'match', 'case', 'type', 'yield', 'or', 'and', 'not', 'is']

literal_identifiers = ['True', 'False', 'None']

simple_operators = {
  '+': 'ADD',
  '-': 'SUB',
  '*': 'MUL',
  '/': 'DIV',
  '(': 'LPAREN',
  ')': 'RPAREN',
  '>=': 'GE',
  '>': 'GT',
  '==': 'EQ',
  '<': 'LT',
  '<=': 'LE',
  '!=': 'NEQ',
  ',': 'COMMA',
  ':': 'COLON',
  ';': 'SEMICOLON',
  '=': 'ASSIGN',
  '+=': 'ADD_ASSIGN',
  '-=': 'SUB_ASSIGN',
  '*=': 'MUL_ASSIGN',
  '/=': 'DIV_ASSIGN'
}

def any_simple_operator_startsWith(val):
  for simple_operator_chars in simple_operators.keys():
    if simple_operator_chars.startswith(val):
      return True
  return False

def is_valid_identifier_char(txt, first_char):
  if first_char:
    return txt.isalpha() or txt == '_'
  else:
    return txt.isalpha() or txt.isdigit() or txt == '_'

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
    if c_char == '':
      return Token('EOF', start_i, '', start_i)

    if c_char.isdigit():
      c_val = c_char
      while self.peek().isdigit():
        c_val += self.get()
      return Token('INT', start_i, c_val, self.get_pos())
    elif is_valid_identifier_char(c_char, True):
      c_val = c_char
      while True:
        n_val = self.peek()
        if not is_valid_identifier_char(n_val, False):
          break
        c_val += self.get()
      return Token('IDENTIFIER', start_i, c_val, self.get_pos())
    elif c_char == '"':
      c_val = ''
      ignore_next = False
      while True:
        n_val = self.get()
        if n_val == '':
          raise Exception(f"Unfinished string starting at {start_i}")
        if not ignore_next and n_val == "\\":
          ignore_next = True
          continue
        if not ignore_next and n_val == '"':
          ignore_next = False
          break
        ignore_next = False
        c_val += n_val
      return Token('STRING', start_i, c_val, self.get_pos())
    elif c_char == "'":
      c_val = ''
      ignore_next = False
      while True:
        n_val = self.get()
        if n_val == '':
          raise Exception(f"Unfinished string starting at {start_i}")
        if not ignore_next and n_val == "\\":
          ignore_next = True
          continue
        if not ignore_next and n_val == "'":
          ignore_next = False
          break
        ignore_next = False
        c_val += n_val
      return Token('STRING', start_i, c_val, self.get_pos())

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
      next_char = self.peek()
      if next_char == '':
        break
      current_simple_id += next_char
      if not any_simple_operator_startsWith(current_simple_id):
        break
      self.get()
      if current_simple_id in simple_operators:
        last_valid_operator = current_simple_id
        last_valid_operator_end_i = self.get_pos()

    if last_valid_operator is not None:
      self.set_pos(last_valid_operator_end_i)
      return Token(simple_operators[last_valid_operator], start_i, last_valid_operator, self.get_pos())
    # End

    raise Exception(f"Unexpected character at {start_i} - `{c_char}`")

  def run_scanner(self):
    tokens = []
    while self.cur_char_i <= len(self.c_str): # True
      token = self.scan()
      tokens.append(token)
      # if token.token_type == 'EOF':
      #   break
    
    tokens.pop() # Remove EOF token

    return tokens

str_input = open("input.txt", "r").read()
testScanner = Scanner(str_input)
tokens = testScanner.run_scanner()

def identifierStyle():
  if token.value in keyword_identifiers:
    return 'color: green;'
  elif token.value in literal_identifiers:
    return 'color: blue;'
  else:
    return ''

token_styles = {
  'ADD': 'color: red;',
  'SUB': 'color: red;',
  'MUL': 'color: red;',
  'DIV': 'color: red;',
  'IDENTIFIER': identifierStyle,
  'GE': 'color: red;',
  'GT': 'color: red;',
  'EQ': 'color: red;',
  'LT': 'color: red;',
  'LE': 'color: red;',
  'NEQ': 'color: red;',
  'COMMA': 'color: red;',
  'COLON': 'color: red;',
  'SEMICOLON': 'color: red;',
  'ASSIGN': 'color: red;',
  'ADD_ASSIGN': 'color: red;',
  'SUB_ASSIGN': 'color: red;',
  'MUL_ASSIGN': 'color: red;',
  'DIV_ASSIGN': 'color: red;',
  'STRING': 'color: brown;',
  'INT': 'color: aqua;'
}

last_coloured_index = 0
output = ''

def html_sanitize(txt):
  return txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;')

def wrap_text_in_element(txt, style=None):
  style = style if style is not None else ''
  changed_txt = txt.replace('\n', '<br/>').replace(' ', '&nbsp;')
  return f'<span style="{style}">{changed_txt}</span>'

for token in tokens:
  output += wrap_text_in_element(str_input[last_coloured_index:token.index])

  style = None
  if token.token_type in token_styles:
    if callable(token_styles[token.token_type]):
      style = token_styles[token.token_type]()
    else:
      style = token_styles[token.token_type]

  output += wrap_text_in_element(str_input[token.index:token.end_index], style)
  last_coloured_index = token.end_index
output += wrap_text_in_element(str_input[last_coloured_index:])

output = f'''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&family=Noto+Sans+JP:wght@100..900&display=swap" rel="stylesheet">
<div style=''>
{output}
</div>
'''

with open("output.html", 'w') as f:
  f.write(output)

print(output)