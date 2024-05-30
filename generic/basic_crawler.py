class Crawler:
  """
  A base class for implementing web crawlers.
  This class defines a single abstract method `run()` which needs to be implemented by subclasses
  to execute the crawling process.
  Methods:
      run(self)
          Execute the crawling process. This method needs to be implemented by subclasses.
  Example Usage:
      class MyCrawler(Crawler):
          def run(self):
              # Implement crawler logic here
              pass
  """
  def run(self):
    """
    Abstract method to execute the crawling process
    This method needs to be implemented by subclasses to define specific crawling functionalities
    Raises:
        NotImplementedError: If the method is called directly from the Crawler base class without
        being implemented by a subclass.
    """
    raise NotImplementedError("Implement me")