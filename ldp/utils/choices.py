from django.utils.datastructures import SortedDict

class Choices(object):
  """
  A helper for a django model fields choices parameter.

  >>> STATUSES = Choices((
                   (1, 'DRAFT', 'Draft'),
                   (2, 'PUBLISHED', 'Published'),
                 ))
  #Acts like a choices list
  >>> list(STATUSES)
  [(1, 'Live'), (2, 'Published')]

  #Has Attributes
  >>> STATUSES.DRAFT
  1

  #Can retrieve Label to an attribute/value
  >>> STATUSES.label(STATUSES.PUBLISHED)
  'Published'
  """
  def __init__(self, values):
    self.labels = SortedDict()
    for index, name, label in values:
      setattr(self, name, index)
      self.labels[index] = label

  def __iter__(self):
    return self.labels.iteritems()

  def __len__(self):
    return len(self.labels)

  def label(self, index):
    return self.labels[index]


