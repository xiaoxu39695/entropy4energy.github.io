(() => {
  const today = new Date();
  for (const jobClosed of document.querySelectorAll('.job-date-close')) {
    const closeDate = new Date(jobClosed.querySelector('.job-date-close-text').innerText);
    if (closeDate < today) {
      jobClosed.nextElementSibling.classList.remove('noscript');  // see jobs.html template
      const jobStatus = jobClosed.nextElementSibling.querySelector('.job-date-stat-text');
      jobStatus.classList.remove("open");
      jobStatus.classList.add("closed");
      jobStatus.innerText = "Closed";
    }
  }
})();
