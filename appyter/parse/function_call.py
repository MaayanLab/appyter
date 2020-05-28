import re

class FunctionCallMatcher:
  '''
  Function call parser since regexd isn't good at nested structures.
    Uncomment prints for debugging.
  '''
  outer_pattern = re.compile(r'([A-Za-z_-]+)\(')
  controlChars = {
    '(': ')',
    '{': '}',
    '[': ']',
  }
  ignoreControlChars = {
    '"': '"',
    "'": "'",
    '#': '\n',
  }
  def finditer_inner(self, val):
    controlStack = []
    ignoreControl = None
    cur_ind = 0
    max_ind = len(val)
    start = 0
    end = None
    while end is None and cur_ind < max_ind:
      if ignoreControl is not None:
        if val[cur_ind] == ignoreControl:
          ignoreControl = None
      elif self.ignoreControlChars.get(val[cur_ind], None) is not None:
        ignoreControl = self.ignoreControlChars[val[cur_ind]]
      elif controlStack != [] and val[cur_ind] == controlStack[-1]:
        # print(controlStack)
        controlStack.pop(-1)
        if controlStack == []:
          end = cur_ind + 1
      elif self.controlChars.get(val[cur_ind], None) is not None:
        # print(controlStack)
        if controlStack == []:
          start = cur_ind
        controlStack.append(self.controlChars[val[cur_ind]])
      cur_ind += 1
    if end is not None:
      return (val[start:end], cur_ind)

  def finditer(self, val):
    cur_ind = 0
    max_ind = len(val)
    end = None
    while end is None and cur_ind < max_ind:
      m = self.outer_pattern.search(val[cur_ind:max_ind])
      # print(val[cur_ind:max_ind])
      # print(m)
      if m is None:
        end = True
      else:
        name = m.group(1)
        # print(name, m.span())
        cur_ind += m.span()[1] - 1
        inner_val = val[cur_ind:max_ind]
        # print(inner_val)
        ret = self.finditer_inner(inner_val)
        # print(ret)
        if ret is None:
          end = True
        else:
          call, last_ind = ret
          cur_ind += last_ind
          yield name + call
