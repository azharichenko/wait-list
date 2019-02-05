# Questions
> To understand the decision whether to join the wait list for a course or to switch and enroll into a different course (course is not technically the correct term section is better)

__Minor note: Define terminology used__
__Minor investigation: Using ratemyprofessors and waitlist of their sections__

### Technical

- [ ] Optimized scraping tool
  - Rip course API from PittAPI and modify from our need
- [ ] Setting up
  - Initial Scrape
  - Have term separation (more of a storing problem)
  - Inital test runs
  - All subjects (with a few exclusions for obvious reason, PittAPI basically has the list)
  - How to account for the creation and deletion of classes (cough cough freshman)
  - Updating details (instructors is the issue, maybe keep track?)
- [ ] Distributed computing problem
  - One scraper vs many!
  - Docker? App Engine?
  - Obviously using async code for requests
  - Maybe just saving the webpage straight up?
    - Batch processing
- [ ] Storing and Schema
  - NoSQL and SQL
    - Elasticsearch or just some kind of Database
- [ ] Analyzing?
  - Spark/hadoop?
  - Kibana?
