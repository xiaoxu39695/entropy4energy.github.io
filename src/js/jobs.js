(() => {
  const today = new Date();
  for (const jobClosed of document.querySelectorAll('.job-date-close')) {
    const closeDate = new Date(jobClosed.innerText);
    if (closeDate < today) {
      const jobStatus = jobClosed.parentElement.nextElementSibling.querySelector('.job-date-stat');
      jobStatus.classList.remove("open");
      jobStatus.classList.add("closed");
      jobStatus.innerText = "Closed";
    }
  }
})();
