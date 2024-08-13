import re

class JobListing:
    """
    A class to represent a job listing and extract relevant information from a job dictionary.

    Attributes:
        job_dict (dict): A dictionary containing job details fetched from an API.

    Methods:
        _parse_salary(salary_str: str) -> tuple:
            Parses a salary string to extract the minimum and maximum salary values.
        
        title() -> str:
            Extracts the job title from the job dictionary.

        id() -> str:
            Returns the job ID from the job dictionary.

        date() -> str:
            Returns the effective date of the job listing from the job dictionary.

        category() -> str:
            Returns the job category from the job dictionary.

        annual_salary_min() -> float or None:
            Returns the minimum annual salary for the job, or None if not available.

        annual_salary_max() -> float or None:
            Returns the maximum annual salary for the job, or None if not available.

        monthly_salary_min() -> float or None:
            Returns the minimum monthly salary for the job, or None if not available.

        monthly_salary_max() -> float or None:
            Returns the maximum monthly salary for the job, or None if not available.
    """
    def __init__(self, job_dict):
        """
        Initializes a JobListing instance with a dictionary of job details.

        Args:
            job_dict (dict): A dictionary containing job details such as title, ID, category, effective date,
                             and salary ranges.
        """
        self.job_dict = job_dict
    
    def _parse_salary(self, salary_str):
        min_max = re.findall(r'\$([\d,]+\.\d{2})', salary_str)
        if len(min_max) == 2:
            return float(min_max[0].replace(',', '')), float(min_max[1].replace(',', ''))
        return None, None
    
    @property
    def title(self):
        title_match = re.search(r'>(.*?)<', self.job_dict["Job Title"])
        return title_match.group(1) if title_match else None
    
    @property
    def id(self):
        return self.job_dict["Job ID (Job Code)"]

    @property
    def date(self):
        return self.job_dict["Effective Date"]
    
    @property
    def category(self):
        return self.job_dict["Job Category"]
    
    @property
    def annual_salary_min(self):
        annual_min, _ = self._parse_salary(self.job_dict["Annual Min - Max"])
        return annual_min
    
    @property
    def annual_salary_max(self):
        _, annual_max = self._parse_salary(self.job_dict["Annual Min - Max"])
        return annual_max
    
    @property
    def monthly_salary_min(self):
        monthly_min, _ = self._parse_salary(self.job_dict["Monthly Min - Max"])
        return monthly_min
    
    @property
    def monthly_salary_max(self):
        _, monthly_max = self._parse_salary(self.job_dict["Monthly Min - Max"])
        return monthly_max
