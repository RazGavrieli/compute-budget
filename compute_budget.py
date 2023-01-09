import logging as logger


logger.basicConfig(level=logger.INFO)
class median_budget:
    def __init__(self, total_budget: float, citizen_votes: list[list], t=None):
        self.C = total_budget
        self.AMOUNT_OF_ADDED_VOTES = len(citizen_votes)-1
        self.NUMBER_OF_CITIZENS = len(citizen_votes)
        self.NUMBER_OF_SUBJECTS = len(citizen_votes[0])
        self.votes = citizen_votes
        logger.info("init median budget algorithm, input: %d subjects, %d citizens", self.NUMBER_OF_SUBJECTS, self.NUMBER_OF_CITIZENS)
        self.subjects = []
        for i in range(self.NUMBER_OF_SUBJECTS):
            self.subjects.append(list())
        for citizen in citizen_votes:
            for indexOfSubject, subjectVote in enumerate(citizen):
                self.subjects[indexOfSubject].append(subjectVote)
        for subject in self.subjects:
            subject.sort()
        if len(self.subjects) < 10:
            logger.info("subjects before adding constant votes: %s", str(self.subjects))
        else:
            logger.info("skipping subject printing due to large size")
        self.medians = []
        self.choose_median()
        self.t = 0
        if t == None:
            self.find_t()
        else:
            self.t = t

        self.final_budget = []

        for i in range(self.AMOUNT_OF_ADDED_VOTES):
            for j in self.subjects:
                j.append(self.f(i+1, self.t))
        for i in self.subjects:
            i.sort()
        if len(self.subjects) < 10:
            logger.info("subjects after adding constant votes: %s", str(self.subjects))
        
        self.choose_median()

        for i in self.medians:
            self.final_budget.append(i)
        

    def find_t(self):
        # Set the initial values of t and the step size
        t = 0
        step = 0.5
        precision = 0.00001

        while True:
            current_budget = []

            currentsubjects = []
            for i in range(self.NUMBER_OF_SUBJECTS):
                currentsubjects.append(list())
            for citizen in self.votes:
                for indexOfSubject, subjectVote in enumerate(citizen):
                    currentsubjects[indexOfSubject].append(subjectVote)

            for i in range(self.AMOUNT_OF_ADDED_VOTES):
                for j in currentsubjects:
                    j.append(self.f(i+1, t))
            for i in currentsubjects:
                i.sort()
            self.choose_median(currentsubjects)
            
            for i in self.medians:
                current_budget.append(i)
            budget_sum = sum(current_budget)

            if abs(budget_sum-self.C) <= precision:
                self.t = t
                logger.info("found t: %f", t)
                break
            elif budget_sum < self.C:
                t += step
            elif budget_sum > self.C:
                t -= step
            step /= 2

    def add_k_votes(self):
        for i in range(self.NUMBER_OF_SUBJECTS):
            for j in range(self.AMOUNT_OF_ADDED_VOTES):
                self.subjects[i].append(j)

    def choose_median(self, currSubjects=None):
        if currSubjects == None:
            currSubjects = self.subjects
        self.medians = []
        for i in currSubjects:
            self.medians.append(i[int(len(i)/2)])

    def f(self, i, t):
        return self.C*min(1, i*t)

def check_budget(total_budget: float, citizen_votes: list[list], final_budget: list) -> bool: 
    """
    Gets a total budget (float) and a list of citizens (list of list of votes), and a list of allocated budget to each subject.
    returns True if the budget is allocated in a fair way to groups, False otherwise.
    >>> check_budget(100, [[100, 0, 0], [0, 0, 100]], compute_budget(100, [[100, 0, 0], [0, 0, 100]]))
    True
    >>> check_budget(100, [[100, 0, 0], [0, 0, 100]], [40, 60])
    False
    >>> check_budget(100, [[100, 0, 0], [0, 100, 0], [0, 100, 0], [0, 100, 0], [0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100]], [10.0, 30.0, 60.0])
    True
    >>> check_budget(100, [[100, 0, 0], [0, 100, 0], [0, 100, 0], [0, 100, 0], [0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100]], [50, 25, 25]) 
    False
    """
    for citizen in citizen_votes:
        for vote in citizen:
            if vote != 0 and vote != sum(citizen):
                logger.warning("can't check budget. citizen %s supports more than 1 subject", str(citizen))
                return True

    subjectSizes = [0]*len(citizen_votes[0])
    for citizen in citizen_votes:
        subjectSizes[citizen.index(sum(citizen))]+=1
    logger.info("citizens divided to subjects: %s", str(subjectSizes))

    for i in range(len(subjectSizes)):
        if round(final_budget[i]) != round(total_budget*(subjectSizes[i]/len(citizen_votes))):
            logger.info("%f != %f", round(final_budget[i]) , round(total_budget*(subjectSizes[i]/len(citizen_votes))))
            return False
    return True

def compute_budget(total_budget: float, citizen_votes: list[list], t=None) -> list[float]:
    """
    gets a total budget (float) and a list of citizens (list of list of votes). 
    prints to the stdout the budget allocated for each subject. 
    the function also checks the budget if its fair to groups (if applicable)
    >>> compute_budget(30, [[0, 0, 30], [15, 15 ,0], [15, 15, 0]])
    [12.0, 12.0, 6.0]
    >>> compute_budget(100, [[100, 0, 0], [0, 100, 0], [0, 100, 0], [0, 100, 0], [0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100]])
    [10.0, 30.0, 60.0]
    >>> compute_budget(30, [[0, 0, 6, 0, 0, 6, 6, 6, 6], [0, 6, 0, 6, 6, 6, 6, 0, 0], [6,0 ,0, 6, 6, 0, 0, 6, 6]])
    [2.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
    """
    number_of_subjects = len(citizen_votes[0])
    for i in citizen_votes:
        if len(i) != number_of_subjects:
            logger.error("bad input, number of subjects is not equal for all citizens")
            return
        if sum(i) != total_budget:
            logger.error("bad input, not all citizens voted for all the budget")
            return
    budget = median_budget(total_budget, citizen_votes, t)
    check_budget(total_budget, citizen_votes, budget.final_budget)
    return [round(h, 3) for h in budget.final_budget]

if __name__ == "__main__":
    import doctest
    #doctest.testmod()

    #compute_budget(100, [[100, 0, 0], [0, 0, 100]])
    #compute_budget(30, [[0, 0, 6, 0, 0, 6, 6, 6, 6], [0, 6, 0, 6, 6, 6, 6, 0, 0], [6,0 ,0, 6, 6, 0, 0, 6, 6]])
    #compute_budget(30, [[0, 0, 30], [15, 15 ,0], [15, 15, 0]])

    #print(compute_budget(100, [[100, 0, 0], [0, 100, 0], [0, 100, 0], [0, 100, 0], [0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100],[0, 0, 100], [0, 0, 100]]))

    ## SMALL CITY EXAMPLE
    import random
    subjects=10 
    budget=10_000
    citizens = []
    for i in range(100):
        current_citizen = [0] * subjects
        for j in range(budget) :
            current_citizen[random.randint(0, random.randint(0, subjects-1))] += 1 # remove the inner random number to get P=1/subjects
        citizens.append(current_citizen)
    res = compute_budget(budget, citizens)
    print(res, sum(res))
