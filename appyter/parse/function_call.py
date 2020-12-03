import re
import logging
logger = logging.getLogger(__name__)


class FunctionCallMatcher:
  '''
  Function call parser since regex isn't good at nested structures.
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
        logger.log(logging.DEBUG-1, controlStack)
        controlStack.pop(-1)
        if controlStack == []:
          end = cur_ind + 1
      elif self.controlChars.get(val[cur_ind], None) is not None:
        logger.log(logging.DEBUG-1, controlStack)
        if controlStack == []:
          start = cur_ind
        controlStack.append(self.controlChars[val[cur_ind]])
      cur_ind += 1
    if end is not None:
      return (val[start:end], cur_ind)

  def finditer(self, val, deep=False):
    cur_ind = 0
    max_ind = len(val)
    end = None
    while end is None and cur_ind < max_ind:
      m = self.outer_pattern.search(val[cur_ind:max_ind])
      logger.log(logging.DEBUG-1, val[cur_ind:max_ind])
      logger.log(logging.DEBUG-1, m)
      if m is None:
        end = True
      else:
        name = m.group(1)
        logger.log(logging.DEBUG-1, str((name, m.span())))
        cur_ind += m.span()[1] - 1
        inner_val = val[cur_ind:max_ind]
        logger.log(logging.DEBUG-1, inner_val)
        ret = self.finditer_inner(inner_val)
        logger.log(logging.DEBUG-1, ret)
        if ret is None:
          end = True
        else:
          call, last_ind = ret
          cur_ind += last_ind
          yield name + call
          if deep:
            for el in self.finditer(call):
              yield el
